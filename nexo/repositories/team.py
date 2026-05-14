import time

from sqlalchemy.orm import Session as DBSession

from nexo.models import Team
from nexo.schemas.team import TeamCreate


class TeamRepository:
    def __init__(self, db: DBSession):
        self.db = db

    def get(self, team_id: str) -> Team | None:
        return self.db.get(Team, team_id)

    def get_all(self) -> list[Team]:
        return list(self.db.query(Team).all())

    def create(self, data: TeamCreate) -> Team:
        team = Team(
            title=data.title,
            signupToken=data.signupToken,
            modifiedBy="",
            updateAt=int(time.time() * 1000),
        )
        self.db.add(team)
        self.db.commit()
        self.db.refresh(team)
        return team
