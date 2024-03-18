from typing import TYPE_CHECKING

from classiq.interface.model.quantum_statement import QuantumOperation

if TYPE_CHECKING:
    from classiq.interface.model.quantum_lambda_function import QuantumOperand


class WithinApplyOperation(QuantumOperation):
    compute: "QuantumOperand"
    action: "QuantumOperand"
