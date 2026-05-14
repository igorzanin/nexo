from pydantic import BaseModel


class WSCommand(BaseModel):
    action: str
    teamId: str = ""
    token: str = ""
    readToken: str = ""
    blockIds: list[str] = []


class WSMessage(BaseModel):
    action: str
    teamId: str = ""
    block: dict | None = None
    board: dict | None = None
    member: dict | None = None
    category: dict | None = None
    blockCategories: list | None = None
    subscription: dict | None = None
    clientConfig: dict | None = None
    timestamp: int | None = None
