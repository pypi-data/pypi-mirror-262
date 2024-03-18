import abc
import collections.abc
import functools
from typing import (
    Any,
    Callable,
    Collection,
    Dict,
    Iterable,
    List,
    Mapping,
    Optional,
    Tuple,
    Union,
    cast,
)

from classiq.interface.generator import function_param_list, function_params
from classiq.interface.generator.control_state import ControlState
from classiq.interface.generator.function_params import IOName, PortDirection
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
    SynthesisPortDeclaration,
)
from classiq.interface.generator.identity import Identity
from classiq.interface.generator.quantum_function_call import (
    SynthesisQuantumFunctionCall,
    WireDict,
)
from classiq.interface.generator.slice_parsing_utils import parse_io_slicing
from classiq.interface.generator.user_defined_function_params import CustomFunction

from classiq.exceptions import ClassiqValueError, ClassiqWiringError
from classiq.model import logic_flow_change_handler
from classiq.model.logic_flow import LogicFlowBuilder
from classiq.quantum_functions.function_library import (
    FunctionLibrary,
    QuantumFunction,
    SynthesisQuantumFunctionDeclaration,
)
from classiq.quantum_register import QReg, QRegGenericAlias

SupportedInputArgs = Union[
    Mapping[IOName, QReg],
    Collection[QReg],
    QReg,
]

_SAME_INPUT_NAME_ERROR_MSG: str = "Cannot create multiple inputs with the same name"
_INPUT_AS_OUTPUT_ERROR_MSG: str = "Can't connect input directly to output"
ILLEGAL_INPUT_OR_SLICING_ERROR_MSG: str = "is not a valid input name/slice"
ILLEGAL_OUTPUT_ERROR_MSG: str = "Illegal output provided"

ASSIGNED = "_assigned_"


def _get_identity_call_name(name: str, io: PortDirection) -> str:
    return f"{name}_{io.value}_Identity"


