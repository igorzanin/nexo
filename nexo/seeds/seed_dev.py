"""
Seed de desenvolvimento para o nexo.

Cria: admin user, time default, categoria My Boards, 3 board templates
(Kanban, Todo, Meeting Notes) com views e cards de exemplo.

Uso:
    python -m alembic.seeds.seed_dev
    # ou
    python alembic/seeds/seed_dev.py
"""

from __future__ import annotations

import sys
import time
import uuid
from pathlib import Path

# Permite rodar como script standalone a partir da raiz do projeto
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from sqlalchemy.orm import Session

from nexo.auth.password import hash_password
from nexo.db.session import SessionLocal, engine
from nexo.db.base import Base
from nexo.models import (
    Board,
    BoardMember,
    Block,
    Category,
    CategoryBoard,
    Preference,
    Sharing,
    Team,
    TeamMember,
    User,
)


# ─── helpers ───────────────────────────────────────────────────────────────────

def _now_ms() -> int:
    return int(time.time() * 1000)


def _id() -> str:
    return str(uuid.uuid4())


# ─── seed data builders ────────────────────────────────────────────────────────

def _make_user(db: Session) -> User:
    now = _now_ms()
    user = User(
        id=_id(),
        username="admin",
        email="admin@nexo.local",
        password_hash=hash_password("admin"),
        is_bot=False,
        props={},
        create_at=now,
        update_at=now,
        delete_at=0,
    )
    db.add(user)
    return user


def _make_onboarding_prefs(db: Session, user: User) -> None:
    for name in ("board", "card", "share_board"):
        db.add(Preference(
            user_id=user.id,
            category="onboarding",
            name=name,
            value="false",
        ))


def _make_team(db: Session) -> Team:
    now = _now_ms()
    team = Team(
        id=_id(),
        display_name="Default",
        type="O",
        description="Time padrão",
        create_at=now,
        update_at=now,
        delete_at=0,
    )
    db.add(team)
    return team


def _make_team_member(db: Session, team: Team, user: User) -> None:
    now = _now_ms()
    db.add(TeamMember(
        team_id=team.id,
        user_id=user.id,
        roles="team_admin",
        scheme_guest=False,
        scheme_user=True,
        scheme_admin=True,
        create_at=now,
        update_at=now,
        delete_at=0,
    ))


def _make_category(db: Session, user: User, team: Team) -> Category:
    now = _now_ms()
    cat = Category(
        id=_id(),
        name="My Boards",
        user_id=user.id,
        team_id=team.id,
        sort_order=0,
        type="system",
        create_at=now,
        update_at=now,
        delete_at=0,
    )
    db.add(cat)
    return cat


def _kanban_card_properties() -> list[dict]:
    status_prop_id = _id()
    priority_prop_id = _id()
    return [
        {
            "id": status_prop_id,
            "name": "Status",
            "type": "select",
            "options": [
                {"id": _id(), "value": "Not Started", "color": "propColorDefault"},
                {"id": _id(), "value": "In Progress", "color": "propColorYellow"},
                {"id": _id(), "value": "Done", "color": "propColorGreen"},
            ],
        },
        {
            "id": priority_prop_id,
            "name": "Priority",
            "type": "select",
            "options": [
                {"id": _id(), "value": "Low", "color": "propColorBlue"},
                {"id": _id(), "value": "Medium", "color": "propColorYellow"},
                {"id": _id(), "value": "High", "color": "propColorRed"},
            ],
        },
    ]


def _todo_card_properties() -> list[dict]:
    return [
        {
            "id": _id(),
            "name": "Done",
            "type": "checkbox",
            "options": [],
        },
        {
            "id": _id(),
            "name": "Due Date",
            "type": "date",
            "options": [],
        },
    ]


def _meeting_card_properties() -> list[dict]:
    return [
        {
            "id": _id(),
            "name": "Type",
            "type": "select",
            "options": [
                {"id": _id(), "value": "Action Item", "color": "propColorRed"},
                {"id": _id(), "value": "Decision", "color": "propColorGreen"},
                {"id": _id(), "value": "Note", "color": "propColorBlue"},
            ],
        },
    ]


def _make_board(
    db: Session,
    team: Team,
    user: User,
    title: str,
    card_properties: list[dict],
    sort_order: int,
) -> Board:
    now = _now_ms()
    board = Board(
        id=_id(),
        team_id=team.id,
        created_by=user.id,
        modified_by=user.id,
        type="O",
        minimum_role="",
        title=title,
        description="",
        icon="",
        show_description=False,
        is_template=True,
        template_version=1,
        properties={},
        card_properties=card_properties,
        create_at=now,
        update_at=now,
        delete_at=0,
    )
    db.add(board)
    return board


def _make_board_member(db: Session, board: Board, user: User) -> None:
    now = _now_ms()
    db.add(BoardMember(
        board_id=board.id,
        user_id=user.id,
        roles="admin",
        scheme_admin=True,
        scheme_editor=False,
        scheme_commenter=False,
        scheme_viewer=False,
        create_at=now,
        update_at=now,
        delete_at=0,
    ))


