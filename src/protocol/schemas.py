import pydantic as pydantic
import time
import uuid

# Player Models

class PlayerResponse(pydantic.BaseModel):
    player_id: str
    nonce: bytes
    ciphertext: bytes
    
class PlayerPayload(pydantic.BaseModel):
    success: bool | None
    error: Error | None = None
    timestamp: float = pydantic.Field(default_factory=time.time)
    message_id: uuid.UUID = pydantic.Field(default_factory=uuid.uuid4)
    payload: dict
    
    
# Server Models

class ServerResponse(pydantic.BaseModel):
    nonce: bytes
    ciphertext: bytes
    
class ServerPayload(pydantic.BaseModel):
    success: bool
    error: Error | None = None
    timestamp: float
    message_id: uuid.UUID
    payload: dict
    
# Universal error model for all API responses
class Error(pydantic.BaseModel):
    error_code: str
    message: str