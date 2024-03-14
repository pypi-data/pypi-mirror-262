__TARGET_TRT_VERSION = "8.6.1"
try:
    import tensorrt as __trt

    assert (
        __trt.__version__ == __TARGET_TRT_VERSION
    ), f"ERROR, TensorRT version is mismatch. Current version is {__trt.__version__}. But, the library need tensorrt=={__TARGET_TRT_VERSION}"
    from ._logger import LoguruTRTLogger
    from ._session import TRTSession
    from ._io_binding import TRTIOBinding
    from ._utils import get_device_count, get_device_list, batch
    from ._patcher import Patcher, pad_vector
except Exception as ex:
    from loguru import logger

    logger.critical(
        f"You CAN NOT import this package. Exception = {ex}\nNote: Since tensorrt does not support pep517, this package will not automatically install tensorrt."
    )

__version__ = "0.1.1"
