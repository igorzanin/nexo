from pydantic import BaseModel, ConfigDict


class SharingCreate(BaseModel):
    enabled: bool = False
    token: str = ""


class SharingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    enabled: bool
    token: str
