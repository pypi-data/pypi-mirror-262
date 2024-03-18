from typing import Any

from classiq.interface.generator.functions.classical_type import Bool, Integer
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.helpers.pydantic_model_helpers import nameables_to_dict
from classiq.interface.model.port_declaration import PortDeclaration
from classiq.interface.model.quantum_function_declaration import (
    QuantumFunctionDeclaration,
    QuantumOperandDeclaration,
)

REPEAT_OPERATOR = QuantumFunctionDeclaration(
    name="repeat",
    param_decls={"count": Integer()},
    operand_declarations={
        "iteration": QuantumOperandDeclaration(
            name="iteration", param_decls={"index": Integer()}
        )
    },
)


def _get_single_empty_operand_operator(
    operator_name: str, **kwargs: Any
) -> QuantumFunctionDeclaration:
    operand_field_name = "operand"
    return QuantumFunctionDeclaration(
        name=operator_name,
        operand_declarations={
            operand_field_name: QuantumOperandDeclaration(name=operand_field_name)
        },
        **kwargs,
    )


INVERT_OPERATOR = _get_single_empty_operand_operator(operator_name="invert")

_CTRL_FIELD_NAME = "ctrl"
CONTROL_OPERATOR = _get_single_empty_operand_operator(
    operator_name="control",
    port_declarations={
        _CTRL_FIELD_NAME: PortDeclaration(
            name=_CTRL_FIELD_NAME,
            direction=PortDeclarationDirection.Inout,
        )
    },
)

IF_OPERATOR = QuantumFunctionDeclaration(
    name="if",
    param_decls={"condition": Bool()},
    operand_declarations={
        "then": QuantumOperandDeclaration(name="then"),
        "else": QuantumOperandDeclaration(name="else"),
    },
)


PERMUTE_OPERATOR = QuantumFunctionDeclaration(
    name="permute",
    operand_declarations={
        "functions": QuantumOperandDeclaration(
            name="functions",
            is_list=True,
        )
    },
)

POWER_OPERATOR = _get_single_empty_operand_operator(
    operator_name="power", param_decls={"power": Integer()}
)

APPLY_OPERATOR = _get_single_empty_operand_operator(operator_name="apply")

COMPUTE = _get_single_empty_operand_operator(operator_name="compute")

UNCOMPUTE = _get_single_empty_operand_operator(operator_name="uncompute")

BUILTIN_QUANTUM_OPERATOR_LIST = [
    REPEAT_OPERATOR,
    INVERT_OPERATOR,
    CONTROL_OPERATOR,
    IF_OPERATOR,
    PERMUTE_OPERATOR,
    POWER_OPERATOR,
    APPLY_OPERATOR,
    COMPUTE,
    UNCOMPUTE,
]

QuantumFunctionDeclaration.BUILTIN_FUNCTION_DECLARATIONS.update(
    nameables_to_dict(BUILTIN_QUANTUM_OPERATOR_LIST)
)
