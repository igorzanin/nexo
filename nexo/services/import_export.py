import json
import time

from sqlalchemy.orm import Session as DBSession

from nexo.models import Block, Board


class ImportExportService:
    def __init__(self, db: DBSession):
        self.db = db

    def export_board(self, board_id: str) -> str:
        board = self.db.get(Board, board_id)
        if not board:
            raise ValueError("Board not found")

        lines = []
        board_data = {
            "type": "board",
            "id": board.id,
            "teamId": board.team_id,
            "title": board.title,
            "description": board.description,
            "icon": board.icon,
            "type_flag": board.type,
            "showDescription": board.show_description,
            "isTemplate": board.is_template,
            "templateVersion": board.template_version,
            "minimumRole": board.minimum_role,
            "createAt": board.create_at,
            "updateAt": board.update_at,
        }
        lines.append(json.dumps(board_data, ensure_ascii=False))

        blocks = self.db.query(Block).filter(
            Block.board_id == board_id,
            Block.delete_at == 0,
        ).all()

        for block in blocks:
            block_data = {
                "type": "block",
                "id": block.id,
                "boardId": block.board_id,
                "parentId": block.parent_id,
                "createdBy": block.created_by,
                "modifiedBy": block.modified_by,
                "type_flag": block.type,
                "title": block.title,
                "fields": block.fields,
                "schema": block.schema,
                "createAt": block.create_at,
                "updateAt": block.update_at,
            }
            lines.append(json.dumps(block_data, ensure_ascii=False))

        return "\n".join(lines)

    def import_board(self, data: str, user_id: str) -> Board:
        lines = [l.strip() for l in data.split("\n") if l.strip()]
        if not lines:
            raise ValueError("Empty archive")

        header = json.loads(lines[0])
        if header.get("type") != "board":
            raise ValueError("First line must be board data")

        now = int(time.time() * 1000)
        board = Board(
            team_id=header.get("teamId", ""),
            type=header.get("type_flag", "P"),
            title=header.get("title", "Imported"),
            description=header.get("description", ""),
            icon=header.get("icon", ""),
            show_description=header.get("showDescription", False),
            is_template=False,
            template_version=0,
            minimum_role=header.get("minimumRole", ""),
            create_at=now,
            update_at=now,
            delete_at=0,
        )
        self.db.add(board)
        self.db.flush()

        for line in lines[1:]:
            item = json.loads(line)
            if item.get("type") == "block":
                block = Block(
                    id=item.get("id", ""),
                    board_id=board.id,
                    parent_id=item.get("parentId") or None,
                    created_by=user_id,
                    modified_by=user_id,
                    type=item.get("type_flag", "text"),
                    title=item.get("title", ""),
                    fields=item.get("fields", {}),
                    schema=item.get("schema", 1),
                    create_at=item.get("createAt", now),
                    update_at=now,
                    delete_at=0,
                )
                self.db.add(block)

        self.db.commit()
        self.db.refresh(board)
        return board
