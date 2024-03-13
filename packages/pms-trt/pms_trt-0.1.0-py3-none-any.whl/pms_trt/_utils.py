import subprocess
from typing import Any, Generator, Iterable, List, TypeVar
from cuda import cuda, cudart  # type: ignore
import numpy as np
import itertools

T = TypeVar("T")  # T 대신 다른 문자/단어를 써도 되지만 일반적으로 T를 사용합니다.


def check_cuda_err(err):
    if isinstance(err, cuda.CUresult):
        if err != cuda.CUresult.CUDA_SUCCESS:
            raise RuntimeError("Cuda Error: {}".format(err))
    if isinstance(err, cudart.cudaError_t):
        if err != cudart.cudaError_t.cudaSuccess:
            raise RuntimeError("Cuda Runtime Error: {}".format(err))
    else:
        raise RuntimeError("Unknown error type: {}".format(err))


def cuda_call(call):
    err, res = call[0], call[1:]
    check_cuda_err(err)
    if len(res) == 1:
        res = res[0]
    return res


def cuda_mem_alloc(size: int) -> int:
    return cuda_call(cudart.cudaMalloc(size))


# Wrapper for cudaMemcpy which infers copy size and does error checking
def memcpy_host_to_device(
    device_ptr: int,
    host_arr: np.ndarray,
):
    nbytes = host_arr.size * host_arr.itemsize
    cuda_call(
        cudart.cudaMemcpy(
            device_ptr,
            host_arr,
            nbytes,
            cudart.cudaMemcpyKind.cudaMemcpyHostToDevice,
        )
    )


# Wrapper for cudaMemcpy which infers copy size and does error checking
def memcpy_device_to_host(
    host_arr: np.ndarray,
    device_ptr: int,
):
    nbytes = host_arr.size * host_arr.itemsize
    cuda_call(
        cudart.cudaMemcpy(
            host_arr,
            device_ptr,
            nbytes,
            cudart.cudaMemcpyKind.cudaMemcpyDeviceToHost,
        )
    )


def get_device_list() -> List[str]:
    stdout = subprocess.check_output("nvidia-smi --list-gpus", shell=True)
    stdout_str = stdout.decode("utf-8")
    device_list = stdout_str.split("\n")[:-1]
    return device_list


def get_device_count() -> int:
    return len(get_device_list())


def batch(target_list: List[T], batch_size: int) -> Generator[List[T], None, None]:
    l = len(target_list)
    for ndx in range(0, l, batch_size):  # iterable 데이터를 배치 단위로 확인
        yield target_list[
            ndx : min(ndx + batch_size, l)
        ]  # batch 단위 만큼의 데이터를 반환
