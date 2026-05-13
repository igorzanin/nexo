# ADR-006: Multi-database support (SQLite, PostgreSQL, MySQL, MariaDB)

> 🟢 CONFIRMADO — Extraído diretamente do código

## Status

Aceito (implementado)

## Contexto

O sistema precisa funcionar em diferentes cenários de deployment:
- **Desktop single-user:** SQLite embutido (simplicidade)
- **Servidor standalone:** SQLite (dev) ou PostgreSQL/MySQL (produção)
- **Plugin Mattermost:** banco PostgreSQL do Mattermost
- **Testes de integração:** todos os 4 bancos

## Decisão

Suportar quatro bancos de dados com:
- **SQL builder:** `squirrel` para queries genéricas (abstrai diferenças de sintaxe)
- **Drivers:** `go-sqlite3`, `lib/pq`, `go-sql-driver/mysql` para cada banco
- **SQLx:** para mapeamento row→struct
- **Mattermost Morph:** framework de migrações com 40 migrações, cada uma testada nos 4 bancos
- **Placeholders:** `{{.prefix}}` para schema de plugin vs standalone, `{{db_specific}}` para diferenças de DDL
- **Testes:** `make server-test` roda suite contra SQLite, MySQL, MariaDB e PostgreSQL em docker

## Alternativas consideradas

- **Apenas PostgreSQL**: rejeitado, pois SQLite é necessário para modo desktop standalone
- **ORM completo (GORM, Ent)**: rejeitado por preferir controle fino sobre SQL e performance
- **Apenas SQLite**: inviável para produção multi-usuário

## Consequências

- 4 combinações de banco para testar a cada release
- SQL builder squirrel reduz mas não elimina necessidade de SQL específico por banco
- Migrações precisam ser compatíveis com todos os bancos (uso de `{{db_specific}}` para diferenças)
- Performance de SQLite é limitante em cenários multi-usuário
- Código de store com branches `if s.dbType == mysql { ... }` ocasionais
