from pydantic import BaseModel
from typing import List
from vbl_aquarium.models_unity import *

class CraniotomyModel(BaseModel):
    index: int
    size: Vector2
    position: Vector3
    rectangle: bool = False

class CraniotomyGroup(BaseModel):
    data: List[CraniotomyModel]