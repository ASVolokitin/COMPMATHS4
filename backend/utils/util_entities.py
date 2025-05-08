from decimal import Decimal
from typing import Callable, List
from backend.utils.http_entities import DataInput
from enum import Enum
from backend.utils.calculation_utils import calculate_determination_coefficient, calculate_e_dots, calculate_mse, calculate_pearson

class ErrorCodes(str, Enum):
    UNABLE_TO_CALCULATE_COEFFICIENTS="The coefficients of the approximating function could not be calculated."
    UNABLE_TO_CALCULATE_MSE="Couldn't calculate mean squared error."
    UNABLE_TO_CALCULATE_DETERMINATION="Couldn't calculate the coefficient of determination."
    UNABLE_TO_CALCULATE_CORRELATION="Couldn't calculate Pearson correlation coefficient."
    UNABLE_TO_CALCULATE_GRAPH_POINTS="Couldn't calculate graph points."

class ApproximationMethods(str, Enum):
    LINEAR="linear"
    QUADRATIC="quadratic"
    CUBIC="cubic"
    EXPONENTIAL="exponential"
    LOGARITHMIC="logarithmic"
    POWER="power"

class ApproximationParameters():

    def __init__(self, data: DataInput, method: ApproximationMethods, coefficients: List[Decimal], phi: Callable[[Decimal], Decimal], calculation_success: bool, errors: List[str]):
        self.data=data
        self.method=method
        self.coefficients=coefficients
        self.phi=phi
        self.mse=0
        self.coefficient_of_determination=0,
        self.correlation_coefficient = None,
        self.e_dots=[]
        self.calculation_success=calculation_success
        self.errors=errors
    
    def calculate(self):
        mse = calculate_mse(self.data.x, self.data.y, self.phi)
        if mse is None:
            self.mse=0
            self.calculation_success=False
            self.errors.append(ErrorCodes.UNABLE_TO_CALCULATE_MSE)
        else: self.mse = mse

        coefficient_of_determination = calculate_determination_coefficient(self.data.x, self.data.y, self.phi)
        if coefficient_of_determination is None:
            self.coefficient_of_determination=0
            self.calculation_success=False
            self.errors.append(ErrorCodes.UNABLE_TO_CALCULATE_DETERMINATION)
        else: self.coefficient_of_determination = coefficient_of_determination
        
        if self.method == ApproximationMethods.LINEAR:
            correlation_coefficient = calculate_pearson(self.data.x, self.data.y)
            if correlation_coefficient is None:
                self.correlation_coefficient=0
                self.calculation_success=False
                self.errors.append(ErrorCodes.UNABLE_TO_CALCULATE_CORRELATION)
            else: self.correlation_coefficient = correlation_coefficient

        
        self.e_dots = calculate_e_dots(self.data.x, self.data.y, self.phi)