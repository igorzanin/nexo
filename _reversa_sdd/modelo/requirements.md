# Modelo — Entidades de Domínio (SQLAlchemy)

## Visão Geral
Camada de modelos SQLAlchemy ORM que define todas as entidades de domínio do Nexo: Board, Block, Card, User, Team, Category, Session, Subscription, BoardMember e Sharing. Contém classes de modelo, validações, constantes e métodos auxiliares usados por todo o sistema.

## Responsabilidades
- Definição de todas as classes ORM com campos tipados (SQLAlchemy)
- Validação de campos (tamanho, formato, obrigatoriedade) via Pydantic + SQLAlchemy
- Constantes de enum (BlockType, PropertyType, BoardType, etc.) via Python Enum
- Serialização/deserialização JSON via Pydantic schemas
- Lógica de limites (card_limit_timestamp — removido por decisão)

## Regras de Negócio
- Board deve ter TeamID e Type (`O`/`P`) válido 🟢
- Block title máximo: 16383 runes; fields JSON máximo: 800000 runes 🟢
- Card deve ter ID, BoardID, ContentOrder e Properties não-nulo 🟢
- BlockType segue hierarquia: `board`, `card`, `view`, `comment`, `attachment`, `text`, `image`, `divider`, `checkbox`, `heading1-3`, `video`, `quote`, `listItem` 🟢
- BoardMember schemeAdmin/Editor/Commenter/Viewer são mutuamente exclusivos 🟡
- Categoria pode ser `system` ou `custom`; deletada via soft-delete (deleteAt > 0) 🟢
- Subscription requer BlockID, BlockType, SubscriberID e SubscriberType = `"user"` 🟢
- Autenticação via JWT com refresh token 🟢
- Senha mínima: 8 caracteres 🟢

## Stack

| Componente | Tecnologia |
|------------|-----------|
| ORM | SQLAlchemy 2.0+ |
| Validação | Pydantic v2 |
| Migrations | Alembic |
| Enums | Python Enum |
| Serialização | Pydantic schemas (BaseModel) |
| UUID | Python uuid4 |

## Requisitos Funcionais

| ID | Requisito | Prioridade |
|----|-----------|-----------|
| MD-RF01 | SQLAlchemy model Board com campos ID, TeamID, Type, Title, Description, ShowDescription, Icon, ChannelID, MinimumRole, IsTemplate, CardProperties | Must |
| MD-RF02 | SQLAlchemy model Block base polimórfica (single-table ou joined) com 15 campos | Must |
| MD-RF03 | SQLAlchemy model Card com CardFields (icon, isTemplate, properties, contentOrder) | Must |
| MD-RF04 | Enum PropertyType com 18 tipos | Must |
| MD-RF05 | Validar limites de tamanho (title 16383 runes, fields 800000 runes) | Must |
| MD-RF06 | Pydantic schemas para serialização/desserialização JSON | Must |
| MD-RF07 | Alembic migrations para todos os modelos | Must |

## Rastreabilidade

| Entidade | Fonte legado | Confiança |
|---------|-------------|-----------|
| Board | `server/model/board.go` | 🟢 |
| Block | `server/model/block.go` | 🟢 |
| Card | `server/model/card.go` | 🟢 |
| User | `server/model/user.go` | 🟢 |
| Team | `server/model/team.go` | 🟢 |
| Session | `server/model/session.go` | 🟢 |
| Category | `server/model/category.go` | 🟢 |
| Subscription | `server/model/subscription.go` | 🟢 |
| Sharing | `server/model/sharing.go` | 🟢 |
