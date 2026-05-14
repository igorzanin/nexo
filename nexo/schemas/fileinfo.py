from pydantic import BaseModel, ConfigDict


class FileInfoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    boardId: str
    name: str
    extension: str
    size: int
    mimeType: str
    path: str
    createAt: int
    deleteAt: int
