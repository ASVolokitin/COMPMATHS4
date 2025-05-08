from decimal import Decimal
import math
from typing import List
from backend.utils.http_entities import DataInput
from backend.utils.calculation_utils import calculate_linear_coefficients
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


def power_solve(data: DataInput):
    calculation_success = True
    errors = []

    if not all(x > 0 for x in data.x):
        errors.append("All X values must be greater than 0.")
        calculation_success = False
        return generate_response_fail_coefficients(data=data, errors=errors)
    
    if not all(y > 0 for y in data.y):
        errors.append("All Y values must be greater than 0.")
        calculation_success = False
        return generate_response_fail_coefficients(data=data, errors=errors)
    
    log_x = list(map(math.log, data.x))
    log_y = list(map(math.log, data.y))
    log_data = DataInput(x=log_x, y=log_y)

    coefficients = calculate_linear_coefficients(log_data)

    if coefficients == None:
        calculation_success = False
        errors.append(ErrorCodes.UNABLE_TO_CALCULATE_COEFFICIENTS)
        return generate_response_fail_coefficients(data=data, errors=errors)
    else:
        coefficients[0] = math.exp(coefficients[0])
        coefficients = [Decimal(a_i) for a_i in coefficients]
    
    power_phi = lambda x: coefficients[0] * x**coefficients[1]


    parameters = ApproximationParameters(data=data,
                                         method=ApproximationMethods.POWER,
                                         coefficients=coefficients,
                                         phi=power_phi,
                                         calculation_success=calculation_success,
                                         errors=errors)
    parameters.calculate()
    return generate_response(parameters)


