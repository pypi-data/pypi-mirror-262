# Copyright 2023 Ant Group Co., Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


""" Async split learning strategy

"""
import copy
from typing import List, Union

import torch

from secretflow.ml.nn.sl.backend.torch.sl_base import SLBaseTorchModel
from secretflow.ml.nn.sl.strategy_dispatcher import register_strategy
from secretflow.utils.communicate import ForwardData


class SLTorchModel(SLBaseTorchModel):
    def base_forward(self, stage: str = 'train', **kwargs):
        """compute hidden embedding
        Args:
            stage: Which stage of the base forward
        Returns: hidden embedding
        """
        if not self.model_base:
            return None
        self._h = self.base_forward_internal(
            self._data_x,
        )

    def base_backward(self):
        """backward on fusenet

        Args:
            self.gradient: gradient of fusenet hidden layer
        """

        return_hiddens = []
        if len(self._gradient) == len(self._h):
            for i in range(len(self._gradient)):
                grad = (
                    self._gradient[i]
                    if isinstance(self._gradient[i], torch.Tensor)
                    else torch.tensor(self._gradient[i])
                )
                return_hiddens.append(self.fuse_op.apply(self._h[i], grad))
        else:
            self._gradient = (
                self._gradient[0]
                if isinstance(self._gradient[0], torch.Tensor)
                else torch.tensor(self._gradient[0])
            )
            return_hiddens.append(self.fuse_op.apply(self._h, self._gradient))

        # apply gradients for base net
        self.optim_base.zero_grad()
        for rh in return_hiddens:
            if rh.requires_grad:
                rh.sum().backward(retain_graph=True)
        self.optim_base.step()

        # clear intermediate results
        self._h = None
        self.kwargs = {}

    def fuse_net(
        self,
        forward_data: Union[List[ForwardData], ForwardData],
        _num_returns=2,
    ):
        """Fuses the hidden layer and calculates the reverse gradient
        only on the side with the label

        Args:
            forward_data: A list of hidden layers for each party to compute.
            _num_returns: the return nums.
        Returns:
            gradient Of hiddens
        """
        assert (
            self.model_fuse is not None
        ), "Fuse model cannot be none, please give model define"

        if isinstance(forward_data, ForwardData):
            forward_data = [forward_data]
        forward_data[:] = (h for h in forward_data if h is not None)

        for i, h in enumerate(forward_data):
            assert h.hidden is not None, f"hidden cannot be found in forward_data[{i}]"
            if isinstance(h.losses, List) and h.losses[0] is None:
                h.losses = None

        hiddens = []
        for fd in forward_data:
            h = fd.hidden
            # h will be list, if basenet is multi output
            if isinstance(h, List):
                for i in range(len(h)):
                    hiddens.append(h[i])
            else:
                hiddens.append(h)
        hiddens = self.to_exec_device(hiddens)
        train_y = self.train_y[0] if len(self.train_y) == 1 else self.train_y

        logs = {}

        gradient = self.fuse_net_internal(
            hiddens,
            train_y,
            self.train_sample_weight,
            logs,
        )
        for m in self.metrics_fuse:
            logs['train_' + m.__class__.__name__] = m.compute().cpu().numpy()
        self.logs = copy.deepcopy(logs)
        return gradient


@register_strategy(strategy_name='split_nn', backend='torch')
class PYUSLTorchModel(SLTorchModel):
    pass
