from typing import Callable, List, Union

from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.model.bind_operation import BindOperation
from classiq.interface.model.inplace_binary_operation import (
    BinaryOperation,
    InplaceBinaryOperation,
)
from classiq.interface.model.quantum_function_call import ArgValue
from classiq.interface.model.quantum_function_declaration import (
    QuantumOperandDeclaration,
)
from classiq.interface.model.quantum_if_operation import QuantumIfOperation
from classiq.interface.model.within_apply_operation import WithinApplyOperation

from classiq.qmod.qmod_variable import Input, Output, QNum, QVar
from classiq.qmod.quantum_callable import QCallable
from classiq.qmod.quantum_expandable import prepare_arg
from classiq.qmod.symbolic_expr import SymbolicExpr


def bind(
    source: Union[Input[QVar], List[Input[QVar]]],
    destination: Union[Output[QVar], List[Output[QVar]]],
) -> None:
    assert QCallable.CURRENT_EXPANDABLE is not None
    if not isinstance(source, list):
        source = [source]
    if not isinstance(destination, list):
        destination = [destination]
    QCallable.CURRENT_EXPANDABLE.append_statement_to_body(
        BindOperation(
            in_handles=[src_var.get_handle_binding() for src_var in source],
            out_handles=[dst_var.get_handle_binding() for dst_var in destination],
        )
    )


def quantum_if(
    condition: SymbolicExpr, then: Union[QCallable, Callable[[], None]]
) -> None:
    assert QCallable.CURRENT_EXPANDABLE is not None
    QCallable.CURRENT_EXPANDABLE.append_statement_to_body(
        QuantumIfOperation(
            expression=Expression(expr=str(condition)),
            then=_to_operand(then),
        )
    )


def inplace_add(
    value: QNum,
    target: QNum,
) -> None:
    assert QCallable.CURRENT_EXPANDABLE is not None
    QCallable.CURRENT_EXPANDABLE.append_statement_to_body(
        InplaceBinaryOperation(
            target=target.get_handle_binding(),
            value=value.get_handle_binding(),
            operation=BinaryOperation.Addition,
        )
    )


def inplace_xor(
    value: QNum,
    target: QNum,
) -> None:
    assert QCallable.CURRENT_EXPANDABLE is not None
    QCallable.CURRENT_EXPANDABLE.append_statement_to_body(
        InplaceBinaryOperation(
            target=target.get_handle_binding(),
            value=value.get_handle_binding(),
            operation=BinaryOperation.Xor,
        )
    )


def within_apply(
    compute: Callable[[], None],
    action: Callable[[], None],
) -> None:
    assert QCallable.CURRENT_EXPANDABLE is not None
    QCallable.CURRENT_EXPANDABLE.append_statement_to_body(
        WithinApplyOperation(
            compute=_to_operand(compute),
            action=_to_operand(action),
        )
    )


def _to_operand(callable_: Union[QCallable, Callable[[], None]]) -> ArgValue:
    return prepare_arg(QuantumOperandDeclaration(name=""), callable_)


__all__ = [
    "bind",
    "quantum_if",
    "inplace_add",
    "inplace_xor",
    "within_apply",
]


def __dir__() -> List[str]:
    return __all__
