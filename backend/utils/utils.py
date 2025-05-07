from decimal import Decimal
import math
from typing import Callable, List, Tuple

import numpy as np

GRAPH_PARTITIONS_AMOUNT = 200


def generate_graph_points(x: List[Decimal], func) -> Tuple[List[Decimal], List[Decimal]]:
    x_plot = np.linspace(min(x), max(x), GRAPH_PARTITIONS_AMOUNT)
    y_plot = [func(x) for x in x_plot]

    x_plot_decimal = [Decimal(str(xi)) for xi in x_plot]
    y_plot_decimal = [Decimal(str(yi)) for yi in y_plot]

    return x_plot_decimal, y_plot_decimal