from decimal import Decimal
import math
from typing import List
from backend.utils.http_entities import DataInput
from backend.utils.calculation_utils import calculate_linear_coefficients
from backend.utils.response_constructor import generate_response, generate_response_fail_coefficients
from backend.utils.util_entities import ApproximationMethods, ApproximationParameters, ErrorCodes

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
    
    ln_x = list(x.ln() for x in data.x)
    ln_y = list(y.ln() for y in data.y)
    ln_data = DataInput(x=ln_x, y=ln_y)

    coefficients = calculate_linear_coefficients(ln_data)

    if coefficients == None:
        calculation_success = False
        errors.append(ErrorCodes.UNABLE_TO_CALCULATE_COEFFICIENTS)
        return generate_response_fail_coefficients(data=data, errors=errors)
    else:
        coefficients = [Decimal(a_i) for a_i in coefficients]
        a = coefficients[1].exp()
        b = coefficients[0]
    
    power_phi = lambda x: Decimal(a) * (Decimal(x) ** Decimal(b))


    parameters = ApproximationParameters(data=data,
                                         method=ApproximationMethods.POWER,
                                         coefficients=coefficients,
                                         phi=power_phi,
                                         calculation_success=calculation_success,
                                         errors=errors)
    parameters.calculate()
    return generate_response(parameters)


