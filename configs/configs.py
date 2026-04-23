from pydantic import BaseModel
from typing import Literal


"""
Type validation for configs. If an agent fills out config incorectly 
it should get a runtime error that will tell it where the mistake is
"""

class EvolConfig(BaseModel):
    kind: Literal["evol"] = "evol"
    iterations: int | None = None
    population: int | None = None

    def __str__(self) -> str: 
        return "Evolutionary algorithm configuration"

class KruskalConfig(BaseModel):
    kind: Literal["kruskals"] = "kruskals"
    weights: dict[str, float] | None = None

    def __str__(self) -> str:
        return "Kruskal's algorithm configuration"
