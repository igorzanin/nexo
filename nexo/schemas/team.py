from pydantic import BaseModel, ConfigDict


class TeamCreate(BaseModel):
    title: str
    signupToken: str = ""


class TeamResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    display_name: str
    type: str = "O"
    create_at: int = 0
    update_at: int = 0
    delete_at: int = 0
