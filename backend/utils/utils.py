from decimal import Decimal
import math
from typing import Callable, List, Tuple

import numpy as np

GRAPH_PARTITIONS_AMOUNT = 200


def generate_graph_points(x: List[Decimal], func, errors) -> Tuple[List[Decimal], List[Decimal]]:
    try:
        if min(x) < 0:
            x_plot = np.linspace(min(x) - max(Decimal(2), abs(min(x)) * Decimal(0.3)), max(x) + max(Decimal(2), abs(max(x)) * Decimal(0.3)), GRAPH_PARTITIONS_AMOUNT)
        else:
            x_plot = np.linspace(max(Decimal('1e-10'), min(x) - max(Decimal(2), abs(min(x)) * Decimal(0.3))), max(x) + max(Decimal(2), abs(max(x)) * Decimal(0.3)), GRAPH_PARTITIONS_AMOUNT)
        try:
            y_plot = [func(x) for x in x_plot]
        except ZeroDivisionError:
            errors.append("Impossible to calculate graph points over the entire interval.")
            return None

        x_plot_decimal = [Decimal(str(xi)) for xi in x_plot]
        y_plot_decimal = [Decimal(str(yi)) for yi in y_plot]

        return x_plot_decimal, y_plot_decimal

    except ZeroDivisionError:
        errors.append("Zero deivision error occured while calculating points for graph.")
        return None
    except OverflowError:
        errors.append("Overflow error occured while calculating points for graph.")
        return None
    except TypeError:
        errors.append("It is impossible to calculate the points for the graph (approximation function is undefined).")
        return None
    
def is_number(value):
    if isinstance(value, (int, float)):
        return True
    if isinstance(value, str):
        try:
            float(value)  # Пробуем преобразовать в float (работает и для целых)
            return True
        except ValueError:
            return False
    return False
