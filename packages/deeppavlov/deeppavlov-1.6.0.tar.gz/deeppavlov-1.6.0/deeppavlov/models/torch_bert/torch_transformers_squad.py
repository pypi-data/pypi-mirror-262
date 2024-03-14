# Copyright 2017 Neural Networks and Deep Learning lab, MIPT
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from collections import namedtuple
from logging import getLogger
from pathlib import Path
from typing import List, Tuple, Optional, Dict

import numpy as np
import torch
from transformers import AutoModelForQuestionAnswering, AutoConfig, AutoModel
from transformers.data.processors.utils import InputFeatures

from deeppavlov.core.commands.utils import expand_path
from deeppavlov.core.common.errors import ConfigError
from deeppavlov.core.common.registry import register
from deeppavlov.core.models.torch_model import TorchModel

logger = getLogger(__name__)


def softmax_mask(val, mask):
    inf = 1e30
    return -inf * (1 - mask.to(torch.float32)) + val


class PassageReaderClassifier(torch.nn.Module):
    """The model with a Transformer encoder and two linear layers: the first for prediction of answer start and end
    positions, the second defines the probability of the paragraph to contain the answer.

    Args:
        config: path to Transformer configuration file
    """

    def __init__(self, config):
        super().__init__()
        self.encoder = AutoModel.from_config(config=config)
        self.qa_outputs = torch.nn.Linear(config.hidden_size, 2)
        self.qa_classifier = torch.nn.Linear(config.hidden_size, 1)

    def forward(self, input_ids, attention_mask, token_type_ids):
        out = self.encoder(input_ids=input_ids, token_type_ids=token_type_ids, attention_mask=attention_mask)
        logits = self.qa_outputs(out[0])
        start_logits, end_logits = logits.split(1, dim=-1)
        start_logits = start_logits.squeeze(-1)
        end_logits = end_logits.squeeze(-1)
        rank_logits = self.qa_classifier(out[0][:, 0, :])
        outputs = namedtuple("outputs", "start_logits end_logits rank_logits")
        return outputs(start_logits=start_logits, end_logits=end_logits, rank_logits=rank_logits)


