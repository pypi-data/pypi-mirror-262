from dataclasses import dataclass
import numpy as np
from pms_trt._utils import memcpy_host_to_device, memcpy_device_to_host


@dataclass
class TRTIOBinding:
    index: int
    name: str
    device_pointer: int
    host_array: np.ndarray

    def upload(self):
        memcpy_host_to_device(
            self.device_pointer,
            self.host_array,
        )

    def download(self):
        memcpy_device_to_host(
            self.host_array,
            self.device_pointer,
        )
