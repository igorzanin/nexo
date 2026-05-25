---
schemaVersion: 1
generatedAt: 2026-05-24T18:10:00-03:00
reversa:
  version: "1.0.0"
kind: screen_deviation_log
producedBy: screen-translator
mode: append-only
hash: "sha256:screen-translator-deviation-log-nexo"
---

# Screen Deviation Log

> Registro de divergências aceitas entre o legado React + Focalboard CSS e a especificação alvo Vue 3 + Bootstrap 5.3.
> Todas as entradas abaixo já estão aprovadas pelo modo `modernized` explicitamente aceito na Fase 1.

## Convenções

- **ID**: `DEV-NNN`.
- **Tipo**: `tecnica`, `modernizacao`, `plataforma`, `correcao`.
- **Aprovação**: `aprovado` em todas as entradas deste lote.
- **Propagação**: todas as entradas aprovadas devem aparecer em `parity_specs.md § Exceções`.

## Resumo

- **Total**: 9
- **Pendentes**: 0
- **Aprovadas**: 9
- **Rejeitadas**: 0

## Entradas

### DEV-001

| Campo | Valor |
|---|---|
| Tela afetada | `SCR-002 RegisterPage` |
| Tipo | `plataforma` |
| Descrição | `RegisterPage` foi especificada sem screenshot de referência. |
| Motivo | A tela existe no fluxo (`LOGIN -> REGISTER`), mas não foi capturada pelo Visor. Em modo modernizado, a tela pode ser especificada por código legado inferido sem bloquear a tradução. |
| Origem no legado | `webapp/src/pages/register_page.tsx:RegisterPage` |
| Implicação para parity tests | Validar contrato semântico (campos, labels, rota e transições), sem comparação visual. |
| Aprovação | `aprovado` |
| Aprovado por | `igorzanin` |
| Aprovado em | `2026-05-24T18:05:00-03:00` |
| Propaga para `parity_specs.md § Exceções` | sim |

### DEV-002

| Campo | Valor |
|---|---|
| Tela afetada | `SCR-003 HomePage` |
| Tipo | `plataforma` |
| Descrição | `HomePage` foi especificada sem screenshot de referência. |
| Motivo | A home/lista de boards está no fluxo e no inventário pendente, mas não há captura. A spec foi derivada de `flow.md`, `inventory.md` e do comportamento legado inferido. |
| Origem no legado | `webapp/src/pages/board_page.tsx:HomePage / BoardList` |
| Implicação para parity tests | Testar navegação, presença do board list, `+ Add board` e `Settings`; não exigir parity visual. |
| Aprovação | `aprovado` |
| Aprovado por | `igorzanin` |
| Aprovado em | `2026-05-24T18:05:00-03:00` |
| Propaga para `parity_specs.md § Exceções` | sim |

### DEV-003

| Campo | Valor |
|---|---|
| Tela afetada | `SCR-018 ChangePasswordPage` |
| Tipo | `plataforma` |
| Descrição | `ChangePasswordPage` foi especificada sem screenshot de referência. |
| Motivo | A tela aparece no fluxo via `UserAccountDropdown`, porém não foi capturada. A implementação alvo precisa seguir contrato funcional, não comparação visual. |
| Origem no legado | `webapp/src/pages/change_password_page.tsx:ChangePasswordPage` |
| Implicação para parity tests | Cobrir campos obrigatórios, sucesso, erro e retorno ao login/cancelamento. |
| Aprovação | `aprovado` |
| Aprovado por | `igorzanin` |
| Aprovado em | `2026-05-24T18:05:00-03:00` |
| Propaga para `parity_specs.md § Exceções` | sim |

### DEV-004

| Campo | Valor |
|---|---|
| Tela afetada | `SCR-019 FilterPanel` |
| Tipo | `plataforma` |
| Descrição | `FilterPanel` foi especificado sem screenshot de referência. |
| Motivo | O botão `Filter` está presente nas views de board e no fluxo principal, mas o painel não foi capturado. A spec usa a semântica do legado inferido e a estrutura esperada para filtros por propriedade. |
| Origem no legado | `webapp/src/components/viewHeader/filterComponent.tsx:FilterPanel` |
| Implicação para parity tests | Testar composição de filtros, aplicação e limpeza; não comparar pixel a pixel. |
| Aprovação | `aprovado` |
| Aprovado por | `igorzanin` |
| Aprovado em | `2026-05-24T18:05:00-03:00` |
| Propaga para `parity_specs.md § Exceções` | sim |

### DEV-005

| Campo | Valor |
|---|---|
| Tela afetada | `SCR-020 SortPanel` |
| Tipo | `plataforma` |
| Descrição | `SortPanel` foi especificado sem screenshot de referência. |
| Motivo | O botão `Sort` consta no fluxo principal, mas o painel não foi capturado. A tradução foi feita a partir do código legado inferido e do comportamento padrão de ordenação do board. |
| Origem no legado | `webapp/src/components/viewHeader/viewHeaderSortMenu.tsx:SortPanel` |
| Implicação para parity tests | Testar seleção de campos, direção e aplicação da ordenação; sem parity visual. |
| Aprovação | `aprovado` |
| Aprovado por | `igorzanin` |
| Aprovado em | `2026-05-24T18:05:00-03:00` |
| Propaga para `parity_specs.md § Exceções` | sim |

