# ADR-004: Soft-delete with history tables

> 🟢 CONFIRMADO — Extraído diretamente do código

## Status

Aceito (implementado)

## Contexto

O sistema precisa permitir undelete de entidades (boards, cards, comentários), manter trilha de auditoria de deleções e suportar compliance/exportação de dados históricos.

## Decisão

Implementar soft-delete com **tabelas de histórico paralelas**:

1. **Tabelas ativas:** armazenam registros correntes (`blocks`, `boards`)
2. **Tabelas de histórico:** armazenam registros deletados com timestamp de deleção (`blocks_history`, `boards_history`, `board_members_history`)
3. **Campo `deleteAt`:** `0` = ativo, `> 0` = timestamp de deleção em milissegundos

**Fluxo de deleção:**
```
DELETE → INSERT INTO history (com deleteAt=now) → DELETE FROM active table
```

**Fluxo de restauração:**
```
UNDELETE → SELECT FROM history → INSERT INTO active (com deleteAt=0) → DELETE FROM history
```

Entidades com suporte:
- Blocks: deleção recursiva de filhos, re-inserção em lote
- Boards: deleção em cascata (blocks, memberships)
- Categories, Subscriptions: soft-delete via UPDATE (sem history table)
- FileInfo: update do campo DeleteAt

## Alternativas consideradas

- **Hard-delete puro**: inviável para compliance e undelete
- **Soft-delete apenas com coluna deleteAt (sem history)**: escalabilidade problemática — a tabela ativa acumularia registros deletados indefinidamente
- **Event sourcing**: complexidade desnecessária para o domínio

## Consequências

- Undelete possível para todas as entidades principais
- Trilha de auditoria completa com timestamp de deleção
- Performance de queries limpa (tabelas ativas enxutas)
- Duplicação de schema entre tabelas ativas e de histórico
- Necessidade de coordenar deleção em cascata manualmente no código
