from decimal import Decimal
import math
from typing import Callable, List

from backend.utils.http_entities import DataInput


def calculate_determination_coefficient(X, Y, phi: Callable[[Decimal], Decimal]):
    try:
        numerator = 0
        denominator = 0

        mean_phi = sum(phi(x) for x in X)/len(X)

        for i in range(len(X)):
            numerator += (Y[i] - phi(X[i]))
            denominator += (Y[i] - mean_phi)
        
        if denominator != 0: return 1 - numerator / denominator
        else: return 1
    except (ValueError, ZeroDivisionError, OverflowError):
        return None


def calculate_e_dots(X: List[Decimal], Y: List[Decimal], phi: Callable[[Decimal], Decimal]):
    try:
        e_dots = []
        for i in range(len(X)):
            e_i = (phi(X[i]) - Decimal(Y[i]))**2
            e_dots.append(e_i)
        
        return e_dots
    except (ValueError, ZeroDivisionError, OverflowError):
        return None

def calculate_mse(X: List[Decimal], Y: List[Decimal], phi: Callable[[Decimal], Decimal]):
    try:
        numerator = 0

        for i in range(len(X)):
            numerator += (phi(X[i]) - Y[i])**2
        
        return math.sqrt(numerator/len(X))
    except (ValueError, ZeroDivisionError, OverflowError):
        return None

def calculate_pearson(X, Y):
    try:
        mean_X = sum(X)/Decimal(len(X))
        mean_Y = sum(Y)/Decimal(len(Y))

        numerator = 0
        denominator_X = 0
        denominator_Y = 0

        for i in range(len(X)):
            numerator += (X[i] - mean_X) * (Y[i] - mean_Y)
            denominator_X += (X[i] - mean_X)**2
            denominator_Y += (Y[i] - mean_Y)**2
        
        pirson = 0
        if denominator_X != 0 and denominator_Y != 0:
            return numerator / Decimal(math.sqrt(denominator_X * denominator_Y))
        else: return None
    except (ValueError, ZeroDivisionError, OverflowError):
        return None
    
def calculate_linear_coefficients(data: DataInput) -> List[Decimal]:
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