from decimal import Decimal
import numpy as np
from typing import List, Dict

from backend.solvers.cubic_approximation import cubic_solve
from backend.solvers.linear_approximation import linear_solve
from backend.utils.http_entities import DataInput
from backend.solvers.quadratic_approximation import quadratic_solve

def solve_all(data: DataInput):
    solutions = {}
    solutions["linear"] = linear_solve(data)
    solutions["quadratic"] = quadratic_solve(data)
    solutions["cubic"] = cubic_solve(data)

    min_mse = solutions["linear"].mse
    for solution in solutions.values(): min_mse = min(min_mse, solution.mse)
    for solution in solutions.values():
        if solution.mse == min_mse:
            solution.best_approximation = True
            break

    return solutions

def solve_approximation(data: DataInput):
    return solve_all(data)