from pydantic import BaseModel
from typing import List
from vbl_aquarium.models_unity import *

# Standard types and lists
class IDData(BaseModel):
    id: str

class Vector3Data(BaseModel):
    id: str
    value: Vector3

class Vector3List(BaseModel):
    id: str
    values: List[Vector3]

class ColorData(BaseModel):
    id: str
    value: Color

class ColorList(BaseModel):
    id: str
    values: List[Color]

class StringData(BaseModel):
    id: str
    value: str

class StringList(BaseModel):
    id: str
    values: List[str]

class FloatData(BaseModel):
    id: str
    value: float

class FloatList(BaseModel):
    id: str
    values: List[float]

class IntData(BaseModel):
    id: str
    value: int

class IntList(BaseModel):
    id: str
    values: List[int]

class BoolData(BaseModel):
    id: str
    value: bool

class BoolList(BaseModel):
    id: str
    values: List[bool]

# ID lists 
    
class IDList(BaseModel):
    ids: List[str]

class IDListVector3Data(BaseModel):
    ids: List[str]
    value: Vector3

class IDListVector3List(BaseModel):
    ids: List[str]
    values: List[Vector3]

class IDListColorData(BaseModel):
    ids: List[str]
    value: Color

class IDListColorList(BaseModel):
    ids: List[str]
    values: List[Color]

class IDListStringData(BaseModel):
    ids: List[str]
    value: str

class IDListStringList(BaseModel):
    ids: List[str]
    values: List[str]

class IDListFloatData(BaseModel):
    ids: List[str]
    value: float

class IDListFloatList(BaseModel):
    ids: List[str]
    values: List[float]

class IDListIntData(BaseModel):
    ids: List[str]
    value: int

class IDListIntList(BaseModel):
    ids: List[str]
    values: List[int]

class IDListBoolData(BaseModel):
    ids: List[str]
    value: bool

class IDListBoolList(BaseModel):
    ids: List[str]
    values: List[bool]