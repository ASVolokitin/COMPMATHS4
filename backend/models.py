from decimal import Decimal
from backend.utils.utils import generate_graph_points
from pydantic import BaseModel, field_serializer
from typing import Callable, List, Dict

class DataInput(BaseModel):
    x: List[Decimal]
    y: List[Decimal]

class ResultOutput(BaseModel):
    coefficients: List[Decimal]
    mse: Decimal
    x: List[Decimal]
    y: List[Decimal]
    x_for_graph: List[Decimal]
    y_for_graph: List[Decimal]
    phi_dots: List[Decimal]
    e_dots: List[Decimal]
    coefficient_of_determination: Decimal
    best_approximation: bool
    calculation_success: bool
    errors: List[str]

    @classmethod
    def create(
        cls,
        coefficients,
        mse,
        data: DataInput,
        phi,
        e_dots,
        coefficient_of_determination,
        calculation_success,
        errors
    ):
        graph_info = generate_graph_points(data.x, phi)
        return cls(
            coefficients=coefficients,
            mse=mse,
            x=data.x,
            y=data.y,
            x_for_graph=graph_info[0],
            y_for_graph=graph_info[1],
            phi_dots=[phi(x) for x in data.x] if phi is not None else [],
            e_dots=e_dots,
            coefficient_of_determination=coefficient_of_determination,
            best_approximation=False,
            calculation_success=calculation_success,
            errors=errors
        )

class LinearResultOutput(ResultOutput):
    correlation_coefficient: Decimal
    @classmethod
    def create(
        cls,
        coefficients,
        mse,
        data: DataInput,
        phi,
        e_dots,
        coefficient_of_determination,
        correlation_coefficient,
        calculation_success,
        errors
    ):
        graph_info = generate_graph_points(data.x, phi)
        return cls(
            coefficients=coefficients,
            mse=mse,
            x=data.x,
            y=data.y,
            x_for_graph=graph_info[0],
            y_for_graph=graph_info[1],
            phi_dots=[phi(x) for x in data.x] if phi is not None else [],
            e_dots=e_dots,
            coefficient_of_determination=coefficient_of_determination,
            correlation_coefficient=correlation_coefficient,
            best_approximation=False,
            calculation_success=calculation_success,
            errors=errors
        )