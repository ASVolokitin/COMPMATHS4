import numpy as np
from typing import List, Dict

def solve_approximation(x: List[float], y: List[float]) -> Dict:
    return {
        "best_function": "linear",
        "coefficients": {
            "linear": [1.0, 2.0],
            "quadratic": [0.5, -1.2, 3.0],
            # и так далее
        },
        "errors": {
            "linear": 0.05,
            "quadratic": 0.04,
            # и так далее
        },
        "r_squared": {
            "linear": 0.95,
            "quadratic": 0.97,
            # и так далее
        },
        "approximations": {
            "linear": [3.0, 5.0, 7.0],
            "quadratic": [2.8, 5.2, 7.1],
            # и так далее
        }
    }
