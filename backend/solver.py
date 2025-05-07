from decimal import Decimal
import numpy as np
from typing import List, Dict

from backend.solvers.linear_approximation import linear_solve
from backend.utils.http_entities import DataInput
from backend.solvers.quadratic_approximation import quadratic_solve

def solve_all(data: DataInput):
    solutions = {}
    solutions["linear"] = linear_solve(data)
    solutions["quadratic"] = quadratic_solve(data)
    return solutions

def solve_approximation(data: DataInput):
    return solve_all(data)