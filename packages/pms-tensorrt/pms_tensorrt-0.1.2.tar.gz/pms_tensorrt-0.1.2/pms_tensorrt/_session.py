import asyncio
import os
import subprocess
from typing import Any, Dict, List, Optional
import tensorrt as trt
from pms_tensorrt._logger import LoguruTRTLogger
from pms_tensorrt._io_binding import TRTIOBinding
from pms_tensorrt._utils import get_device_count, cuda_mem_alloc
import numpy as np
from loguru import logger


def _get_binding_idx_by_name(engine: Any, name: str) -> int:
    num_bindings: int = engine.num_bindings
    bindings: List[str] = [engine.get_binding_name(i) for i in range(num_bindings)]
    return bindings.index(name)


class TRTSession:
    def __init__(
        self,
        model_path: str,
        device_id: int,
        io_shapes: Dict[str, List[int]],
    ) -> None:
        self.model_path = model_path
        self.io_shapes = io_shapes
        self.device_id = device_id

        # check gpu
        device_count = get_device_count()
        assert device_count > 0, f"There is no device to use."

        # set env
        os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
        os.environ["CUDA_VISIBLE_DEVICES"] = f"{device_id}"

        # Create Logger
        self._logger = LoguruTRTLogger()

        # Load TRT engine
        with open(model_path, "rb") as f, trt.Runtime(self._logger) as runtime:  # type: ignore
            assert runtime
            self._engine = runtime.deserialize_cuda_engine(f.read())
        assert self._engine

        # Create exec context
        self._inference_context = self._engine.create_execution_context()
        assert self._inference_context

        self.input_bindings: List[TRTIOBinding] = []
        self.output_bindings: List[TRTIOBinding] = []
        self._pointers: List[int] = []
        for i in range(self._engine.num_bindings):
            name = self._engine.get_tensor_name(i)
            mode = self._engine.get_tensor_mode(
                name
            ).value  # 0: NONE, 1:INPUT, 2:OUTPUT
            is_input = mode == 1
            dtype = self._engine.get_tensor_dtype(name)
            org_shape = self._engine.get_tensor_shape(name)
            shape = self.io_shapes[name]
            size = np.dtype(trt.nptype(dtype)).itemsize
            for target_shape in shape:
                size *= target_shape
            pointer = cuda_mem_alloc(size)
            binding = TRTIOBinding(
                index=i,
                name=name,
                device_pointer=pointer,
                host_array=np.zeros(list(shape), np.dtype(trt.nptype(dtype))),
            )
            self._pointers.append(pointer)
            if is_input:
                self.input_bindings.append(binding)
                res = self._inference_context.set_input_shape(name=name, shape=shape)  # type: ignore
                assert (
                    res
                ), f"ERROR, 'set_shape_input' is failed with {name}. | binding_idx:{i} | org_shape:{org_shape} | target_shape:{shape}"
            else:
                self.output_bindings.append(binding)

        assert len(self.input_bindings) > 0
        assert len(self.output_bindings) > 0

    def upload(self):
        [binding.upload() for binding in self.input_bindings]

    def inference(self):
        self._inference_context.execute_v2(self._pointers)

    def download(self):
        [binding.download() for binding in self.output_bindings]

    def set_input(
        self,
        input_datas: List[np.ndarray],
    ):
        assert len(input_datas) == len(
            self.input_bindings
        ), f"ERROR, len(input_datas) != len(self.input_bindings)"
        for binding, input_data in zip(self.input_bindings, input_datas):
            assert (
                binding.host_array.shape == input_data.shape
            ), f"ERROR, binding.host_array.shape({binding.host_array.shape}) =! input_data.shape({input_data.shape})."
            np.copyto(
                dst=binding.host_array,
                src=input_data,
            )

    def get_output(
        self,
        output_datas: List[np.ndarray],
    ):
        assert len(output_datas) == len(
            self.output_bindings
        ), f"ERROR, len(output_datas) != len(self.output_bindings)"
        for binding, output_data in zip(self.output_bindings, output_datas):
            assert (
                binding.host_array.shape == output_data.shape
            ), f"ERROR, binding.host_array.shape({binding.host_array.shape}) =! output_data.shape({output_data.shape})."
            np.copyto(
                dst=output_data,
                src=binding.host_array,
            )

    def run(
        self,
        input_datas: Optional[List[np.ndarray]] = None,
        output_datas: Optional[List[np.ndarray]] = None,
    ) -> None:
        # Set input
        if input_datas is not None:
            self.set_input(input_datas=input_datas)

        # Host to Device
        self.upload()

        # Inference
        self.inference()

        # Device to Host
        self.download()

        # Get output
        if output_datas is not None:
            self.get_output(output_datas=output_datas)

    async def run_async(
        self,
        input_datas: Optional[List[np.ndarray]] = None,
        output_datas: Optional[List[np.ndarray]] = None,
    ) -> None:
        # upload & inference & download
        await asyncio.to_thread(
            self.run,
            input_datas=input_datas,
            output_datas=output_datas,
        )
