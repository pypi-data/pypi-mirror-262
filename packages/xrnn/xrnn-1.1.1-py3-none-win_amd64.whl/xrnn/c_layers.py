"""This module loads the shared library that contain function definitions for convolution and pooling that are written
in C and compiled into a shared library for performance reasons and makes these functions callable from Python."""
import ctypes
import os
import platform
from typing import Union, Optional, Any, Callable

from xrnn import ops


def make_argtypes_list(
        dtype: Union[type, str, ops.dtype],
        ndim: Optional[int] = None,
        shape: Optional[Union[int, tuple, list, ops.ndarray]] = None,
        flags: Optional[Union[str, tuple]] = None,
        npointers: int = 1,
        numeral_type=ctypes.c_size_t,
        n_numerals: int = 1,
        takes_bool: bool = True) -> list:
    """
    Returns a list containing all the argument types for the inputs to C function

    Parameters
    ----------
    dtype: type, str, dtype instance
        The data type of the array that the C functions take.
    ndim: int, optional
        The number of dimensions the array should be expected to have.
    shape: tuple, optional
        The shape the array is expected to have.
    flags: str, list, optional
        Any flags the array is expected to have. For example the 'C' flags checks if the array is C contagious.
    npointers: int, optional
        The number of array pointers to create with the above checks/restrictions. For example if the C function expects
        4 arrays as inputs, set this to 4.
    numeral_type: int
        The data type that the C function expects the inputs to be in.
    n_numerals: int, optional
        How many numerical arguments does the C function expect.
    takes_bool: bool, optional
        Whether the C function takes a bool value as its last argument.

    Returns
    -------
    argtypes:
        A list containing all the arguments' types
    """

    argtypes = []
    for _ in range(npointers):
        argtypes.append(ops.ctypeslib.ndpointer(dtype=dtype, ndim=ndim, shape=shape, flags=flags))
    for _ in range(n_numerals):
        argtypes.append(numeral_type)
    if takes_bool:
        argtypes.append(ctypes.c_bool)
    return argtypes


def make_callable(function: Callable, argtypes: list, restype: Optional[Union[list, Any]] = None) -> None:
    """Supplies the C function with the parameters data types and return type to make it callable from python and
    enable type checking."""
    function.argtypes = argtypes
    function.restype = restype


operating_system = platform.system()
if operating_system == 'Windows':
    SHARED_LIB_FILE_EXTENSION = '.dll'
elif operating_system in ('Linux', 'Darwin'):
    SHARED_LIB_FILE_EXTENSION = '.so'
else:
    raise OSError(
        f"Supported OSes are Windows, Linux and MacOS. Got {operating_system}")

SHARED_LIB_PATH = os.path.join(os.path.dirname(__file__), 'lib', 'c_layers' + SHARED_LIB_FILE_EXTENSION)
if not os.path.exists(SHARED_LIB_PATH):
    raise FileNotFoundError(
        "The compiled shared/dynamic library doesn't exist, you are probably running source distribution code. "
        "To build the package run `python -m build` and install the wheel using `pip install "
        "dist/xrnn-REST-OF-THE-NAME.whl`. If you've already done this, you might be running your commands from the"
        "source distribution directory, and Python will import that code instead of the installed one.")

# Use windll.LoadLibrary on Windows instead of CDLL because it uses stdcall.
# That's useful when passing too many arguments to a C function because it raises a TypeError, making it harder to
# pass the wrong number of arguments to the C functions. Using CDLL on Windows would allow passing too many arguments.
# However, that's not the case for Linux and macOS.
if operating_system == 'Windows':
    functions_cdll = ctypes.windll.LoadLibrary(SHARED_LIB_PATH)
else:
    functions_cdll = ctypes.CDLL(SHARED_LIB_PATH)

# Python caches the imported module so the following module level code will only be executed once, therefor the shared
# library is only loaded once.

# Convolution forward operation that takes float inputs.
convForwardF = functions_cdll.convForwardF
make_callable(convForwardF, make_argtypes_list('float32', npointers=4, n_numerals=11))
# Convolution forward operation that takes double inputs.
convForwardD = functions_cdll.convForwardD
make_callable(convForwardD, make_argtypes_list('float64', npointers=4, n_numerals=11))

convBackwardF = functions_cdll.convBackwardF
make_callable(convBackwardF, make_argtypes_list('float32', npointers=5, n_numerals=11))
convBackwardD = functions_cdll.convBackwardD
make_callable(convBackwardD, make_argtypes_list('float64', npointers=5, n_numerals=11))

maxPoolForwardF = functions_cdll.maxPoolForwardF
make_callable(maxPoolForwardF, make_argtypes_list('float32', npointers=3, n_numerals=10))
maxPoolForwardD = functions_cdll.maxPoolForwardD
make_callable(maxPoolForwardD, make_argtypes_list('float64', npointers=3, n_numerals=10))

maxPoolBackwardF = functions_cdll.maxPoolBackwardF
make_callable(maxPoolBackwardF, make_argtypes_list('float32', npointers=3, n_numerals=10))
maxPoolBackwardD = functions_cdll.maxPoolBackwardD
make_callable(maxPoolBackwardD, make_argtypes_list('float64', npointers=3, n_numerals=10))

avgPoolForwardF = functions_cdll.avgPoolForwardF
make_callable(avgPoolForwardF, make_argtypes_list('float32', npointers=2, n_numerals=10))
avgPoolForwardD = functions_cdll.avgPoolForwardD
make_callable(avgPoolForwardD, make_argtypes_list('float64', npointers=2, n_numerals=10))

avgPoolBackwardF = functions_cdll.avgPoolBackwardF
make_callable(avgPoolBackwardF, make_argtypes_list('float32', npointers=2, n_numerals=10))
avgPoolBackwardD = functions_cdll.avgPoolBackwardD
make_callable(avgPoolBackwardD, make_argtypes_list('float64', npointers=2, n_numerals=10))
