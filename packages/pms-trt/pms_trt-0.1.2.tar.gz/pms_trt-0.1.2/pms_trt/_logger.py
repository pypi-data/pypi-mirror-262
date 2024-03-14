from typing import Any
import tensorrt as trt
from loguru import logger


class LoguruTRTLogger(trt.ILogger):
    def __init__(self):
        trt.ILogger.__init__(self)

    def log(self, severity: Any, msg: str):
        if severity == trt.ILogger.INTERNAL_ERROR:
            # Represents an internal error. Execution is unrecoverable.
            logger.critical(msg)

        elif severity == trt.ILogger.ERROR:
            # Represents an application error.
            logger.error(msg)

        elif severity == trt.ILogger.WARNING:
            # Represents an application error that TensorRT has recovered from or fallen back to a default.
            logger.warning(msg)

        elif severity == trt.ILogger.INFO:
            # Represents informational messages.
            logger.info(msg)

        elif severity == trt.ILogger.VERBOSE:
            # Verbose messages with debugging information.
            logger.debug(msg)
        else:
            raise NotImplementedError(f"severity '{severity}' is not implemented.")
