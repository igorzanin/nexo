# screens — componentes

> Spec de interface dos componentes de UI pertencentes à unit `componentes` (`webapp/src/components`).
> Gerado por: reversa-visor
> Atualizado em: 2026-05-24 (6 novos componentes adicionados)

---

## Componente 1 — Card Detail Modal

**Screenshot:** `screenshots/card-detail-modal.png`
**Propósito:** Exibição e edição completa de todos os atributos de um card.
**Estado:** Card preenchido e finalizado (Status: FINALIZADO, % Completo: 100).
**Contexto de uso:** Clique no nome de qualquer card na view tabela ou kanban.

### Header do modal

| Elemento | Tipo | Comportamento |
|---|---|---|
| 📎 Attach | Botão | Anexa arquivos ao card |
| `...` | Menu overflow | Ações adicionais (duplicar, excluir, etc.) |
| ✕ | Botão fechar | Fecha o modal sem salvar |

### Corpo

- **Ícone de tipo** (grande, ex: 🐛 para Bug) — clicável para mudar o ícone.
- **Título** — editável diretamente (campo de texto simples).

### Painel de propriedades

Cada propriedade exibe **rótulo** à esquerda e **valor** à direita (clicável para editar):

| Propriedade | Tipo do valor | Observações |
|---|---|---|
| Status | Tag selecionável | FINALIZADO, EM PROGRESSO, etc. |
| Tipo | Tag selecionável | BUG, HISTÓRIA, ÉPICO, FUNCIONALIDADE, TAREFA |
| Sprint | Tag selecionável | SPRINT 1–N |
| Prioridade | Tag selecionável | P1, P2, P3 |
| Responsável | Texto (username) | Assignee |
| Data alvo | Data | Exibe "Empty" se não preenchida |
| % Completo | Número (0–100) | Percentual de conclusão |
| Created time | Data/hora (read-only) | Gerado automaticamente |
| Created by | Texto (username, read-only) | Gerado automaticamente |
| Categoria | Tag selecionável | COMERCIAL, SISTEMA, ADMINISTRAÇÃO |

**"+ Add a property"** — link para adicionar propriedade customizada ao template do board.

### Área de comentários

- Avatar do usuário + input "Add a comment..." (texto livre, suporta markdown).

### Corpo / Descrição

- Campo de texto livre abaixo dos comentários.
- Suporta texto formatado / markdown.
- Exibe o conteúdo da descrição do card (ex: "Também é necessário entender se há problemas no formulário.").

### Scroll

O modal possui scroll interno, permitindo ver propriedades e conteúdo longos.

---

## Componente 2 — New Card Template Selector

**Screenshot:** `screenshots/new-card-template-selector.png`
**Propósito:** Selecionar o tipo/template ao criar um novo card.
**Estado:** Dropdown aberto.
**Contexto de uso:** Clique na seta ▾ do botão "New" na barra de controles do board.

### Estrutura

**Cabeçalho:** "Select a template"

**Lista de templates (com ícone + nome + `...`):**

| Template | Ícone |
|---|---|
| Tarefa | 📌 |
| História | 📖 |
| Bug | 🐛 |
| Épico | 🏆 |
| Funcionalidade | 🏗️ |
| Empty card | ▪ |
| + New template | + |

- Clique em um template cria um card com as propriedades pré-definidas daquele tipo.
- `...` ao lado de cada template permite editar ou excluir o template.
- "+ New template" abre editor de template customizado.

---

## Componente 3 — Group By Dropdown

**Screenshot:** `screenshots/group-by-dropdown.png`
**Propósito:** Selecionar o campo de agrupamento das colunas (kanban) ou linhas (tabela).
**Estado:** Aberto, opção "Sprint" selecionada (✓).
**Contexto de uso:** Clique em "Group by: \<campo\>" na barra de controles.

### Opções disponíveis

| Campo | Selecionado |
|---|---|
| Status | — |
| Tipo | — |
| Sprint | ✓ |
| Prioridade | — |
| Created By | — |
| Categoria | — |

A opção selecionada recebe um checkmark (✓). A mudança é aplicada imediatamente ao fechar o dropdown.

---

## Componente 4 — Share Board Modal

