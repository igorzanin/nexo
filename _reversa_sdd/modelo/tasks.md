# Modelo, Tarefas de Implementação

## Pré-requisitos
- [ ] Python 3.12+ configurado
- [ ] SQLAlchemy 2.0+ instalado
- [ ] Alembic configurado

## Tarefas

- [ ] T-01, Implementar SQLAlchemy models (Board, Block, Card, User, Team, Session, Category, Subscription, Sharing)
  - Fonte legado: `server/model/*.go`
  - Critério: Todos os modelos com relacionamentos, indexes e constraints

- [ ] T-02, Implementar Python Enums (BlockType, BoardType, MemberRole, PropertyType, FilterCondition, BoardMemberRole)
  - Fonte legado: `server/model/block.go`, `server/model/board.go`
  - Critério: Enums com 18 PropertyTypes, 16 BlockTypes, 15 FilterConditions

- [ ] T-03, Implementar Pydantic schemas (create, update, response) para cada modelo
  - Fonte legado: `server/model/*.go` DTOs
  - Critério: Schemas com validação de campos (title ≤ 16383 runes, fields ≤ 800000 runes)

- [ ] T-04, Implementar validadores Pydantic (@field_validator) para regras de negócio
  - Fonte legado: `server/model/*.go` métodos IsValid()
  - Critério: Board type válido, Block title/fields limits, Card icon ≤ 1 grafema

- [ ] T-05, Criar migration inicial Alembic
  - Fonte legado: `server/services/store/sqlstore/migrations/000001_init.up.sql`
  - Critério: Migration cria todas as tabelas; downgrade funcional

## Lacunas
- Nenhuma — comportamento extraído do código legado e adaptado para SQLAlchemy
