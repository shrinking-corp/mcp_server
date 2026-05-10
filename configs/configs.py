from pydantic import BaseModel
from typing import Literal


"""
Type validation for configs. If an agent fills out config incorectly 
it should get a runtime error that will tell it where the mistake is
"""

class KruskalWeights(BaseModel):
    dependency: float = 1
    extension: float = 3
    implementation: float = 3
    aggregation: float = 2
    composition: float = 2
    association: float = 1

class EvolConfig(BaseModel):
    kind: Literal["evol"] = "evol"
    generations: int | None = None
    population_size: int | None = None

    def __str__(self) -> str: 
        return "Evolutionary algorithm configuration"

class KruskalConfig(BaseModel):
    kind: Literal["kruskals"] = "kruskals"
    weights: KruskalWeights | None = None

    def __str__(self) -> str:
        return "Kruskal's algorithm configuration"
