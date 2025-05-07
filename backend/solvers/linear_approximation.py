from decimal import Decimal
import math
from backend.models import DataInput, LinearResultOutput
from backend.utils.response_constructor import generate_response, generate_response_fail_coefficients
from backend.utils.util_entities import ApproximationMethods, ApproximationParameters, ErrorCodes
from backend.utils.calculation_utils import calculate_determination_coefficient, calculate_e_dots, calculate_mse




def linear_solve(data: DataInput):
    calculation_success = True
    errors = []

    n = len(data.x)
    sx = Decimal(sum(data.x))
    sy = Decimal(sum(data.y))
    sxx = sum(Decimal(x)*Decimal(x) for x in data.x)
    sxy = sum(Decimal(x) * Decimal(y) for x, y in zip(data.x, data.y))

    delta = sxx * n - sx * sx
    delta_1 = sxy * n - sx * sy
    delta_2 = sxx * sy - sx * sxy

    if delta == 0:
        calculation_success = False
        errors.append(ErrorCodes.UNABLE_TO_CALCULATE_COEFFICIENTS)
        return generate_response_fail_coefficients(data=data)
    
    a = delta_1/delta
    b = delta_2/delta
    coefficients = [a, b]
    linear_phi = lambda x: Decimal(a * Decimal(x) + b)

    parameters = ApproximationParameters(data=data,
                                         method=ApproximationMethods.LINEAR,
                                         coefficients=coefficients,
                                         phi=linear_phi,
                                         calculation_success=calculation_success,
                                         errors=errors)
    parameters.calculate()
    return generate_response(parameters)