@register('torch_transformers_squad')
class TorchTransformersSquad(TorchModel):
    """Bert-based on PyTorch model for SQuAD-like problem setting:
    It predicts start and end position of answer for given question and context.

    [CLS] token is used as no_answer. If model selects [CLS] token as most probable
    answer, it means that there is no answer in given context.

    Start and end position of answer are predicted by linear transformation
    of Bert outputs.

    Args:
        pretrained_bert: pretrained Bert checkpoint path or key title (e.g. "bert-base-uncased")
        attention_probs_keep_prob: keep_prob for Bert self-attention layers
        hidden_keep_prob: keep_prob for Bert hidden layers
        bert_config_file: path to Bert configuration file, or None, if `pretrained_bert` is a string name
        psg_cls: whether to use a separate linear layer to define if a passage contains the answer to the question
        batch_size: batch size for inference of squad model
    """

    def __init__(self,
                 pretrained_bert: str,
                 attention_probs_keep_prob: Optional[float] = None,
                 hidden_keep_prob: Optional[float] = None,
                 bert_config_file: Optional[str] = None,
                 psg_cls: bool = False,
                 batch_size: int = 10,
                 **kwargs) -> None:
        self.batch_size = batch_size
        self.psg_cls = psg_cls

        if pretrained_bert:
            logger.debug(f"From pretrained {pretrained_bert}.")
            config = AutoConfig.from_pretrained(pretrained_bert, output_attentions=False, output_hidden_states=False)
            if self.psg_cls:
                model = PassageReaderClassifier(config=config)
            else:
                model = AutoModelForQuestionAnswering.from_pretrained(pretrained_bert, config=config)

        elif bert_config_file and Path(bert_config_file).is_file():
            bert_config = AutoConfig.from_json_file(str(expand_path(bert_config_file)))
            if attention_probs_keep_prob is not None:
                bert_config.attention_probs_dropout_prob = 1.0 - attention_probs_keep_prob
            if hidden_keep_prob is not None:
                bert_config.hidden_dropout_prob = 1.0 - hidden_keep_prob
            if self.psg_cls:
                model = PassageReaderClassifier(config=self.bert_config)
            else:
                model = AutoModelForQuestionAnswering(config=self.bert_config)
        else:
            raise ConfigError("No pre-trained BERT model is given.")
        super().__init__(model, **kwargs)

    def train_on_batch(self, features: List[List[InputFeatures]],
                       y_st: List[List[int]], y_end: List[List[int]]) -> Dict:
        """Train model on given batch.
        This method calls train_op using features and labels from y_st and y_end

        Args:
            features: batch of InputFeatures instances
            y_st: batch of lists of ground truth answer start positions
            y_end: batch of lists of ground truth answer end positions

        Returns:
            dict with loss and learning_rate values

        """
        input_ids = [f[0].input_ids for f in features]
        input_masks = [f[0].attention_mask for f in features]
        input_type_ids = [f[0].token_type_ids for f in features]

        b_input_ids = torch.cat(input_ids, dim=0).to(self.device)
        b_input_masks = torch.cat(input_masks, dim=0).to(self.device)
        b_input_type_ids = torch.cat(input_type_ids, dim=0).to(self.device)

        y_st = [x[0] for x in y_st]
        y_end = [x[0] for x in y_end]
        b_y_st = torch.from_numpy(np.array(y_st)).to(self.device)
        b_y_end = torch.from_numpy(np.array(y_end)).to(self.device)

        input_ = {
            'input_ids': b_input_ids,
            'attention_mask': b_input_masks,
            'token_type_ids': b_input_type_ids,
            'start_positions': b_y_st,
            'end_positions': b_y_end,
            'return_dict': True
        }

        self.optimizer.zero_grad()
        input_ = {arg_name: arg_value for arg_name, arg_value in input_.items() if arg_name in self.accepted_keys}
        loss = self.model(**input_).loss
        if self.is_data_parallel:
            loss = loss.mean()
        self._make_step(loss)

        return {'loss': loss.item()}

    @property
    def accepted_keys(self) -> Tuple[str]:
        if self.is_data_parallel:
            accepted_keys = self.model.module.forward.__code__.co_varnames
        else:
            accepted_keys = self.model.forward.__code__.co_varnames
        return accepted_keys

    def __call__(self, features_batch: List[List[InputFeatures]]) -> Tuple[
        List[List[int]], List[List[int]], List[List[float]], List[List[float]], List[int]]:
        """get predictions using features as input

        Args:
            features_batch: batch of InputFeatures instances

        Returns:
            start_pred_batch: answer start positions
            end_pred_batch: answer end positions
            logits_batch: answer logits
            scores_batch: answer confidences
            ind_batch: indices of paragraph pieces where the answer was found

        """
        predictions = {}
        # TODO: refactor batchification
        indices, input_ids, input_masks, input_type_ids = [], [], [], []
        for n, features_list in enumerate(features_batch):
            for f in features_list:
                input_ids.append(f.input_ids)
                input_masks.append(f.attention_mask)
                input_type_ids.append(f.token_type_ids)
                indices.append(n)

        num_batches = len(indices) // self.batch_size + int(len(indices) % self.batch_size > 0)
        for i in range(num_batches):
            b_input_ids = torch.cat(input_ids[i * self.batch_size:(i + 1) * self.batch_size], dim=0).to(self.device)
            b_input_masks = torch.cat(input_masks[i * self.batch_size:(i + 1) * self.batch_size], dim=0).to(self.device)
            b_input_type_ids = torch.cat(input_type_ids[i * self.batch_size:(i + 1) * self.batch_size],
                                         dim=0).to(self.device)
            input_ = {
                'input_ids': b_input_ids,
                'attention_mask': b_input_masks,
                'token_type_ids': b_input_type_ids,
                'return_dict': True
            }

            with torch.no_grad():
                input_ = {arg_name: arg_value for arg_name, arg_value in input_.items()
                          if arg_name in self.accepted_keys}
                # Forward pass, calculate logit predictions
                outputs = self.model(**input_)

                logits_st = outputs.start_logits
                logits_end = outputs.end_logits

                bs = b_input_ids.size()[0]
                seq_len = b_input_ids.size()[-1]
                mask = torch.cat([torch.ones(bs, 1, dtype=torch.int32),
                                  torch.zeros(bs, seq_len - 1, dtype=torch.int32)], dim=-1).to(self.device)
                logit_mask = b_input_type_ids + mask
                logits_st = softmax_mask(logits_st, logit_mask)
                logits_end = softmax_mask(logits_end, logit_mask)

                start_probs = torch.nn.functional.softmax(logits_st, dim=-1)
                end_probs = torch.nn.functional.softmax(logits_end, dim=-1)
                if self.psg_cls:
                    scores = outputs.rank_logits.squeeze(1)
                else:
                    scores = torch.tensor(1) - start_probs[:, 0] * end_probs[:, 0]

                outer = torch.matmul(start_probs.view(*start_probs.size(), 1),
                                     end_probs.view(end_probs.size()[0], 1, end_probs.size()[1]))
                outer_logits = torch.exp(logits_st.view(*logits_st.size(), 1) + logits_end.view(
                    logits_end.size()[0], 1, logits_end.size()[1]))

                context_max_len = torch.max(torch.sum(b_input_type_ids, dim=1)).to(torch.int64)

                max_ans_length = torch.min(torch.tensor(20).to(self.device), context_max_len).to(torch.int64).item()

                outer = torch.triu(outer, diagonal=0) - torch.triu(outer, diagonal=outer.size()[1] - max_ans_length)
                outer_logits = torch.triu(outer_logits, diagonal=0) - torch.triu(
                    outer_logits, diagonal=outer_logits.size()[1] - max_ans_length)

                start_pred = torch.argmax(torch.max(outer, dim=2)[0], dim=1)
                end_pred = torch.argmax(torch.max(outer, dim=1)[0], dim=1)
                logits = torch.max(torch.max(outer_logits, dim=2)[0], dim=1)[0]

            # Move logits and labels to CPU and to numpy arrays
            start_pred = start_pred.detach().cpu().numpy()
            end_pred = end_pred.detach().cpu().numpy()
            logits = logits.detach().cpu().numpy().tolist()
            scores = scores.detach().cpu().numpy().tolist()

            for j, (start_pred_elem, end_pred_elem, logits_elem, scores_elem) in \
                    enumerate(zip(start_pred, end_pred, logits, scores)):
                ind = indices[i * self.batch_size + j]
                if ind in predictions:
                    predictions[ind] += [(start_pred_elem, end_pred_elem, logits_elem, scores_elem)]
                else:
                    predictions[ind] = [(start_pred_elem, end_pred_elem, logits_elem, scores_elem)]

        start_pred_batch, end_pred_batch, logits_batch, scores_batch, ind_batch = [], [], [], [], []
        for ind in sorted(predictions.keys()):
            prediction = predictions[ind]
            max_ind = np.argmax([pred[2] for pred in prediction])
            start_pred_batch.append(prediction[max_ind][0])
            end_pred_batch.append(prediction[max_ind][1])
            logits_batch.append(prediction[max_ind][2])
            scores_batch.append(prediction[max_ind][3])
            ind_batch.append(max_ind)

        return start_pred_batch, end_pred_batch, logits_batch, scores_batch, ind_batch
