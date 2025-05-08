from decimal import Decimal
from typing import List
from backend.utils.calculation_utils import calculate_linear_coefficients
from backend.utils.http_entities import DataInput
from backend.utils.response_constructor import generate_response, generate_response_fail_coefficients
from backend.utils.util_entities import ApproximationMethods, ApproximationParameters, ErrorCodes

# def calculate_coefficients(data: DataInput) -> List[Decimal]:
#     n = len(data.x)
#     sx = Decimal(sum(data.x))
#     sy = Decimal(sum(data.y))
#     sxx = sum(Decimal(x)*Decimal(x) for x in data.x)
#     sxy = sum(Decimal(x) * Decimal(y) for x, y in zip(data.x, data.y))

#     delta = sxx * n - sx * sx
#     delta_1 = sxy * n - sx * sy
#     delta_2 = sxx * sy - sx * sxy

#     if delta == 0: return None
        
#     a = delta_1/delta
#     b = delta_2/delta

#     return [a, b]


def linear_solve(data: DataInput):
    calculation_success = True
    errors = []

    coefficients = calculate_linear_coefficients(data)

    if coefficients == None:
        calculation_success = False
        errors.append(ErrorCodes.UNABLE_TO_CALCULATE_COEFFICIENTS)
        return generate_response_fail_coefficients(data=data, errors=errors)
    else:
        a, b = coefficients[0], coefficients[1]

    
    linear_phi = lambda x: Decimal(a * Decimal(x) + b)

    parameters = ApproximationParameters(data=data,
                                         method=ApproximationMethods.LINEAR,
                                         coefficients=coefficients,
                                         phi=linear_phi,
                                         calculation_success=calculation_success,
                                         errors=errors)
    parameters.calculate()
    return generate_response(parameters)


