# Requirements: Fechamento de lacunas do frontend

> Identificador: `002-frontend-gap-closure`
> Data: `2026-05-14`
> Pasta da extração reversa: `_reversa_sdd/`
> Fonte legado: `focalboard-legacy/webapp/src/`
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA / DÚVIDA

## 1. Resumo executivo

Implementar todas as funcionalidades do frontend legado do Focalboard que ainda não foram transcritas para o novo sistema Vue 3 + Bootstrap 5.3. Isso cobre edição de conteúdo de card, sistema de filtros, drag-and-drop, cálculos de coluna, gerenciamento de views, agrupamento de linhas, editors de propriedade faltantes, calendário completo, badges, archive de board, undo/redo, resize de colunas, switcher de visualização e widgets ausentes. O entregável é um frontend com paridade funcional de 100% com o legado.

## 2. Contexto a partir do legado

| Fonte | Trecho relevante | Confidência |
|-------|------------------|-------------|
| `_reversa_sdd/frontend-inventory.md` | Inventário completo com 92 componentes legados vs ~47 novos | 🟢 |
| `_reversa_sdd/componentes/requirements.md` | Regras atuais do frontend Vue 3 | 🟢 |
| `focalboard-legacy/webapp/src/components/blocksEditor/` | 14 arquivos de editor de blocos de conteúdo | 🟢 |
| `focalboard-legacy/webapp/src/components/viewHeader/` | 35 arquivos de header com filtros, search, menus | 🟢 |
| `focalboard-legacy/webapp/src/components/calculations/` | 8 arquivos de cálculos de coluna | 🟢 |
| `focalboard-legacy/webapp/src/components/kanban/` | 15 arquivos Kanban (DnD, collapse, cálculos, badges) | 🟢 |
| `focalboard-legacy/webapp/src/components/table/` | 22 arquivos Table (group, resize, headerMenu) | 🟢 |
| `focalboard-legacy/webapp/src/components/calendar/` | 4 arquivos Calendar (FullCalendar) | 🟢 |
| `focalboard-legacy/webapp/src/properties/` | 19 property editors legados, 11 implementados | 🟢 |
| `focalboard-legacy/webapp/src/widgets/` | 30 widgets legados, 7 implementados | 🟢 |

## 3. Personas e cenários de uso

| Persona | Objetivo | Cenário-chave |
|---------|----------|---------------|
| Usuário de board | Editar conteúdo do card | Abrir card, adicionar bloco de texto, editar markdown, enviar imagem |
| Usuário de kanban | Arrastar cards entre colunas | Mover card de "To Do" para "In Progress" via drag-and-drop |
| Gerente de projeto | Filtrar board por status/data | Adicionar filtro "Status = Done" + "Due Date < this week" |
| Visualizador de dados | Ver cálculos de coluna | Ver contagem de cards, soma de horas na tabela |
| Administrador | Exportar board como archive | Exportar board completo para arquivo .boardarchive |

## 4. Regras de negócio novas ou alteradas

1. **RN-01:** Content blocks podem ser adicionados, editados, reordenados e deletados dentro do CardDialog, via ContentRegistry com suporte a edit mode. 🟢
   - Fonte: `focalboard-legacy/webapp/src/components/blocksEditor/`
   - Tipo: nova

2. **RN-02:** Todo filtro aplicado a uma view deve ser persistido no campo `fields.filter` do BoardView, usando árvore FilterGroup/FilterClause. 🟢
   - Fonte: `focalboard-legacy/webapp/src/components/viewHeader/filterComponent.tsx`
   - Tipo: nova

3. **RN-03:** Cálculos de coluna (count, sum, avg, min, max) devem ser exibidos no header de cada coluna do Kanban e no footer da Table. 🟢
   - Fonte: `focalboard-legacy/webapp/src/components/calculations/`
   - Tipo: nova

4. **RN-04:** Views podem ser renomeadas, duplicadas e deletadas via menu no ViewHeader. 🟢
   - Fonte: `focalboard-legacy/webapp/src/components/viewHeader/viewMenu.tsx`
   - Tipo: nova

5. **RN-05:** Tabela suporta agrupamento de linhas por propriedade com group headers colapsáveis. 🟢
   - Fonte: `focalboard-legacy/webapp/src/components/table/tableGroup.tsx`
   - Tipo: nova

6. **RN-06:** Tabela suporta redimensionamento de colunas via arraste horizontal grip. 🟢
   - Fonte: `focalboard-legacy/webapp/src/components/table/horizontalGrip.tsx`
   - Tipo: nova

