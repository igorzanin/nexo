# ADR-003: Custom property-based status (em vez de estado fixo)

> 🟢 CONFIRMADO — Extraído diretamente do código

## Status

Aceito (implementado)

## Contexto

Ferramentas de gerenciamento de projeto tipicamente têm fluxos de trabalho (workflows) com estados fixos (To Do → In Progress → Done). O sistema precisa decidir se implementa um workflow rígido ou permite que cada board defina seus próprios status.

## Decisão

**Não implementar uma máquina de estados fixa.** Em vez disso, o "Status" é uma propriedade de card do tipo `select` configurável por board:

- Todo board novo recebe automaticamente uma propriedade `Status` do tipo `select` sem opções (`createBoard` em `board.ts:102`)
- O usuário define as opções de status (ex: "To Do", "In Progress", "Done") como options da propriedade select
- Não há transições forçadas entre valores — o usuário simplesmente altera o valor da propriedade
- O sistema de filtros (`FilterClause`) permite filtrar cards por qualquer valor de propriedade, incluindo Status

## Alternativas consideradas

- **Workflow fixo com transições (To Do → In Progress → Done)**: rejeitado por limitar casos de uso (nem todo board usa kanban, alguns querem status diferentes)
- **Workflow configurável com regras de transição**: rejeitado por complexidade de implementação e UX

## Consequências

- Status é altamente flexível: cada board pode ter seu próprio conjunto de status
- Não há validação de transições: um card pode ir de "Done" para "To Do" sem restrições
- Relatórios e automações baseados em status precisam ser genéricos (baseados em propriedades)
- Simplicidade de implementação: o status é apenas mais uma propriedade no sistema de properties
