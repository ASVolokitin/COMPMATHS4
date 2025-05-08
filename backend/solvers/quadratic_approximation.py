
from decimal import Decimal
from typing import List
from backend.utils.http_entities import DataInput
from sympy import Matrix

from backend.utils.response_constructor import generate_response, generate_response_fail_coefficients
from backend.utils.util_entities import ApproximationMethods, ApproximationParameters, ErrorCodes

def calculate_coefficients(data: DataInput) -> List[Decimal]:
    x_0 = len(data.x)
    x_1 = sum(data.x)
    x_2 = sum(x * x for x in data.x)
    x_3 = sum(x * x * x for x in data.x)
    x_4 = sum(x * x * x * x for x in data.x)
    y_0 = sum(data.y)
    x_y = sum(x * y for x, y in zip(data.x, data.y))
    x_2_y = sum(x * x * y for x, y in zip(data.x, data.y))

    A = Matrix([
        [x_0, x_1, x_2],
        [x_1, x_2, x_3],
        [x_2, x_3, x_4]])
    B = Matrix([y_0, x_y, x_2_y])

    coefficients = None
    try:
        coefficients = [Decimal(str(a)) for a in A.LUsolve(B)]
    except ValueError:
        print("Singular matrix, the system does not have a single solution.")
    
    return coefficients

    

def quadratic_solve(data: DataInput):
    calculation_success = True
    errors = []

    coefficients = calculate_coefficients(data)
    print(coefficients)
    if coefficients is None:
        coefficients = []
        calculation_success = False
        errors.append(ErrorCodes.UNABLE_TO_CALCULATE_COEFFICIENTS)
        return generate_response_fail_coefficients(data, errors=errors)
    
    quadratic_phi = lambda x: coefficients[0] + coefficients[1] * x + coefficients[2] * x * x

    parameters = ApproximationParameters(
        data=data,
        method=ApproximationMethods.QUADRATIC,
        coefficients=coefficients,
        phi=quadratic_phi,
        calculation_success=calculation_success,
        errors=errors
    )
    parameters.calculate()

    return generate_response(parameters=parameters)
    

