# screens — paginas

> Spec de interface das telas pertencentes à unit `paginas` (`webapp/src/pages`).
> Gerado por: reversa-visor

---

## Tela 1 — Board Table: Por Sprint

**Screenshot:** `screenshots/board-table-por-sprint.png`
**Propósito:** Visualização tabular de um board agrupado por Sprint.
**Estado:** Preenchido (24 cards visíveis, dois sprints expandidos).
**Contexto de uso:** Usuário acessa o board e seleciona a view "Por Sprint" na sidebar ou via seletor de view na barra superior.

### Sidebar (painel esquerdo)

| Elemento | Tipo | Comportamento |
|---|---|---|
| Focalboard v7.11.4 | Logo + versão | Clicável (home/refresh) |
| `<<` (recolher) | Botão ícone | Colapsa a sidebar |
| Find boards | Input de busca | Filtra boards da lista |
| BOARDS | Seção colapsável | Boards sem workspace |
| BLISSYS | Seção expandida | Workspace "Blissys" |
| ↳ Sprint Blissys | Board ativo | Selecionado (destaque azul) |
| ↳↳ Por Sprint | Sub-view (tabela) | Ativa (negrito) |
| ↳↳ Por Status | Sub-view (kanban) | — |
| ↳↳ Por Tipo | Sub-view | — |
| ↳↳ Sprint Kanban | Sub-view (kanban) | — |
| ↳↳ Metas Blisterpack | Sub-view | — |
| KAHUN | Seção | Workspace "Kahun" |
| ↳ Objetivos e entregas | Board | — |
| HUMANART | Seção | Workspace "Humanart" |
| ↳ Humanart 3.0 | Board | — |
| BOARDS | Seção | Boards avulsos |
| + Add board | Botão | Abre modal "Create a board" |
| Settings | Link | Abre menu de configurações do app |

### Barra de controles

| Elemento | Tipo | Comportamento |
|---|---|---|
| "Por Sprint" ▾ | Dropdown de views | Troca a view ativa |
| Properties | Botão | Gerencia colunas visíveis |
| Group by: Sprint | Dropdown | Escolhe campo de agrupamento |
| Filter | Botão | Abre painel de filtros |
| Sort | Botão | Abre painel de ordenação |
| Search cards | Input | Filtra cards em tempo real |
| `...` | Menu overflow | Exportar (CSV / archive) |
| New ▾ | Botão primário (split) | Cria card; seta abre template selector |
| Give feedback | Link | Feedback externo |
| Share | Botão primário | Abre modal "Share Board" |

### Tabela

**Colunas visíveis:** Name, Status, Categoria, Tipo, Sprint, Prioridade, Responsável, Data alvo, % Completo, Created time, Created by.

**Grupos (linhas de cabeçalho colapsáveis):**
- Sprint 1 — 8 cards
- Sprint 2 — 9 cards (mais, com scroll)

**Rodapé:** `COUNT 24` (total de cards no board).

### Tags de Status

| Tag | Cor | Significado |
|---|---|---|
| FINALIZADO ✨ | Verde | Concluído |
| EM PROGRESSO | Azul | Em desenvolvimento |
| PRÓXIMO NA FILA | Laranja claro | Pronto para iniciar |
| SUSPENSO | Vermelho | Bloqueado / pausado |
| NÃO INICIADO | Cinza | Backlog |

### Tags de Tipo

| Tag | Ícone | Cor |
|---|---|---|
| BUG | 🐛 | Vermelho claro |
| HISTÓRIA | 📖 | Azul claro |
| ÉPICO | 🏆 | Amarelo |
| FUNCIONALIDADE | 🏗️ | Laranja |
| TAREFA | — | Cinza |

### Tags de Categoria

| Tag | Ícone | Cor |
|---|---|---|
| COMERCIAL | 🏪 | Amarelo |
| SISTEMA | 🖥️ | Verde |
| ADMINISTRAÇÃO | 📋 | Roxo |

### Tags de Sprint

`SPRINT 1`, `SPRINT 2`, `SPRINT 3`, `SPRINT 4` — badges coloridas (azul/verde/roxo/amarelo).

### Prioridade

Valores: `P1`, `P2`, `P3` — exibidos como texto simples.

---

## Tela 2 — Board Kanban: Por Status

**Screenshot:** `screenshots/board-kanban-por-status.png`
**Propósito:** Visualização kanban do board Sprint Blissys agrupada por Status.
**Estado:** Preenchido (24 cards distribuídos nas colunas).
**Contexto de uso:** Usuário seleciona "Por Status" na sidebar, ou muda o "Group by" para Status na barra de controles.

### Colunas Kanban

| Coluna | Contagem | Cor do cabeçalho |
|---|---|---|
| Não iniciado | 9 | Cinza claro |
| Próximo na fila | 2 | Laranja claro |
| Em progresso | 2 | Azul |
| Suspenso | 0 | Vermelho |
| Finalizado ✨ | 11 | Verde |
| Hidden columns | — | — |
| No Status | 0 | Cinza |

**Ações do cabeçalho de coluna:** `...` (renomear / excluir coluna) e `+` (novo card nesta coluna).

### Cards Kanban

Cada card exibe:
- Ícone de tipo + título
- Badge de Tipo (BUG, HISTÓRIA, ÉPICO, FUNCIONALIDADE)
- Badge de Sprint
- Badge de Prioridade (P1/P2/P3)

**Botão `+ New`** no rodapé de cada coluna cria card com o status da coluna pré-preenchido.

### Diferenças em relação à view tabela

- Layout visual em colunas (Kanban) em vez de linhas
- Group by muda de "Sprint" para "Status"
- Colunas representam cada valor de Status
- Colunas podem ser reordenadas, renomeadas ou ocultadas ("Hidden columns")
