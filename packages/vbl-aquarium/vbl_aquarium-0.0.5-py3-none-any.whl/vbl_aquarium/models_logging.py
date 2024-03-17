from pydantic import BaseModel

class LogError(BaseModel):
    msg: str
    
class LogWarning(BaseModel):
    msg: str

class Log(BaseModel):
    msg: str

    