def _make_category_board(
    db: Session,
    category: Category,
    board: Board,
    user: User,
    team: Team,
    sort_order: int,
) -> None:
    now = _now_ms()
    db.add(CategoryBoard(
        id=_id(),
        user_id=user.id,
        team_id=team.id,
        category_id=category.id,
        board_id=board.id,
        sort_order=sort_order,
        hide=False,
        create_at=now,
        update_at=now,
        delete_at=0,
    ))


def _make_view_block(
    db: Session,
    board: Board,
    user: User,
    view_type: str,
    title: str,
) -> Block:
    now = _now_ms()
    block = Block(
        id=_id(),
        parent_id=None,
        root_id=None,
        created_by=user.id,
        modified_by=user.id,
        schema=1,
        type="view",
        title=title,
        fields={
            "viewType": view_type,
            "sortOptions": [],
            "visiblePropertyIds": [],
            "visibleOptionIds": [],
            "hiddenOptionIds": [],
            "filterGroups": [],
            "cardOrder": [],
            "columnWidths": {},
            "columnCalculations": {},
            "kanbanCalculations": {},
            "defaultTemplateId": "",
        },
        create_at=now,
        update_at=now,
        delete_at=0,
        board_id=board.id,
    )
    db.add(block)
    return block


def _make_card(
    db: Session,
    board: Board,
    user: User,
    title: str,
    properties: dict | None = None,
) -> Block:
    now = _now_ms()
    card = Block(
        id=_id(),
        parent_id=None,
        root_id=None,
        created_by=user.id,
        modified_by=user.id,
        schema=1,
        type="card",
        title=title,
        fields={
            "icon": "",
            "isTemplate": False,
            "properties": properties or {},
            "contentOrder": [],
        },
        create_at=now,
        update_at=now,
        delete_at=0,
        board_id=board.id,
    )
    db.add(card)
    return card


def _make_sharing(db: Session, board: Board, user: User, enabled: bool = False) -> None:
    now = _now_ms()
    db.add(Sharing(
        id=board.id,
        enabled=enabled,
        token=_id(),
        modified_by=user.id,
        update_at=now,
        create_at=now,
    ))


# ─── main seed ─────────────────────────────────────────────────────────────────

def seed(db: Session, *, verbose: bool = True) -> None:
    def log(msg: str) -> None:
        if verbose:
            print(f"  {msg}")

    # --- guard: skip if already seeded ---
    if db.query(User).filter_by(email="admin@nexo.local").first():
        print("Seed já aplicada (admin@nexo.local existe). Pulando.")
        return

    print("Aplicando seed de desenvolvimento...")

    user = _make_user(db)
    log(f"user: {user.email} (id={user.id[:8]}...)")

    _make_onboarding_prefs(db, user)
    log("preferences: onboarding 3 chaves")

    team = _make_team(db)
    log(f"team: {team.display_name} (id={team.id[:8]}...)")

    _make_team_member(db, team, user)
    log("team_member: admin como scheme_admin")

    category = _make_category(db, user, team)
    log(f"category: {category.name}")

    # Kanban template
    kanban_props = _kanban_card_properties()
    kanban = _make_board(db, team, user, "Kanban Template", kanban_props, sort_order=0)
    _make_board_member(db, kanban, user)
    _make_category_board(db, category, kanban, user, team, sort_order=0)
    _make_view_block(db, kanban, user, view_type="board", title="Board View")
    _make_view_block(db, kanban, user, view_type="table", title="Table View")
    status_id = kanban_props[0]["id"]
    status_opts = {o["value"]: o["id"] for o in kanban_props[0]["options"]}
    _make_card(db, kanban, user, "Example Card 1", {status_id: status_opts["Not Started"]})
    _make_card(db, kanban, user, "Example Card 2", {status_id: status_opts["In Progress"]})
    _make_card(db, kanban, user, "Example Card 3", {status_id: status_opts["Done"]})
    _make_sharing(db, kanban, user, enabled=True)
    log(f"board: {kanban.title} + 2 views + 3 cards + sharing")

    # Todo template
    todo = _make_board(db, team, user, "Todo Template", _todo_card_properties(), sort_order=1)
    _make_board_member(db, todo, user)
    _make_category_board(db, category, todo, user, team, sort_order=1)
    _make_view_block(db, todo, user, view_type="table", title="Table View")
    _make_view_block(db, todo, user, view_type="gallery", title="Gallery View")
    _make_sharing(db, todo, user, enabled=False)
    log(f"board: {todo.title} + 2 views")

    # Meeting Notes template
    meeting = _make_board(db, team, user, "Meeting Notes Template", _meeting_card_properties(), sort_order=2)
    _make_board_member(db, meeting, user)
    _make_category_board(db, category, meeting, user, team, sort_order=2)
    _make_view_block(db, meeting, user, view_type="table", title="Table View")
    _make_sharing(db, meeting, user, enabled=False)
    log(f"board: {meeting.title} + 1 view")

    db.commit()
    print("Seed concluída com sucesso.")


def run() -> None:
    db = SessionLocal()
    try:
        seed(db)
    finally:
        db.close()


if __name__ == "__main__":
    run()
