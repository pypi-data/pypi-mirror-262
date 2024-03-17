from pydantic import BaseModel
from typing import List
from vbl_aquarium.models_unity import *

# CustomAtlas

class CustomAtlasModel(BaseModel):
    name: str
    dimensions: Vector3
    resolution: Vector3

# CustomMesh

class CustomMeshData(BaseModel):
    id: str
    vertices: List[Vector3]
    triangles: List[int]
    normals: List[Vector3] = None

class CustomMeshModel(BaseModel):
    id: str
    position: Vector3
    use_reference: bool
    material: str
    scale: Vector3
    color: Color

# Area
    
class AreaGroupData(BaseModel):
    acronyms: List[str]
    visible: List[bool]
    side: List[int]

# Camera
    
class CameraModel(BaseModel):
    class CameraMode(str, Enum):
        orthographic = "orthographic"
        perspective = "perspective"

    id: float
    type: str
    position: Vector3
    rotation: Vector3
    target: Vector3
    zoom: float
    pan: Vector2
    mode: CameraMode
    controllable: bool
    main: bool
    
# Individual mesh neuron
    
class MeshModel(BaseModel):
    id: str
    shape: str
    position: Vector3
    color: Color
    scale: Vector3
    material: str
    interactive: bool

# Particle group
    
class ParticleGroupModel(BaseModel):
    id: str
    scale: Vector3
    shape: str
    material: str

    xs: List[float]
    ys: List[float]
    zs: List[float]

    colors: List[Color]