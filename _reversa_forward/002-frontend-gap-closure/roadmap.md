# Roadmap: Fechamento de lacunas do frontend

> Identificador: `002-frontend-gap-closure`
> Data: `2026-05-14`
> Requirements: `_reversa_forward/002-frontend-gap-closure/requirements.md`
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA

## 1. Resumo da abordagem

Implementação em 5 módulos na ordem: **Kanban → Table → Calendar → Card Detail → Demais**. Cada módulo recebe as funcionalidades faltantes para atingir paridade com o legado. Nenhuma alteração no backend. Abordagem híbrida (Bootstrap 5.3 + JS custom) e click-to-edit para conteúdo. Undo/redo via estensão do Mutator com `[updatePatch, undoPatch]`.

## 2. Princípios aplicados

Nenhum arquivo `.reversa/principles.md` encontrado. Nenhum princípio a verificar.

## 3. Decisões técnicas

| ID | Decisão | Justificativa | Alternativas descartadas | Confidência |
|----|---------|----------------|--------------------------|-------------|
| D-01 | Mutator estendido com undo/redo via `createPatchesFromBlocks` | Decisão do usuário. Mesmo padrão do legado: cada mutação gera `[updatePatch, undoPatch]` | Pilha simples em memória (perde histórico ao recarregar) | 🟢 |
| D-02 | Kanban DnD apenas entre colunas, sem reordenação de colunas | Decisão do usuário. Reduz complexidade inicial | Reordenação de colunas + criação via drag | 🟢 |
| D-03 | Editor de conteúdo click-to-edit (como legado) | Decisão do usuário. Bloco vira editável ao clicar, salva no blur | Toolbar fixa, modo edição/visualização | 🟢 |
| D-04 | Ordem por módulo: Kanban → Table → Calendar → Card Detail → demais | Decisão do usuário. Kanban é a view mais usada | Por prioridade MoSCoW, por camada | 🟢 |
| D-05 | Filtros usam BoardView.fields.filter com árvore FilterGroup/FilterClause | Mecanismo existente no backend e tipos TypeScript já implementados | Estado local no componente | 🟢 |
| D-06 | Cálculos usam composable `useCalculations` existente, add display UI | Já implementado, só falta UI | Reimplementar do zero | 🟢 |

## 4. Premissas

Nenhuma dúvida pendente. Todas validadas na sessão de esclarecimentos.

## 5. Delta arquitetural

| Componente | Arquivo de origem | Tipo de mudança | Resumo |
|------------|-------------------|-----------------|--------|
| Kanban | `webapp/src/components/kanban/` | regra-alterada | Adicionar DnD cards entre colunas, cálculos no header, badges nos cards |
| Table | `webapp/src/components/table/` | regra-alterada | Adicionar agrupamento de linhas, resize de colunas, header menu, cálculos |
| Calendar | `webapp/src/components/calendar/Calendar.vue` | regra-alterada | Substituir grid simples por FullCalendar com navegação mês/semana/dia |
| Card Detail | `webapp/src/components/cardDetail/` | regra-alterada | Adicionar editor de blocos (CRUD), content add menu, attachment upload, image paste |
| Properties | `webapp/src/components/properties/` | componente-novo | Adicionar 8 property editors faltantes |
| ViewHeader | `webapp/src/components/common/` | regra-alterada | Adicionar UI de filtros completa, view switcher, view menu |
| Widgets | `webapp/src/components/widgets/` | componente-novo | Adicionar Modal/Dialog genérico, PropertyMenu, ValueSelector, etc. |
| Mutator | `webapp/src/composables/useMutator.ts` | regra-alterada | Estender com geração de patches undo/redo |
| Stores | `webapp/src/stores/` | regra-alterada | Adicionar integração undo stack com mutations |

## 6. Delta no modelo de dados

- Resumo das mudanças: Nenhuma mudança no backend. Frontend adiciona/edit tipos relacionados a filtros e cálculos, mas tudo já existe nos tipos TypeScript.
- Detalhe completo em: `_reversa_forward/002-frontend-gap-closure/data-delta.md`

## 7. Delta de contratos externos

Nenhum contrato externo afetado. Mesmos endpoints da API existente.

## 8. Plano de migração

n/a — Implementação incremental. Componentes novos são adicionados sem remover existentes.

## 9. Riscos e mitigações

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| Editor de conteúdo pode exigir mudanças na API para upload de arquivos | médio | médio | Verificar se endpoint de upload já existe no backend |
| FullCalendar pode conflitar com Bootstrap CSS | médio | baixo | Testar integração em ambiente dev |
| Undo/redo via patches pode ser complexo de integrar com todas as stores | médio | médio | Implementar gradualmente, começando por boardStore |

## 10. Critério de pronto

- [ ] Kanban: DnD entre colunas, cálculos, badges funcionando
- [ ] Table: agrupamento, resize, header menu, cálculos funcionando
- [ ] Calendar: FullCalendar com navegação e criação por clique
- [ ] Card Detail: editor de blocos CRUD, upload de anexo, paste de imagem
- [ ] 8 property editors faltantes implementados
- [ ] Filtros: UI completa no ViewHeader
- [ ] View menu: renomear, duplicar, deletar views
- [ ] Undo/redo integrado com Mutator
- [ ] Modal/Dialog genérico implementado
- [ ] Cross-check via `/reversa-audit` sem CRITICAL nem HIGH

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-05-14 | Versão inicial gerada por `/reversa-plan` | reversa |
