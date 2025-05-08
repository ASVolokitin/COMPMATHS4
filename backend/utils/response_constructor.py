from pydantic import ValidationError
from backend.utils.http_entities import LinearResultOutput, ResultOutput
from backend.utils.util_entities import ApproximationMethods, ApproximationParameters

def generate_response(parameters: ApproximationParameters):
    coefficients=parameters.coefficients if parameters.coefficients is not None else [],
    mse=parameters.mse if parameters.mse is not None else 0,
    data=parameters.data,
    phi=parameters.phi if parameters.phi is not None else [],
    e_dots = parameters.e_dots if parameters.e_dots is not None else [],
    coefficient_of_determination=parameters.coefficient_of_determination if parameters.coefficient_of_determination is not None else 0,
    correlation_coefficient=parameters.correlation_coefficient if parameters.correlation_coefficient is not None else 0,
    calculation_success=parameters.calculation_success,
    best_approximation=False,
    errors=parameters.errors

    try:
        if parameters.method == ApproximationMethods.LINEAR:
            return LinearResultOutput.create(
                coefficients=parameters.coefficients if parameters.coefficients is not None else [],
                mse=parameters.mse if parameters.mse is not None else 0,
                data=parameters.data,
                phi=parameters.phi if parameters.phi is not None else [],
                e_dots = parameters.e_dots if parameters.e_dots is not None else [],
                coefficient_of_determination=parameters.coefficient_of_determination if parameters.coefficient_of_determination is not None else 0,
                correlation_coefficient=parameters.correlation_coefficient if parameters.correlation_coefficient is not None else 0,
                calculation_success=parameters.calculation_success,
                errors=parameters.errors
            )
        return ResultOutput.create(
            coefficients=parameters.coefficients if parameters.coefficients is not None else [],
            mse=parameters.mse if parameters.mse is not None else 0,
            data=parameters.data,
            phi=parameters.phi if parameters.phi is not None else [],
            e_dots = parameters.e_dots if parameters.e_dots is not None else [],
            coefficient_of_determination=parameters.coefficient_of_determination if parameters.coefficient_of_determination is not None else 0,
            calculation_success=parameters.calculation_success,
            errors=parameters.errors
        )
    except ValidationError:
        errors.append("The provided input results in values that are too large. Consider reducing the input range.")
        return generate_response_fail_coefficients(data, errors)

def generate_response_fail_coefficients(data, errors):
    return ResultOutput.create_empty(data, errors)