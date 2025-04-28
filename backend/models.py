from pydantic import BaseModel
from typing import List, Dict

class DataInput(BaseModel):
    x: List[float]
    y: List[float]

class ResultOutput(BaseModel):
    best_function: str
    coefficients: Dict[str, List[float]]
    errors: Dict[str, float]
    r_squared: Dict[str, float]
    approximations: Dict[str, List[float]]
