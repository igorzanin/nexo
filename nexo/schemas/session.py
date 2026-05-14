from pydantic import BaseModel, ConfigDict


class SessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    token: str
    userId: str
    createAt: int
    updateAt: int
    expiresAt: int
