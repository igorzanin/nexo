from pydantic import BaseModel, ConfigDict


class TeamCreate(BaseModel):
    title: str
    signupToken: str = ""


class TeamResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    signupToken: str
    modifiedBy: str
    updateAt: int
