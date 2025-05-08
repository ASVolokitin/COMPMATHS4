from decimal import Decimal
import math
from typing import List
from backend.utils.http_entities import DataInput
from backend.utils.response_constructor import generate_response, generate_response_fail_coefficients
from backend.utils.util_entities import ApproximationMethods, ApproximationParameters, ErrorCodes


def calculate_coefficients(data: DataInput) -> List[Decimal]:
    n = len(data.x)
    sx = Decimal(sum(data.x))
    sy = Decimal(sum(data.y))
    sxx = sum(Decimal(x)*Decimal(x) for x in data.x)
    sxy = sum(Decimal(x) * Decimal(y) for x, y in zip(data.x, data.y))

    delta = sxx * n - sx * sx
    delta_1 = sxy * n - sx * sy
    delta_2 = sxx * sy - sx * sxy

    if delta == 0: return None
        
    a = delta_1/delta
    b = delta_2/delta

    return [a, b]


def logarithmic_solve(data: DataInput):
    calculation_success = True
    errors = []

    if not all(x > 0 for x in data.x):
        errors.append("All X values must be greater than 0.")
        calculation_success = False
        return generate_response_fail_coefficients(data=data, errors=errors)
    
    log_x = list(map(math.log, data.x))
    log_data = DataInput(x=log_x, y=data.y)

    coefficients = calculate_coefficients(log_data)

    if coefficients == None:
        calculation_success = False
        errors.append(ErrorCodes.UNABLE_TO_CALCULATE_COEFFICIENTS)
        return generate_response_fail_coefficients(data=data, errors=errors)
    else:
        coefficients = [Decimal(a_i) for a_i in coefficients]
    
    logarithmic_phi = lambda x: coefficients[0] + coefficients[1] * Decimal(math.log(x))


    parameters = ApproximationParameters(data=data,
                                         method=ApproximationMethods.LOGARITHMIC,
                                         coefficients=coefficients,
                                         phi=logarithmic_phi,
                                         calculation_success=calculation_success,
                                         errors=errors)
    parameters.calculate()
    return generate_response(parameters)


