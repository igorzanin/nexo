import json
import time

from sqlalchemy.orm import Session as DBSession

from nexo.models import Board, Block


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
            "teamId": board.teamId,
            "title": board.title,
            "description": board.description,
            "icon": board.icon,
            "type_flag": board.type,
            "showDescription": board.showDescription,
            "isTemplate": board.isTemplate,
            "templateVersion": board.templateVersion,
            "minimumRole": board.minimumRole,
            "createAt": board.createAt,
            "updateAt": board.updateAt,
        }
        lines.append(json.dumps(board_data, ensure_ascii=False))

        blocks = self.db.query(Block).filter(
            Block.boardId == board_id,
            Block.deleteAt == 0,
        ).all()

        for block in blocks:
            block_data = {
                "type": "block",
                "id": block.id,
                "boardId": block.boardId,
                "parentId": block.parentId,
                "createdBy": block.createdBy,
                "modifiedBy": block.modifiedBy,
                "type_flag": block.type,
                "title": block.title,
                "fields": block.fields,
                "schema": block.schema,
                "createAt": block.createAt,
                "updateAt": block.updateAt,
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
            teamId=header.get("teamId", ""),
            channelId="",
            type=header.get("type_flag", "P"),
            title=header.get("title", "Imported"),
            description=header.get("description", ""),
            icon=header.get("icon", ""),
            showDescription=header.get("showDescription", False),
            isTemplate=False,
            templateVersion=0,
            minimumRole=header.get("minimumRole", ""),
            createAt=now,
            updateAt=now,
            deleteAt=0,
        )
        self.db.add(board)
        self.db.flush()

        for line in lines[1:]:
            item = json.loads(line)
            if item.get("type") == "block":
                block = Block(
                    id=item.get("id", ""),
                    boardId=board.id,
                    parentId=item.get("parentId", ""),
                    createdBy=user_id,
                    modifiedBy=user_id,
                    type=item.get("type_flag", "text"),
                    title=item.get("title", ""),
                    fields=item.get("fields", {}),
                    schema=item.get("schema", 1),
                    createAt=item.get("createAt", now),
                    updateAt=now,
                    deleteAt=0,
                )
                self.db.add(block)

        self.db.commit()
        self.db.refresh(board)
        return board
