
from decimal import Decimal
from typing import List

from sympy import Matrix
from backend.utils.http_entities import DataInput
from backend.utils.response_constructor import generate_response, generate_response_fail_coefficients
from backend.utils.util_entities import ApproximationMethods, ApproximationParameters, ErrorCodes


def calculate_coefficients(data: DataInput) -> List[Decimal]:
    

    A = Matrix([
        [len(data.x), sum(data.x), sum(x**2 for x in data.x), sum(x**3 for x in data.x)],
        [sum(data.x), sum(x * x for x in data.x), sum(x**3 for x in data.x), sum(x**4 for x in data.x)],
        [sum(x**2 for x in data.x), sum(x**3 for x in data.x), sum(x**4 for x in data.x), sum(x**5 for x in data.x)],
        [sum(x**3 for x in data.x), sum(x**4 for x in data.x), sum(x**5 for x in data.x), sum(x**6 for x in data.x)]])
    B = Matrix([sum(data.y), sum(x * y for x, y in zip(data.x, data.y)), sum(x**2 * y for x, y in zip(data.x, data.y)), sum(x**3 * y for x, y in zip(data.x, data.y))])

    coefficients = None
    try:
        coefficients = [Decimal(str(a)) for a in A.LUsolve(B)]
    except ValueError:
        print("Singular matrix, the system does not have a single solution.")
    
    return coefficients

    

def cubic_solve(data: DataInput):
    calculation_success = True
    errors = []

    coefficients = calculate_coefficients(data)
    print(coefficients)
    if coefficients is None:
        coefficients = []
        calculation_success = False
        errors.append(ErrorCodes.UNABLE_TO_CALCULATE_COEFFICIENTS)
        return generate_response_fail_coefficients(data)
    
    cubic_phi = lambda x: coefficients[0] + coefficients[1] * x + coefficients[2] * x * x + coefficients[3] * x**3

    parameters = ApproximationParameters(
        data=data,
        method=ApproximationMethods.QUADRATIC,
        coefficients=coefficients,
        phi=cubic_phi,
        calculation_success=calculation_success,
        errors=errors
    )
    parameters.calculate()

    return generate_response(parameters=parameters)