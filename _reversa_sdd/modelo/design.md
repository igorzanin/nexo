# Modelo, Design Técnico

## Stack

| Componente | Tecnologia |
|------------|-----------|
| ORM | SQLAlchemy 2.0 (Declarative Base) |
| Validação | Pydantic v2 (BaseModel) |
| Migrations | Alembic |
| Enum | Python Enum + SQLAlchemy Enum |
| UUID | `uuid.uuid4()` |

## SQLAlchemy Models

### Board

```python
class Board(Base):
    __tablename__ = "boards"
    id = Column(String(36), primary_key=True, default=uuid4_str)
    team_id = Column(String(36), ForeignKey("teams.id"), nullable=False)
    type = Column(Enum(BoardType), nullable=False, default=BoardType.PRIVATE)
    title = Column(String(1024), default="")
    description = Column(Text, default="")
    show_description = Column(Boolean, default=False)
    icon = Column(String(32), default="")
    channel_id = Column(String(36), default="")
    minimum_role = Column(Enum(MemberRole), default=MemberRole.NONE)
    is_template = Column(Boolean, default=False)
    template_version = Column(Integer, default=0)
    card_properties = Column(JSON, default=list)
    create_at = Column(BigInteger, default=current_timestamp)
    update_at = Column(BigInteger, default=current_timestamp, onupdate=current_timestamp)
    delete_at = Column(BigInteger, default=0)
```

### Block (Single Table Inheritance)

```python
class Block(Base):
    __tablename__ = "blocks"
    id = Column(String(36), primary_key=True, default=uuid4_str)
    board_id = Column(String(36), ForeignKey("boards.id"), nullable=False)
    parent_id = Column(String(36), default="")
    type = Column(Enum(BlockType), nullable=False)
    title = Column(Text, default="")
    fields = Column(JSON, default=dict)
    create_at = Column(BigInteger, default=current_timestamp)
    update_at = Column(BigInteger, default=current_timestamp, onupdate=current_timestamp)
    delete_at = Column(BigInteger, default=0)
```

### Card (extends Block via type='card')

```python
class Card:
    """Card é um Block com type='card' + campos específicos em fields"""
    # fields: {icon, isTemplate, properties: {}, contentOrder: []}
```

### Pydantic Schemas

```python
class BoardCreate(BaseModel):
    team_id: str
    type: BoardType = BoardType.PRIVATE
    title: str = ""
    description: str = ""
    # ...

class BoardResponse(BaseModel):
    id: str
    team_id: str
    type: BoardType
    title: str
    # ...
    model_config = ConfigDict(from_attributes=True)

class BlockCreate(BaseModel):
    board_id: str
    parent_id: str = ""
    type: BlockType
    title: str = ""
    fields: dict = {}
```

## BlockType Enum

```python
class BlockType(str, Enum):
    BOARD = "board"
    CARD = "card"
    VIEW = "view"
    COMMENT = "comment"
    ATTACHMENT = "attachment"
    TEXT = "text"
    IMAGE = "image"
    DIVIDER = "divider"
    CHECKBOX = "checkbox"
    HEADING1 = "heading1"
    HEADING2 = "heading2"
    HEADING3 = "heading3"
    VIDEO = "video"
    QUOTE = "quote"
    LIST_ITEM = "listItem"
```

## Fluxo Principal

1. FastAPI router recebe payload JSON → valida com Pydantic schema 🟢
2. Service layer chama validações de negócio 🟢
3. SQLAlchemy model é criado e persistido via repositório 🟢
4. Pydantic schema serializa resposta 🟢