**Screenshot:** `screenshots/share-board-modal.png`
**Propósito:** Compartilhar o board com membros da equipe e gerar link de acesso interno.
**Estado:** Modal aberto.
**Contexto de uso:** Clique no botão "Share" no canto superior direito do header do board.

### Estrutura

**Título:** "Share Board"

**Busca de pessoas/canais:**
- Input: "Search for people and channels" — autocomplete de usuários e canais.

**Lista de membros:**

| Membro | Papel | Ação |
|---|---|---|
| Everyone at team | None (dropdown) | Alterar permissão do grupo |
| igorzanin @igorzanin (You) | Admin (dropdown) | Alterar papel do usuário |

**Papéis disponíveis (inferido):** None, Viewer, Editor, Admin.

**Share internally:**
- Texto: "Users who have permissions will be able to use this link."
- Input com URL do board (ex: `https://focalboard.fischerzanin.com.br/bn1set5ni63d5iqzr...`)
- Botão **"Copy link"** (copia a URL para a área de transferência).

---

## Componente 5 — Export Dropdown

**Screenshot:** `screenshots/export-dropdown.png`
**Propósito:** Exportar os dados do board em diferentes formatos.
**Estado:** Dropdown aberto.
**Contexto de uso:** Clique em `...` na barra de controles (ao lado do campo "Search cards").

### Opções

| Opção | Comportamento |
|---|---|
| Export to CSV | Baixa todos os cards do board em arquivo `.csv` |
| Export board archive | Baixa o board completo (cards + estrutura) como arquivo de archive |

---

## Componente 6 — Settings App Menu

**Screenshot:** `screenshots/settings-app-menu.png`
**Propósito:** Acesso rápido a importação, exportação, preferências de idioma, tema e configurações gerais do aplicativo.
**Estado:** Menu aberto (dropdown escuro).
**Contexto de uso:** Clique em "Settings" no rodapé da sidebar ou via atalho de contexto.

### Itens do menu

| Item | Tipo | Comportamento |
|---|---|---|
| Import | Item com submenu ▶ | Abre opções de importação (Trello, Asana, etc.) |
| Export archive | Item | Exporta backup do app inteiro |
| Set language | Item com submenu ▶ | Seleciona idioma da interface |
| Set theme | Item com submenu ▶ | Seleciona tema visual (claro/escuro) |
| Random icons | Toggle (ligado 🔵) | Habilita/desabilita ícones aleatórios nos boards |
| Settings | Rodapé / link | Abre página de configurações avançadas |

---

## Componente 7 — Create a Board Modal

**Screenshot:** `screenshots/create-board-modal.png`
**Propósito:** Criar um novo board a partir de um template existente ou em branco.
**Estado:** Modal aberto, template "Meeting Agenda" selecionado.
**Contexto de uso:** Clique em "+ Add board" no rodapé da sidebar.

### Estrutura

**Título:** "Create a board"
**Subtítulo:** "Add a board to the sidebar using any of the templates defined below or start from scratch."

**Painel esquerdo — lista de templates (scrollável):**

| Template | Ícone |
|---|---|
| + Create new template | + |
| Meeting Agenda | 🔴 |
| Sales Pipeline CRM | ✏️ |
| Personal Tasks | ✅ |
| Project Tasks | 🔵 |
| Company Goals & OKRs | 🌱 |
| Personal Goals | ⭐ |
| Sprint Planner | 📋 |
| User Research Sessions | 👤 |
| Competitive Analysis | 🟡 |
| Content Calendar | 📅 |
| Team Retrospective | 🔄 |
| Roadmap | 📘 |
| *(scroll para mais)* | |

**Painel direito — preview do template selecionado:**
- Nome e descrição textual do template.
- Miniatura interativa do board (mostra colunas e cards de exemplo).
- Exemplo do "Meeting Agenda": colunas "To Discuss" (2), "Revisit Later" (1), "Done / Archived" (1), "+ Add a group".

**Rodapé:**
- **"Create an empty board"** — botão outline, cria board em branco sem template.
- **"Use this template"** — botão primário azul, cria board com o template selecionado.

---

## Componente 8 — Properties Panel (visibilidade de colunas)

**Screenshot:** `screenshots/properties-panel.png`
**Propósito:** Controlar quais colunas/propriedades são exibidas na view de tabela ou kanban.
**Estado:** Painel aberto; Status, Sprint e Prioridade habilitados (🔵); demais desabilitados (⚪).
**Contexto de uso:** Clique no botão "Properties" na barra de controles do board.

