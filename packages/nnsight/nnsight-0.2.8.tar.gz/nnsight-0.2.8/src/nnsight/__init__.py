from functools import wraps
import os

import yaml
import torch
from .patching import *
from .pydantics.Config import ConfigModel

PATH = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(PATH, "config.yaml"), "r") as file:
    CONFIG = ConfigModel(**yaml.safe_load(file))

from .logger import logger
from .models.NNsightModel import NNsight
from .models.LanguageModel import LanguageModel

from .patching import Patch, Patcher
from .tracing.Proxy import proxy_wrapper

logger.disabled = not CONFIG.APP.LOGGING

# Below do default patching:
DEFAULT_PATCHER = Patcher()

from inspect import getmembers, isfunction

import einops

for key, value in getmembers(einops.einops, isfunction):
    DEFAULT_PATCHER.add(Patch(einops.einops, proxy_wrapper(value), key))


from torch._subclasses.fake_tensor import FakeTensor


def _bool(self):
    return True


DEFAULT_PATCHER.add(Patch(FakeTensor, _bool, "__bool__"))


def fake_tensor_new_wrapper(fn):

    @wraps(fn)
    def inner(cls, fake_mode, elem, device, constant=None):

        if isinstance(elem, FakeTensor):

            return elem

        else:

            return fn(cls, fake_mode, elem, device, constant=constant)

    return inner


DEFAULT_PATCHER.add(
    Patch(FakeTensor, fake_tensor_new_wrapper(FakeTensor.__new__), "__new__")
)


def onehot_wrapper(fn):
    @wraps(fn)
    def onehot(input: torch.Tensor, num_classes=-1):
        if input.device.type == "meta":
            return torch.zeros((*input.shape, num_classes), device="meta")

        else:
            return fn(input, num_classes=num_classes)

    return onehot


DEFAULT_PATCHER.add(
    Patch(torch.nn.functional, onehot_wrapper(torch.nn.functional.one_hot), "one_hot")
)

def noop_wrapper(fn):
    @wraps(fn)
    def noop(input: torch.Tensor, *args, **kwargs):
        return input

    return noop

DEFAULT_PATCHER.add(Patch(FakeTensor, noop_wrapper(FakeTensor.tolist), "tolist"))

DEFAULT_PATCHER.__enter__()
