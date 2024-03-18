from datetime import datetime
from typing import Any, Dict, List, Literal, Optional, Union

import pydantic
from pydantic import BaseModel, Field
from typing_extensions import Annotated

from classiq.interface.backend.backend_preferences import IonqBackendPreferences
from classiq.interface.executor.estimation import OperatorsEstimation
from classiq.interface.executor.execution_preferences import ExecutionPreferences
from classiq.interface.executor.quantum_code import QuantumCode, QuantumInstructionSet
from classiq.interface.generator.quantum_program import QuantumProgram
from classiq.interface.helpers.custom_encoders import CUSTOM_ENCODERS
from classiq.interface.helpers.versioned_model import VersionedModel
from classiq.interface.jobs import JobStatus

from classiq.exceptions import ClassiqValueError


class QuantumProgramExecution(QuantumProgram):
    execution_type: Literal["quantum_program2"] = "quantum_program2"


class QuantumCodeExecution(QuantumCode):
    execution_type: Literal["quantum_code"] = "quantum_code"


class EstimateOperatorsExecution(OperatorsEstimation):
    execution_type: Literal["estimate_operators"] = "estimate_operators"


ExecutionPayloads = Annotated[
    Union[QuantumProgramExecution, QuantumCodeExecution, EstimateOperatorsExecution],
    Field(discriminator="execution_type"),
]


class ExecutionRequest(BaseModel, json_encoders=CUSTOM_ENCODERS):
    execution_payload: ExecutionPayloads
    preferences: ExecutionPreferences = pydantic.Field(
        default_factory=ExecutionPreferences,
        description="preferences for the execution",
    )

    @pydantic.validator("preferences")
    def validate_ionq_backend(
        cls, preferences: ExecutionPreferences, values: Dict[str, Any]
    ) -> ExecutionPreferences:
        """
        This function implement the following check:
        BE \\ payload | IonQ program | Qasm program | Other
        --------------|--------------|--------------|------
        IonQ backend  |       V      |      V       |   X
        Other backend |       X      |      V       |   V
        Since:
        - We can't execute non-programs on the IonQ backends
        - We can't execute IonQ programs on non-IonQ backends
        """
        quantum_program = values.get("execution_payload")
        is_ionq_backend = isinstance(
            preferences.backend_preferences, IonqBackendPreferences
        )
        if isinstance(quantum_program, QuantumCode):
            if (
                quantum_program.syntax == QuantumInstructionSet.IONQ
                and not is_ionq_backend
            ):
                raise ClassiqValueError("Can only execute IonQ code on IonQ backend.")
        else:
            # If we handle anything other than a program.
            if is_ionq_backend:
                raise ClassiqValueError(
                    "IonQ backend supports only execution of QuantumPrograms"
                )
        return preferences


class QuantumProgramExecutionRequest(ExecutionRequest):
    execution_payload: QuantumCodeExecution


class ExecutionJobDetails(VersionedModel):
    id: str

    name: Optional[str]
    start_time: datetime
    end_time: Optional[datetime]

    provider: Optional[str]
    backend_name: Optional[str]

    status: JobStatus

    num_shots: Optional[int]
    program_id: Optional[str]

    error: Optional[str]


class ExecutionJobsQueryResults(VersionedModel):
    results: List[ExecutionJobDetails]
