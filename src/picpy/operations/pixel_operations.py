import numpy as np
from numpy.typing import NDArray
from typing import Tuple


def inverse(array: NDArray[np.float32]) -> NDArray[np.float32]:
    result = 1 - array
    return result


def brightness(array: NDArray[np.float32], beta: float) -> NDArray[np.float32]:
    result = array + beta
    return result


def contrast(array: NDArray[np.float32], gamma: float, beta: float) -> NDArray[np.float32]:
    result = array * gamma + beta
    return result


def logarithmic(array: NDArray[np.float32], c: float | np.float32) -> NDArray[np.float32]:
    c = np.float32(c)
    result = c * np.log1p(array)
    return result


def power(array: NDArray[np.float32], exp: float, c: float | np.float32) -> NDArray[np.float32]:
    c = np.float32(c)
    result = c * np.power(array, exp)
    return result


def exponential(array: NDArray[np.float32], c: float | np.float32) -> NDArray[np.float32]:
    c = np.float32(c)
    result = np.expm1(array/c)
    return result
