from typing import List

from classiq.interface.generator.function_param_list import *  # noqa: F403
from classiq.interface.generator.function_param_list_without_self_reference import *  # noqa: F403
from classiq.interface.generator.oracles.oracle_function_param_list import *  # noqa: F403

from ..builtin_functions import (
    amplitude_loading,
    binary_ops,
    exponentiation,
    qpe,
    qsvm,
    range_types,
    state_preparation,
    suzuki_trotter,
)
from .standard_gates import *  # noqa: F403

__all__ = (
    [function.__name__ for function in function_param_library.param_list]  # noqa: F405
    + [
        function.__name__
        for function in standard_gate_function_param_library.param_list  # noqa: F405
    ]
    + [
        function.__name__
        for function in oracle_function_param_library.param_list  # noqa: F405
    ]
    + [
        "exponentiation",
        "state_preparation",
        "suzuki_trotter",
        "range_types",
        "binary_ops",
        "qpe",
        "amplitude_loading",
        "qsvm",
    ]
)


def __dir__() -> List[str]:
    return __all__
