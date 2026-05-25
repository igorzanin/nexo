from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession

from nexo.auth.dependencies import get_current_user
from nexo.db.session import get_db
from nexo.models import User
from nexo.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from nexo.services.category import CategoryService

router = APIRouter(prefix="/api/v1", tags=["categories"])


@router.get("/teams/{team_id}/categories")
async def get_categories(
    team_id: str,
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    svc = CategoryService(db)
    cats = svc.get_by_team(team_id)
    return [
        CategoryResponse.model_validate(c, from_attributes=True).model_dump(by_alias=True)
        for c in cats
    ]


@router.post("/categories", response_model=CategoryResponse)
async def create_category(
    data: CategoryCreate,
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    svc = CategoryService(db)
    cat = svc.create(data)
    return CategoryResponse.model_validate(cat, from_attributes=True)


@router.patch("/categories/{category_id}", response_model=CategoryResponse)
async def patch_category(
    category_id: str,
    data: CategoryUpdate,
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    svc = CategoryService(db)
    cat = svc.update(category_id, data)
    return CategoryResponse.model_validate(cat, from_attributes=True)


@router.delete("/categories/{category_id}", status_code=204)
async def delete_category(
    category_id: str,
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    svc = CategoryService(db)
    svc.delete(category_id)


@router.post("/categories/reorder")
async def reorder_categories(
    data: list[str],
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    svc = CategoryService(db)
    svc.reorder_categories(data)
    return {"ok": True}


@router.post("/categories/{category_id}/reorder")
async def reorder_category_boards(
    category_id: str,
    data: list[str],
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    svc = CategoryService(db)
    svc.reorder_category_boards(category_id, data)
    return {"ok": True}
