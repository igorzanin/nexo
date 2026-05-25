from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session as DBSession
from fastapi.responses import Response

from nexo.auth.dependencies import get_current_user
from nexo.db.session import get_db
from nexo.models import User
from nexo.services.file import FileService
from nexo.config import get_settings

router = APIRouter(prefix="/api/v1", tags=["files"])
settings = get_settings()


@router.post("/files/{team_id}/{board_id}")
async def upload_file(
    team_id: str,
    board_id: str,
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    content = await file.read()
    if len(content) > settings.max_file_size:
        raise HTTPException(status_code=413, detail="File too large")
    svc = FileService()
    file_id, ext, size = svc.store_file(board_id, file, content)
    svc.persist_metadata(
        db=db,
        file_id=file_id,
        board_id=board_id,
        creator_id=user.id,
        name=file.filename or file_id,
        extension=ext,
        size=size,
        mime_type=file.content_type,
    )
    url = f"/api/v1/files/{team_id}/{board_id}/{file_id}"
    if ext:
        url += f"?ext={ext}"
    return {"fileId": file_id, "extension": ext, "size": size, "boardId": board_id, "url": url}


@router.get("/files/{team_id}/{board_id}/{file_id}")
async def download_file(
    team_id: str,
    board_id: str,
    file_id: str,
    ext: str = "",
    user: User = Depends(get_current_user),
):
    svc = FileService()
    data = svc.read_file(board_id, file_id, ext)
    if data is None:
        raise HTTPException(status_code=404, detail="File not found")
    return Response(content=data, media_type="application/octet-stream")
