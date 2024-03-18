from typing import List, Union

from classiq.interface.model.bind_operation import BindOperation
from classiq.interface.model.inplace_binary_operation import InplaceBinaryOperation
from classiq.interface.model.quantum_expressions.amplitude_loading_operation import (
    AmplitudeLoadingOperation,
)
from classiq.interface.model.quantum_expressions.arithmetic_operation import (
    ArithmeticOperation,
)
from classiq.interface.model.quantum_function_call import QuantumFunctionCall
from classiq.interface.model.quantum_if_operation import QuantumIfOperation
from classiq.interface.model.quantum_lambda_function import QuantumLambdaFunction
from classiq.interface.model.variable_declaration_statement import (
    VariableDeclarationStatement,
)
from classiq.interface.model.within_apply_operation import WithinApplyOperation

ConcreteQuantumStatement = Union[
    QuantumFunctionCall,
    ArithmeticOperation,
    AmplitudeLoadingOperation,
    VariableDeclarationStatement,
    BindOperation,
    InplaceBinaryOperation,
    QuantumIfOperation,
    WithinApplyOperation,
]

StatementBlock = List[ConcreteQuantumStatement]

QuantumLambdaFunction.update_forward_refs(StatementBlock=StatementBlock)