class FunctionHandler(abc.ABC):
    def __init__(self) -> None:
        self._function_library: Optional[FunctionLibrary] = None
        self._port_declarations: Dict[IOName, SynthesisPortDeclaration] = dict()
        self._external_port_wiring: Dict[PortDirection, WireDict] = {
            PortDirection.Input: dict(),
            PortDirection.Output: dict(),
        }
        self._generated_qregs: Dict[IOName, QReg] = dict()
        self._logic_flow_builder: LogicFlowBuilder = LogicFlowBuilder()

    @property
    def input_wires(self) -> WireDict:
        return self._external_port_wiring[PortDirection.Input]

    @property
    def output_wires(self) -> WireDict:
        return self._external_port_wiring[PortDirection.Output]

    def _verify_unique_inputs(self, input_names: Iterable[IOName]) -> None:
        input_port_declarations = {
            name: port_declaration
            for name, port_declaration in self._port_declarations.items()
            if port_declaration.direction.is_input
        }
        if not input_port_declarations.keys().isdisjoint(input_names):
            raise ClassiqWiringError(_SAME_INPUT_NAME_ERROR_MSG)

    def _verify_no_inputs_as_outputs(self, output_qregs: Iterable[QReg]) -> None:
        for qreg in output_qregs:
            if any(
                qreg.isoverlapping(gen_qreg)
                for gen_qreg in self._generated_qregs.values()
            ):
                raise ClassiqWiringError(f"{_INPUT_AS_OUTPUT_ERROR_MSG} {qreg}")

    @staticmethod
    def _parse_control_states(
        control_states: Optional[Union[ControlState, Iterable[ControlState]]] = None
    ) -> List[ControlState]:
        if control_states is None:
            return list()
        elif isinstance(control_states, ControlState):
            return [control_states]
        return list(control_states)

    def create_inputs(
        self,
        inputs: Mapping[IOName, QRegGenericAlias],
    ) -> Dict[IOName, QReg]:
        self._verify_unique_inputs(inputs.keys())
        qregs_dict = {
            name: self._create_input_with_identity(name, qreg_type)
            for name, qreg_type in inputs.items()
        }
        self._generated_qregs.update(qregs_dict)
        return qregs_dict

    def _create_input_with_identity(
        self, name: IOName, qreg_type: QRegGenericAlias
    ) -> QReg:
        qreg = qreg_type()
        self._handle_io_with_identity(PortDirection.Input, name, qreg)
        return qreg

    def set_outputs(self, outputs: Mapping[IOName, QReg]) -> None:
        for name, qreg in outputs.items():
            self._set_output_with_identity(name, qreg)

    def _set_output_with_identity(self, name: IOName, qreg: QReg) -> None:
        self._handle_io_with_identity(PortDirection.Output, name, qreg)

    def _handle_io_with_identity(
        self, port_direction: PortDirection, name: IOName, qreg: QReg
    ) -> None:
        # We need to add an Identity call on each input/output of the logic flow,
        # since function input/output pins don't support "pin slicing".
        # (Which means we cannot use QRegs in the wiring directly - because it gets
        # decomposed into 1 bit wirings).
        # Adding the identity also indirectly adds support for slicing on IOs
        # (via the QReg slicing).
        rui = qreg.to_register_user_input(name)
        identity_call = SynthesisQuantumFunctionCall(
            name=_get_identity_call_name(name, port_direction),
            function_params=Identity(arguments=[rui]),
        )
        self._body.append(identity_call)
        wire_name = logic_flow_change_handler.handle_io_connection(
            port_direction, identity_call, name
        )
        if port_direction == PortDirection.Input:
            self._logic_flow_builder.connect_func_call_to_qreg(
                identity_call, name, qreg
            )
        else:
            self._logic_flow_builder.connect_qreg_to_func_call(
                qreg, name, identity_call
            )
        declaration_direction = PortDeclarationDirection.from_port_direction(
            port_direction
        )
        if (
            name in self._port_declarations
            and self._port_declarations[name].direction != declaration_direction
        ):
            declaration_direction = PortDeclarationDirection.Inout
        self._port_declarations[name] = SynthesisPortDeclaration(
            name=name,
            size=rui.size,
            direction=declaration_direction,
        )
        external_port_wiring_dict = dict(self._external_port_wiring[port_direction])
        external_port_wiring_dict[name] = wire_name
        self._external_port_wiring[port_direction] = external_port_wiring_dict

    def apply(
        self,
        function_name: Union[
            str,
            SynthesisQuantumFunctionDeclaration,
            QuantumFunction,
        ],
        in_wires: Optional[SupportedInputArgs] = None,
        out_wires: Optional[SupportedInputArgs] = None,
        is_inverse: bool = False,
        strict_zero_ios: bool = True,
        release_by_inverse: bool = False,
        control_states: Optional[Union[ControlState, Iterable[ControlState]]] = None,
        should_control: bool = True,
        power: int = 1,
        call_name: Optional[str] = None,
    ) -> Dict[IOName, QReg]:
        # if there's no function library, create one
        if self._function_library is None:
            self.create_library()

        if isinstance(function_name, SynthesisQuantumFunctionDeclaration):
            function_data = function_name
        elif isinstance(function_name, QuantumFunction):
            function_data = function_name.function_data
        else:
            function_data = None

        if function_data:
            if function_data.name not in self._function_library.function_dict:  # type: ignore[union-attr]
                self._function_library.add_function(function_data)  # type: ignore[union-attr]

            function_name = function_data.name

        function_name = cast(str, function_name)
        return self._add_function_call(
            function_name,
            self._function_library.get_function(function_name),  # type: ignore[union-attr]
            in_wires=in_wires,
            out_wires=out_wires,
            is_inverse=is_inverse,
            strict_zero_ios=strict_zero_ios,
            release_by_inverse=release_by_inverse,
            control_states=control_states,
            should_control=should_control,
            power=power,
            call_name=call_name,
        )

    def release_qregs(self, qregs: Union[QReg, Collection[QReg]]) -> None:
        if isinstance(qregs, QReg):
            qregs = [qregs]
        for qreg in qregs:
            self._logic_flow_builder.connect_qreg_to_zero(qreg)

    def _add_function_call(
        self,
        function: str,
        params: function_params.FunctionParams,
        control_states: Optional[Union[ControlState, Iterable[ControlState]]] = None,
        in_wires: Optional[SupportedInputArgs] = None,
        out_wires: Optional[SupportedInputArgs] = None,
        is_inverse: bool = False,
        release_by_inverse: bool = False,
        should_control: bool = True,
        power: int = 1,
        call_name: Optional[str] = None,
        strict_zero_ios: bool = True,
    ) -> Dict[IOName, QReg]:
        if function != type(params).__name__ and not isinstance(params, CustomFunction):
            raise ClassiqValueError(
                "The FunctionParams type does not match function name"
            )

        if (
            isinstance(params, CustomFunction)
            and self._function_library
            and function not in self._function_library.function_dict
        ):
            raise ClassiqValueError(
                "QuantumFunctionCall: The function is not found in included library."
            )

        call = SynthesisQuantumFunctionCall(
            function=function,
            function_params=params,
            is_inverse=is_inverse,
            release_by_inverse=release_by_inverse,
            strict_zero_ios=strict_zero_ios,
            control_states=self._parse_control_states(control_states),
            should_control=should_control,
            power=power,
            name=call_name,
        )

        if in_wires is not None:
            self._connect_in_qregs(call=call, in_wires=in_wires)

        self._body.append(call)

        return self._connect_out_qregs(call=call, out_wires=out_wires or {})

    def _connect_in_qregs(
        self,
        call: SynthesisQuantumFunctionCall,
        in_wires: SupportedInputArgs,
    ) -> None:
        if isinstance(in_wires, dict):
            self._connect_named_in_qregs(call=call, in_wires=in_wires)
        elif isinstance(in_wires, QReg):
            self._connect_unnamed_in_qregs(call=call, in_wires=[in_wires])
        elif isinstance(in_wires, collections.abc.Collection):
            self._connect_unnamed_in_qregs(
                # mypy doesn't recognize that `dict` wouldn't reach this point
                call=call,
                in_wires=in_wires,  # type: ignore[arg-type]
            )
        else:
            raise ClassiqWiringError(
                f"Invalid in_wires type: {type(in_wires).__name__}"
            )

    def _connect_unnamed_in_qregs(
        self,
        call: SynthesisQuantumFunctionCall,
        in_wires: Collection[QReg],
    ) -> None:
        call_inputs = call.function_params.inputs_full(call.strict_zero_ios).keys()
        self._connect_named_in_qregs(call, dict(zip(call_inputs, in_wires)))

    def _connect_named_in_qregs(
        self,
        call: SynthesisQuantumFunctionCall,
        in_wires: Dict[IOName, QReg],
    ) -> None:
        for input_name, in_qreg in in_wires.items():
            pin_name, pin_indices = self._get_pin_name_and_indices(input_name, call)
            if len(in_qreg) != len(pin_indices):
                raise ClassiqWiringError(
                    f"Incorrect size of input QReg: expected {len(pin_indices)}, actual {len(in_qreg)}"
                )
            self._logic_flow_builder.connect_qreg_to_func_call(
                in_qreg, pin_name, call, pin_indices
            )

    @staticmethod
    def _get_pin_name_and_indices(
        input_name: IOName,
        call: SynthesisQuantumFunctionCall,
    ) -> Tuple[IOName, range]:
        try:
            name, slicing = parse_io_slicing(input_name)
        except (AssertionError, ValueError) as e:
            raise ClassiqWiringError(
                f"{input_name} {ILLEGAL_INPUT_OR_SLICING_ERROR_MSG}"
            ) from e
        pin_info = call.input_regs_dict.get(name)
        if pin_info is None:
            raise ClassiqWiringError(
                f"No register size information on input pin {name}"
            )
        indices = range(pin_info.size)[slicing]
        return name, indices

    def _connect_out_qregs(
        self,
        call: SynthesisQuantumFunctionCall,
        out_wires: SupportedInputArgs,
    ) -> Dict[IOName, QReg]:
        if isinstance(out_wires, dict):
            return self._connect_named_out_qregs(call, out_wires)
        elif isinstance(out_wires, QReg):
            return self._connect_unnamed_out_qregs(call, [out_wires])
        elif isinstance(out_wires, collections.abc.Collection):
            return self._connect_unnamed_out_qregs(
                # mypy doesn't recognize that `dict` wouldn't reach this point
                call,
                out_wires,  # type: ignore[arg-type]
            )
        else:
            raise ClassiqWiringError(
                f"Invalid in_wires type: {type(out_wires).__name__}"
            )

    def _connect_unnamed_out_qregs(
        self,
        call: SynthesisQuantumFunctionCall,
        out_wires: Collection[QReg],
    ) -> Dict[IOName, QReg]:
        call_outputs = call.function_params.outputs.keys()
        return self._connect_named_out_qregs(call, dict(zip(call_outputs, out_wires)))

    def _connect_named_out_qregs(
        self,
        call: SynthesisQuantumFunctionCall,
        out_wires: Mapping[IOName, QReg],
    ) -> Dict[IOName, QReg]:
        if not all(output_name in call.output_regs_dict for output_name in out_wires):
            raise ClassiqWiringError(ILLEGAL_OUTPUT_ERROR_MSG)
        output_dict = {}
        for output_name, reg_user_input in call.output_regs_dict.items():
            if reg_user_input is None:
                raise ClassiqValueError(
                    f"No output register information for {output_name}"
                )
            qreg = out_wires.get(output_name) or QReg.from_arithmetic_info(
                reg_user_input
            )
            self._logic_flow_builder.connect_func_call_to_qreg(call, output_name, qreg)
            output_dict[output_name] = qreg
        return output_dict

    def __getattr__(self, item: str) -> Callable[..., Any]:
        # This is added due to problematic behaviour in deepcopy.
        # deepcopy approaches __getattr__ before __init__ is called,
        # and therefore self._function_library doesn't exist.
        # Thus, we treat _function_library differently.

        if item == "_function_library":
            raise AttributeError(
                f"{self.__class__.__name__!r} has no attribute {item!r}"
            )

        is_builtin_function_name = any(
            item == func.__name__
            for func in function_param_list.function_param_library.param_list
        )

        if is_builtin_function_name:
            return functools.partial(self._add_function_call, item)

        is_user_function_name = (
            self._function_library is not None
            and item in self._function_library.function_names
        )

        if is_user_function_name:
            return functools.partial(self.apply, item)

        if (
            self._function_library is not None
            and item in self._function_library.function_factory_names
        ):
            return functools.partial(
                self._function_library.get_function_factory(item),
                add_method=functools.partial(
                    self._function_library.add_function,
                    override_existing_functions=True,
                ),
                apply_method=self.apply,
            )

        raise AttributeError(f"{self.__class__.__name__!r} has no attribute {item!r}")

    def __dir__(self) -> List[str]:
        builtin_func_name = [
            func.__name__
            for func in function_param_list.function_param_library.param_list
        ]
        user_func_names = (
            list(self._function_library.function_names)
            if self._function_library is not None
            else list()
        )
        return list(super().__dir__()) + builtin_func_name + user_func_names

    def include_library(self, library: FunctionLibrary) -> None:
        """Includes a function library.

        Args:
            library (FunctionLibrary): The function library.
        """
        if self._function_library is not None:
            raise ClassiqValueError("Another function library is already included.")

        self._function_library = library

    @property
    @abc.abstractmethod
    def _body(
        self,
    ) -> List[SynthesisQuantumFunctionCall]:
        pass

    @abc.abstractmethod
    def create_library(self) -> None:
        pass
