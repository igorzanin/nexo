from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as DBSession

from nexo.auth.dependencies import get_current_user
from nexo.db.session import get_db
from nexo.models import User
from nexo.repositories.team import TeamRepository
from nexo.schemas.team import TeamResponse, TeamCreate

router = APIRouter(prefix="/api/v1", tags=["teams"])


@router.get("/teams", response_model=list[TeamResponse])
async def get_teams(
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    repo = TeamRepository(db)
    teams = repo.get_all()
    return [TeamResponse.model_validate(t, from_attributes=True) for t in teams]


@router.get("/teams/{team_id}", response_model=TeamResponse)
async def get_team(
    team_id: str,
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    repo = TeamRepository(db)
    team = repo.get(team_id)
    return TeamResponse.model_validate(team, from_attributes=True)


@router.post("/teams", response_model=TeamResponse)
async def create_team(
    data: TeamCreate,
    user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    repo = TeamRepository(db)
    team = repo.create(data)
    return TeamResponse.model_validate(team, from_attributes=True)