## 5. Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de aceite | Confidência |
|----|-----------|------------|--------------------|-------------|
| RF-01 | Implementar editor de blocos de conteúdo no CardDialog: adicionar, editar, reordenar e deletar blocos de texto, imagem, checkbox, divisor, h1-h3, anexo | Must | Usuário pode adicionar bloco de texto, digitar conteúdo, salvar; blocos podem ser reordenados via drag | 🟢 |
| RF-02 | Implementar UI de filtros no ViewHeader: adicionar/editar/remover filtros por propriedade, com suporte a FilterGroup (and/or) | Must | Usuário pode adicionar filtro "Status = Done", board filtra cards; filtro persiste ao recarregar | 🟢 |
| RF-03 | Implementar drag-and-drop de cards entre colunas no Kanban | Must | Card pode ser arrastado de uma coluna para outra; propriedade de status é atualizada. Sem reordenação de colunas | 🟢 |
| RF-04 | Implementar exibição de cálculos de coluna (count, sum, avg, min, max) no Kanban e Table | Should | Header de coluna Kanban mostra contagem; Table mostra soma no footer | 🟢 |
| RF-05 | Implementar gerenciamento de views: renomear, duplicar, deletar via menu no ViewHeader | Should | Usuário pode renomear view inline, duplicar com novo ID, deletar com confirmação | 🟢 |
| RF-06 | Implementar agrupamento de linhas na Table View | Should | Tabela agrupa linhas por propriedade selecionada; grupos são colapsáveis | 🟢 |
| RF-07 | Implementar redimensionamento de colunas na Table View | Could | Usuário pode arrastar borda do header para redimensionar coluna | 🟢 |
| RF-08 | Implementar property editors faltantes (8): multiPerson, createdBy, createdTime, updatedBy, updatedTime, unknown, baseTextEditor robusto | Should | Cada property editor renderiza e edita corretamente conforme spec em `_reversa_sdd/properties/` | 🟢 |
| RF-09 | Implementar calendário com FullCalendar: navegação mês/semana/dia, criação de card por clique, drag para reagendar | Should | Usuário pode alternar entre mês/semana/dia, clicar em data para criar card | 🟢 |
| RF-10 | Implementar card badges: contagem de comentários, indicador de descrição, data de vencimento | Could | Card no Kanban/Table mostra badges com info relevante | 🟢 |
| RF-11 | Implementar board archive import/export (boardarchive JSON) | Could | Usuário pode exportar board completo e importar de volta | 🟢 |
| RF-12 | Implementar integração undo/redo com mutações: estender Mutator para gerar `[updatePatch, undoPatch]` em toda operação, alimentando pilha de undo | Should | Ctrl+Z desfaz última mutação (criar/deletar/mover card) via patches | 🟢 |
| RF-13 | Implementar widgets faltantes: EditableArea, EditableDayPicker, GuestBadge, Label, PropertyMenu, ValueSelector, Dialog, Modal genérico | Should | Widgets listados em `_reversa_sdd/widgets/spec-widgets.md` são implementados | 🟢 |
| RF-14 | Implementar switcher de visualização no ViewHeader (display-by menu) | Could | Usuário pode alternar entre Kanban/Table/Calendar/Gallery pelo header | 🟢 |
| RF-15 | Implementar criação de card por template: NewCardButton com template items | Could | Usuário pode criar card a partir de template existente | 🟢 |

## 6. Requisitos Não Funcionais

| Tipo | Requisito | Evidência ou justificativa | Confidência |
|------|-----------|----------------------------|-------------|
| Compatibilidade | Nenhuma mudança no backend API. Frontend consome mesmos endpoints | Feature anterior `001` não alterou backend | 🟢 |
| Performance | Drag-and-drop deve ter latência < 100ms entre ação e feedback visual | Expectativa de UX de planos de quadro | 🟡 |
| Persistência | Filtros, sort e agrupamento persistem via BoardView.fields | Mecanismo existente no backend | 🟢 |

## 7. Critérios de Aceitação

```gherkin
Cenário: Usuário edita bloco de texto no card
  Dado que o CardDialog está aberto para um card
  Quando o usuário clica em "+ Text" e digita "Minha nota"
  Então o bloco de texto aparece no conteúdo do card

Cenário: Usuário filtra board por status
  Dado que existe um board com cards de status "To Do" e "Done"
  Quando o usuário adiciona filtro "Status = Done"
  Então apenas cards "Done" são exibidos

Cenário: Usuário arrasta card entre colunas Kanban
  Dado que o Kanban tem colunas "To Do" e "In Progress"
  Quando o usuário arrasta um card de "To Do" para "In Progress"
  Então o card aparece na coluna "In Progress" e a propriedade de status é atualizada

Cenário: Usuário renomeia view
  Dado que existe uma view "Board view"
  Quando o usuário clica no menu de view e seleciona "Rename"
  Então o título da view fica editável e a mudança persiste
```

## 8. Ordem de implementação

A execução será por **módulo** na ordem: Kanban → Table → Calendar → Card Detail → demais.

## 9. Esclarecimentos

### Sessão 2026-05-14

- **Q:** Qual abordagem para undo/redo no Mutator?
  **R:** Completa — estender o Mutator para gerar `[updatePatch, undoPatch]` em toda operação, como o legado faz com `createPatchesFromBlocks`.

- **Q:** Qual nível de drag-and-drop no Kanban?
  **R:** Cards entre colunas — arrastar cards entre colunas existentes, sem reordenação de colunas.

- **Q:** Qual comportamento de edição de conteúdo de card?
  **R:** Click-to-edit — bloco fica editável ao clicar, salva ao perder foco (como o legado).

- **Q:** Quais widgets prioritários?
  **R:** Modal/Dialog genérico reutilizável primeiro.

- **Q:** Qual ordem de implementação?
  **R:** Por módulo: 1º Kanban, 2º Table, 3º Calendar, 4º Card Detail, 5º demais.

## 10. Lacunas

Resolvidas na sessão de esclarecimentos de 2026-05-14. Nenhuma lacuna pendente.

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-05-14 | Versão inicial gerada por `/reversa-requirements` | reversa |
| 2026-05-14 | Sessão de esclarecimentos: undo/redo via patches, DnD cards entre colunas, click-to-edit, Modal genérico, ordem por módulo | reversa |