### Estrutura

**Aba ativa:** "Properties" (aba lateral "Group by: Sprint" também visível, indicando as duas abas do painel).

**Lista de propriedades com toggle (ligado 🔵 / desligado ⚪):**

| Propriedade | Estado padrão visível |
|---|---|
| Status | 🔵 Ligado |
| Tipo | ⚪ Desligado |
| Sprint | 🔵 Ligado |
| Prioridade | 🔵 Ligado |
| Responsável | ⚪ Desligado |
| Data alvo | ⚪ Desligado |
| % Completo | ⚪ Desligado |
| Created Time | ⚪ Desligado |
| Created By | ⚪ Desligado |
| Categoria | ⚪ Desligado |
| Comments and description | ⚪ Desligado |

Cada toggle altera imediatamente a visibilidade da coluna correspondente na view ativa.

---

## Componente 9 — Sidebar Category Context Menu

**Screenshot:** `screenshots/sidebar-category-context-menu.png`
**Propósito:** Gerenciar categorias (workspaces/grupos) de boards na sidebar.
**Estado:** Menu de contexto aberto sobre a categoria "HUMANART".
**Contexto de uso:** Clique em `...` ao lado do nome de uma categoria na sidebar (visível ao passar o mouse).

### Opções

| Opção | Ícone | Comportamento |
|---|---|---|
| Rename Category | ✏️ | Renomeia a categoria inline |
| Delete Category | 🗑️ | Remove a categoria (e move boards para outra) |
| Create New Category | 📁 | Cria uma nova categoria na sidebar |

### Sidebar visível no contexto

Mostra a estrutura do workspace HUMANART com o board "Humanart 3.0" expandido, exibindo as views:
- Por categoria
- Por Sprint
- Por Sprint Kanban

---

## Componente 10 — Set Theme Submenu

**Screenshot:** `screenshots/set-theme-submenu.png`
**Propósito:** Selecionar o tema visual da interface.
**Estado:** Submenu aberto, "Default theme" selecionado (✓).
**Contexto de uso:** Menu de Configurações → "Set theme ▶".

### Opções

| Tema | Selecionado |
|---|---|
| Default theme | ✓ |
| Dark theme | — |
| Light theme | — |
| System theme | — |

A seleção é aplicada imediatamente à interface.

---

## Componente 11 — Set Language Submenu

**Screenshot:** `screenshots/set-language-submenu.png`
**Propósito:** Selecionar o idioma da interface do Focalboard.
**Estado:** Submenu aberto, "English" selecionado (✓).
**Contexto de uso:** Menu de Configurações → "Set language ▶".

### Idiomas disponíveis

| Idioma | Selecionado |
|---|---|
| English | ✓ |
| Español | — |
| Deutsch | — |
| 日本語 | — |
| Français | — |
| Nederlands | — |
| Русский | — |
| 中文 (繁體) | — |
| 中文 (简体) | — |
| Türkçe | — |
| Occitan | — |
| Português (Brasil) | — |
| Català | — |
| Ελληνικά | — |
| bahasa Indonesia | — |
| Italiano | — |
| Svenska | — |

### Sidebar visível no contexto

Workspace HUMANART → Humanart 3.0 com as views:
- Por categoria
- Por Sprint
- Por Sprint Kanban
- Por Status
- Por Tipo

> **Observação:** confirma que o board "Humanart 3.0" possui 5 sub-views: Por categoria, Por Sprint, Por Sprint Kanban, Por Status, Por Tipo.

---

## Componente 12 — User Account Dropdown

**Screenshot:** `screenshots/user-account-dropdown.png`
**Propósito:** Acesso às ações de conta do usuário logado.
**Estado:** Dropdown aberto.
**Contexto de uso:** Clique no logo/nome do app "Focalboard" no canto superior esquerdo da sidebar.

### Estrutura

**Cabeçalho:** username do usuário logado (ex: "igorzanin") — somente leitura.

**Ações:**

| Item | Comportamento |
|---|---|
| Log out | Encerra a sessão e redireciona para a tela de login |
| Change password | Abre formulário para troca de senha |
| Invite users | Abre formulário para convidar novos usuários |
| About Focalboard | Exibe modal com informações da versão e licença |
