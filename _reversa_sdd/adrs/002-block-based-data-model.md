# ADR-002: Block-based data model

> 🟢 CONFIRMADO — Extraído do código legado, mantido no Nexo

## Status

Mantido (sem alterações do legado).

## Decisão

O modelo de dados baseado em blocos (Block como entidade universal, Board/Card/View como subtipos) é mantido integralmente no Nexo. É o core do modelo de dados e não há razão para alterá-lo.

O Block usa **Single Table Inheritance** no SQLAlchemy (tabela única `blocks` com coluna `type`), mesma estratégia do legado.

## Consequências

- SQLAlchemy model `Block` com `type` Column(Enum)
- Pydantic schemas para validação
- 15 tipos de Block no servidor, 16 no frontend
