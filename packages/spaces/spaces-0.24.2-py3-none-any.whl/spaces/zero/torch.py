"""
"""
# pyright: reportPrivateImportUsage=false

from __future__ import annotations

import multiprocessing
import os
from concurrent.futures import ProcessPoolExecutor
from contextlib import suppress
from functools import partial
from types import SimpleNamespace
from typing import TYPE_CHECKING
from typing import Any
from typing import Tuple

from ..config import Config
from . import bitsandbytes
from .utils import maybe_import_torch

if TYPE_CHECKING:
    import torch as Torch


# Nvidia A100.80G MIG (drivers 535) / Torch 2.2.0
CUDA_DEVICE_NAME = 'NVIDIA A100-SXM4-80GB MIG 3g.40gb'
CUDA_TOTAL_MEMORY = 42144366592
CUDA_MEM_GET_INFO = (41911451648, CUDA_TOTAL_MEMORY)
CUDA_DEVICE_CAPABILITY = (8, 0)
CUDA_DEVICE_PROPERTIES = SimpleNamespace(name=CUDA_DEVICE_NAME, major=8, minor=0, total_memory=CUDA_TOTAL_MEMORY, multi_processor_count=42)

GENERIC_METHOD_NAMES = [
    'arange',
    'as_tensor',
    'asarray',
    'bartlett_window',
    'blackman_window',
    'empty',
    'empty_like',
    'empty_strided',
    'eye',
    'full',
    'full_like',
    'hamming_window',
    'hann_window',
    'kaiser_window',
    'linspace',
    'logspace',
    'obj',
    'ones',
    'ones_like',
    'rand',
    'rand_like',
    'randint',
    'randint_like',
    'randn',
    'randn_like',
    'randperm',
    'range',
    'sparse_bsc_tensor',
    'sparse_bsr_tensor',
    'sparse_compressed_tensor',
    'sparse_coo_tensor',
    'sparse_csc_tensor',
    'sparse_csr_tensor',
    'tensor',
    'tril_indices',
    'triu_indices',
    'zeros',
    'zeros_like',
]