### DEV-006

| Campo | Valor |
|---|---|
| Tela afetada | `SCR-001` a `SCR-020` |
| Tipo | `modernizacao` |
| Descrição | O sistema de estilos legado em Focalboard CSS foi substituído por Bootstrap 5.3 + tokens do design system. |
| Motivo | Esta é a essência do modo `modernized` aprovado. A hierarquia de informação, labels e fluxo foram preservados, mas spacing, grid, shadows, menus e modais passaram a usar primitives Bootstrap idiomáticas do alvo Vue 3. |
| Origem no legado | `screen_modernization_decision.md:Modo modernizado` |
| Implicação para parity tests | Executar parity semântico por estrutura, eventos e conteúdo textual. Não exigir equivalência visual byte-a-byte. |
| Aprovação | `aprovado` |
| Aprovado por | `igorzanin` |
| Aprovado em | `2026-05-24T18:05:00-03:00` |
| Propaga para `parity_specs.md § Exceções` | sim |

### DEV-007

| Campo | Valor |
|---|---|
| Tela afetada | `SCR-001 LoginPage`, `SCR-002 RegisterPage`, `SCR-003 HomePage`, `SCR-011 SettingsAppMenu`, `SCR-017 UserAccountDropdown` |
| Tipo | `correcao` |
| Descrição | Qualquer superfície textual de marca deixa de exibir `Focalboard` e passa a exibir `Nexo`. |
| Motivo | O produto alvo é `Nexo`, não o fork legado. A alteração corrige branding residual do legado sem alterar o fluxo principal. |
| Origem no legado | `paginas/screens.md` e `componentes/screens.md` (branding Focalboard nas capturas e descrições) |
| Implicação para parity tests | Tratar `Nexo` como texto canônico aprovado para branding; não falhar por ausência de `Focalboard`. |
| Aprovação | `aprovado` |
| Aprovado por | `igorzanin` |
| Aprovado em | `2026-05-24T18:05:00-03:00` |
| Propaga para `parity_specs.md § Exceções` | sim |

### DEV-008

| Campo | Valor |
|---|---|
| Tela afetada | `SCR-004 BoardTableView`, `SCR-005 BoardKanbanView` |
| Tipo | `modernizacao` |
| Descrição | O link externo `Give feedback` foi removido da barra de ações do board. |
| Motivo | O link aponta para um fluxo legado externo do Focalboard que não faz parte do produto alvo. A remoção reduz ruído e evita fuga de contexto. |
| Origem no legado | `paginas/screens.md` — barra de controles do board |
| Implicação para parity tests | Não esperar presença de link externo; validar apenas ações funcionais do board (`Properties`, `Group by`, `Filter`, `Sort`, `Share`, `New`, `...`). |
| Aprovação | `aprovado` |
| Aprovado por | `igorzanin` |
| Aprovado em | `2026-05-24T18:05:00-03:00` |
| Propaga para `parity_specs.md § Exceções` | sim |

### DEV-009

| Campo | Valor |
|---|---|
| Tela afetada | `SCR-017 UserAccountDropdown` |
| Tipo | `modernizacao` |
| Descrição | O item `About Focalboard` e o modal associado foram removidos do dropdown de conta. |
| Motivo | A referência é específica do legado e não deve ser transportada para o produto alvo. O dropdown mantém apenas ações úteis de conta. |
| Origem no legado | `componentes/screens.md` — User Account Dropdown |
| Implicação para parity tests | Não esperar modal de about; validar apenas `Change password`, `Invite users` e `Log out`. |
| Aprovação | `aprovado` |
| Aprovado por | `igorzanin` |
| Aprovado em | `2026-05-24T18:05:00-03:00` |
| Propaga para `parity_specs.md § Exceções` | sim |

## Telas com mais de uma deviation

| Tela | IDs |
|---|---|
| `SCR-002 RegisterPage` | DEV-001, DEV-006, DEV-007 |
| `SCR-003 HomePage` | DEV-002, DEV-006, DEV-007 |
| `SCR-004 BoardTableView` | DEV-006, DEV-008 |
| `SCR-005 BoardKanbanView` | DEV-006, DEV-008 |
| `SCR-017 UserAccountDropdown` | DEV-006, DEV-007, DEV-009 |
| `SCR-018 ChangePasswordPage` | DEV-003, DEV-006 |
| `SCR-019 FilterPanel` | DEV-004, DEV-006 |
| `SCR-020 SortPanel` | DEV-005, DEV-006 |

## Notas

- As cinco ausências de screenshot foram absorvidas como divergências de plataforma porque o modo modernizado foi aprovado explicitamente.
- Nenhuma deviation ficou pendente; o próximo agente pode consumir estas exceções diretamente.
- O adapter `web-spa__vue3-spa` continua adequado para v1: todas as telas podem ser descritas via `component-tree` sem necessidade de formato raw.
