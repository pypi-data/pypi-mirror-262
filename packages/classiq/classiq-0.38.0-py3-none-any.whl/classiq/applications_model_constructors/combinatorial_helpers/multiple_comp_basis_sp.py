from classiq.interface.generator.function_params import DEFAULT_OUTPUT_NAME
from classiq.interface.generator.functions import SynthesisNativeFunctionDefinition
from classiq.interface.generator.state_preparation import (
    ComputationalBasisStatePreparation,
)

from classiq import FunctionGenerator, QReg

BinaryStr = str
Name = str


def multiple_comp_basis_sp(
    function_name: str, states: dict[Name, BinaryStr], call_name_frmt: str = "{}"
) -> SynthesisNativeFunctionDefinition:
    generator = FunctionGenerator(function_name=function_name)
    qregs_dict = {
        var_name: QReg[len(state)]  # type:ignore[misc]
        for var_name, state in states.items()
    }
    qregs = generator.create_inputs(qregs_dict)

    for var_name, state in states.items():
        params = ComputationalBasisStatePreparation(computational_state=state)
        qregs[var_name] = generator.ComputationalBasisStatePreparation(
            params,
            in_wires=qregs[var_name],
            strict_zero_ios=False,
            call_name=call_name_frmt.format(var_name),
        )[DEFAULT_OUTPUT_NAME]

    generator.set_outputs(qregs)

    return generator.to_function_definition()