if (torch := maybe_import_torch()):

    from torch.utils.weak import WeakTensorKeyDictionary

    # TODO: Tensor.cpu() must remove from to_ops

    _tensor_to         = torch.Tensor.to
    _tensor_cuda       = torch.Tensor.cuda
    _torch_generics    = {name: getattr(torch, name) for name in GENERIC_METHOD_NAMES}
    _cuda_init         = torch._C._cuda_init
    _cuda_available      = torch.cuda.is_available
    _cuda_device_count   = torch.cuda.device_count
    _cuda_current_device = torch.cuda.current_device
    _cuda_mem_get_info   = torch.cuda.mem_get_info
    _cuda_get_device_capability   = torch.cuda.get_device_capability
    _cuda_get_device_properties   = torch.cuda.get_device_properties
    _cuda_get_device_name         = torch.cuda.get_device_name

    TensorToArgs = Tuple[torch.device, torch.dtype, bool, torch.memory_format]

    to_ops: dict[Torch.Tensor, TensorToArgs | None] = WeakTensorKeyDictionary() # type: ignore

    @property
    def _tensor_device_property(self: Torch.Tensor):
        if self in to_ops:
            return torch.device(type='cuda', index=0)
        del torch.Tensor.device
        try:
            return self.device
        finally:
            torch.Tensor.device = _tensor_device_property # type: ignore

    def _to_op_register(self: Torch.Tensor, *args, **kwargs):
        parsed = torch._C._nn._parse_to(*args, **kwargs)
        device, *_ = parsed
        if not isinstance(device, torch.device):
            return _tensor_to(self, *args, **kwargs)
        if device.type != 'cuda':
            return _tensor_to(self, *args, **kwargs)
        to_ops[self] = parsed
        return self

    def _cuda_op_arg_check(device: Torch.device | int | str | None) -> bool:
        if device is None:
            return True
        if isinstance(device, int):
            return True
        if isinstance(device, str):
            device = torch.device(device)
        return device.type == 'cuda'

    def _cuda_op_register(self: Torch.Tensor, device: Torch.device | int | str | None = None, **kwargs):
        if not _cuda_op_arg_check(device):
            # Let PyTorch handle the fail
            return _tensor_cuda(self, device, **kwargs)
        to_ops[self] = None
        return self

    def _cuda_init_raise():
        raise RuntimeError(
            "CUDA must not be initialized in the main process "
            "on Spaces with Stateless GPU environment.\n"
            "You can look at this Stacktrace to find out "
            "which part of your code triggered a CUDA init"
        )

    def _generic_method_register(name: str, *args: Any, **kwargs: Any):
        try:
            device = torch.device(kwargs.get('device', "cpu"))
        except Exception:
            return _torch_generics[name](*args, **kwargs)
        if device.type != 'cuda':
            return _torch_generics[name](*args, **kwargs)
        tensor = _torch_generics[name](*args, **{**kwargs, 'device': "cpu"})
        to_ops[tensor] = None
        return tensor

    def _patch():
        torch.Tensor.to         = _to_op_register   # type: ignore
        torch.Tensor.cuda       = _cuda_op_register # type: ignore
        if Config.zero_patch_torch_device:
            torch.Tensor.device = _tensor_device_property # type: ignore
        for name in GENERIC_METHOD_NAMES:
            setattr(torch, name, partial(_generic_method_register, name))
        torch._C._cuda_init     = _cuda_init_raise
        torch.cuda.is_available   = lambda: True
        torch.cuda.device_count   = lambda: 1
        torch.cuda.current_device = lambda: 0
        torch.cuda.mem_get_info   = lambda *args, **kwargs: CUDA_MEM_GET_INFO
        torch.cuda.get_device_capability = lambda *args, **kwargs: CUDA_DEVICE_CAPABILITY
        torch.cuda.get_device_properties = lambda *args, **kwargs: CUDA_DEVICE_PROPERTIES
        torch.cuda.get_device_name       = lambda *args, **kwargs: CUDA_DEVICE_NAME
        bitsandbytes.patch()

    def _unpatch():
        torch.Tensor.to         = _tensor_to
        torch.Tensor.cuda       = _tensor_cuda
        with suppress(AttributeError):
            del torch.Tensor.device
        for name in GENERIC_METHOD_NAMES:
            setattr(torch, name, _torch_generics[name])
        torch._C._cuda_init     = _cuda_init
        torch.cuda.is_available   = _cuda_available
        torch.cuda.device_count   = _cuda_device_count
        torch.cuda.current_device = _cuda_current_device
        torch.cuda.mem_get_info   = _cuda_mem_get_info
        torch.cuda.get_device_capability = _cuda_get_device_capability
        torch.cuda.get_device_properties = _cuda_get_device_properties
        torch.cuda.get_device_name       = _cuda_get_device_name
        bitsandbytes.unpatch()

    def _move(nvidia_uuid: str):
        os.environ['CUDA_VISIBLE_DEVICES'] = nvidia_uuid
        torch.Tensor([0]).cuda() # CUDA init
        for op in to_ops.items():
            tensor, parsed_args = op
            if parsed_args:
                _, dtype, _, memory_format = parsed_args
            else:
                dtype, memory_format = None, None
            tensor.data = _tensor_to(tensor,
                device='cuda',
                dtype=dtype,
                memory_format=memory_format,
            ) # type: ignore
        bitsandbytes.move()
        torch.cuda.synchronize()

    def _is_in_bad_fork():
        with ProcessPoolExecutor(mp_context=multiprocessing.get_context('fork')) as e:
            f = e.submit(torch.cuda._is_in_bad_fork)
            return f.result()

    def _disable_cuda_intercept():
        torch.Tensor.to   = _tensor_to
        torch.Tensor.cuda = _tensor_cuda

else:

    _patch = lambda: None
    _unpatch = lambda: None
    _move = lambda nvidia_uuid: None
    _is_in_bad_fork = lambda: False
    _disable_cuda_intercept = lambda: None


patch = _patch
unpatch = _unpatch
move = _move
is_in_bad_fork = _is_in_bad_fork
disable_cuda_intercept = _disable_cuda_intercept
