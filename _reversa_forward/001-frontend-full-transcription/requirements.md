# Requirements: Transcrição completa do frontend legado

> Identificador: `001-frontend-full-transcription`
> Data: `2026-05-14`
> Pasta da extração reversa: `_reversa_sdd/`
> Fonte legado: `focalboard-legacy/webapp/`
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA / DÚVIDA

## 1. Resumo executivo

Reanalisar integralmente o frontend legado do Focalboard (React + TypeScript + SCSS) localizado em `focalboard-legacy/webapp/`, documentar todas as telas, componentes, estados, estilos, store, blocos de dados, property editors e widgets que ficaram de fora da reconstrução anterior, e gerar o planejamento completo para transcrever cada elemento para a stack alvo (Vue 3 + Composition API + Pinia + Bootstrap 5.3 + TypeScript). O entregável é um conjunto de especificações executáveis que cubram 100% do frontend legado, permitindo que a transcrição seja precisa e sem lacunas.

## 2. Contexto a partir do legado

| Fonte | Trecho relevante | Confidência |
|-------|------------------|-------------|
| `_reversa_sdd/architecture.md#Frontend-SPA` | Arquitetura Vue 3 atual: Pages → Components → Pinia Stores → Models | 🟢 |
| `_reversa_sdd/componentes/requirements.md` | 31 componentes Vue 3 documentados (Workspace, Kanban, Table, Calendar, Gallery, CardDetail, etc.) | 🟢 |
| `_reversa_sdd/paginas/requirements.md` | 7 páginas/rotas documentadas (Login, Register, ChangePassword, Error, BoardPage) | 🟢 |
| `_reversa_sdd/store/requirements.md` | 14 Pinia stores documentadas (board, card, view, user, team, comment, content, etc.) | 🟢 |
| `_reversa_sdd/blocos/requirements.md` | Modelos de dados TypeScript (Block, Board, Card, BoardView, factories, patches) | 🟢 |
| `focalboard-legacy/webapp/src/components/` | 92 entries no diretório de componentes React legados | 🟢 |
| `focalboard-legacy/webapp/src/pages/` | 6 páginas React legadas (boardPage, changePassword, error, login, register, welcome) | 🟢 |
| `focalboard-legacy/webapp/src/store/` | 19 arquivos de store Redux legados | 🟢 |
| `focalboard-legacy/webapp/src/blocks/` | 24 arquivos de modelos/blocos de dados legados | 🟢 |
| `focalboard-legacy/webapp/src/properties/` | 19 property editors legados (text, number, select, multiSelect, date, person, checkbox, url, email, phone, etc.) | 🟢 |
| `focalboard-legacy/webapp/src/widgets/` | 30 widgets de UI legados (buttons, menu, emojiPicker, tooltip, switch, label, editable, etc.) | 🟢 |
| `focalboard-legacy/webapp/src/styles/` | 9 arquivos de estilo SCSS (variables, typography, main, labels, z-index, modifiers, markdown) | 🟢 |
| `focalboard-legacy/webapp/src/hooks/` | 4 hooks React legados (permissions, sortable, websockets, useGetAllTemplates) | 🟢 |
| `focalboard-legacy/webapp/src/svg/` | Ícones SVG do legado | 🟢 |
| `focalboard-legacy/webapp/i18n/` | Arquivos de internacionalização | 🟢 |

## 3. Personas e cenários de uso

| Persona | Objetivo | Cenário-chave |
|---------|----------|---------------|
| Desenvolvedor fullstack | Transcrever componente legado para Vue 3 | Pegar um componente React existente em `focalboard-legacy/webapp/src/components/kanban/` e reimplementá-lo fielmente em Vue 3 com Bootstrap 5.3, preservando comportamento e estado |
| Arquiteto de frontend | Validar cobertura da transcrição | Comparar inventário de componentes legados vs. implementados e identificar lacunas |
| Designer de sistemas | Garantir fidelidade visual | Verificar se todos os tokens de design (cores, tipografia, espaçamentos) do legado foram mapeados para o novo design system |
| QA | Validar paridade comportamental | Testar cada tela transcrita contra o comportamento original do legado |

## 4. Regras de negócio novas ou alteradas

1. **RN-01:** Todo componente React legado em `focalboard-legacy/webapp/src/` deve ser analisado e classificado como: transcrito (já existe equivalente Vue), pendente (não existe equivalente), excluído (fora de escopo por decisão do usuário) ou obsoleto (não aplicável ao novo sistema). 🟢
   - Origem no legado: `focalboard-legacy/webapp/src/`
   - Exclusões confirmadas: integrações Mattermost (`webapp/src/plugins/`), componentes desktop nativos (`win-wpf/`, `mac/`)
   - Tipo: nova

2. **RN-02:** A transcrição deve preservar 100% dos estados visuais (normal, vazio, carregando, erro, disabled) de cada componente legado. 🟢
   - Origem no legado: análise dos componentes React
   - Tipo: nova

3. **RN-03:** Property editors legados (18 tipos) devem ser reimplementados usando Bootstrap 5.3, mantendo o mesmo comportamento de edição, validação e exibição. 🟢
   - Origem no legado: `focalboard-legacy/webapp/src/properties/`
   - Tipo: nova

4. **RN-04:** O sistema de design do legado (cores, tipografia, variáveis SCSS, z-index, breakpoints) deve ser completamente extraído e mapeado para os tokens equivalentes no novo sistema Bootstrap 5.3 e CSS custom properties. 🟢
   - Origem no legado: `focalboard-legacy/webapp/src/styles/`
   - Tipo: nova

5. **RN-05:** Toda store Redux legada deve ter sua store Pinia correspondente verificada para paridade de estado, actions e getters. 🟢
   - Origem no legado: `focalboard-legacy/webapp/src/store/`
   - Tipo: nova

6. **RN-06:** Widgets de UI reutilizáveis do legado (menu, tooltip, modal, emojiPicker, switch, label, editable) devem ser catalogados e reimplementados como componentes Vue 3 reutilizáveis. 🟢
   - Origem no legado: `focalboard-legacy/webapp/src/widgets/`
   - Tipo: nova

## 5. Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de aceite | Confidência |
|----|-----------|------------|--------------------|-------------|
| RF-01 | Reanalisar todas as páginas legadas (`pages/`) e documentar cada rota, estado e transição | Must | Cada página legada tem entry correspondente no inventário com análise de comportamento | 🟢 |
| RF-02 | Reanalisar todos os componentes legados (`components/`) e classificar como transcrito/pendente/obsoleto | Must | Inventário completo com 100% dos componentes classificados | 🟢 |
| RF-03 | Extrair o sistema de design completo do legado: cores, tipografia, espaçamentos, z-index, breakpoints, shadows | Must | Documento de design tokens gerado em `_reversa_sdd/design-system/` | 🟢 |
| RF-04 | Reanalisar os 19 property editors legados e gerar specs para reimplementação em Vue 3 + Bootstrap 5.3 | Must | Spec de cada property editor com comportamento, validação e aparência | 🟢 |
| RF-05 | Reanalisar os 30 widgets de UI legados e gerar specs para componentes Vue 3 reutilizáveis | Must | Spec de cada widget com estados e variantes | 🟢 |
| RF-06 | Reanalisar as 19 stores Redux legadas e verificar paridade com as 14 Pinia stores existentes | Should | Matriz de rastreamento store-legado → store-Pinia com lacunas identificadas | 🟢 |
| RF-07 | Reanalisar os blocks/models legados e verificar paridade com os tipos TypeScript existentes | Should | Matriz completa blocks-legados → tipos-existente com lacunas | 🟢 |
| RF-08 | Catalogar todos os ícones SVG do legado (`svg/`) e mapear para equivalentes no Bootstrap Icons, documentando substituições | Should | Inventário de ícones com mapeamento legado → Bootstrap Icons | 🟢 |
| RF-09 | Reanalisar os hooks legados e mapear para composables Vue 3 equivalentes | Should | Mapeamento hooks → composables com implementação se necessário | 🟢 |
| RF-10 | Reanalisar a internacionalização do legado (`i18n/`) e comparar com a estrutura vue-i18n atual | Could | Relatório de chaves i18n faltantes ou divergentes | 🟢 |
| RF-11 | Reanalisar os arquivos de utilitários legados (`utils.ts`, `mutator.ts`, `octoClient.ts`, `cardFilter.ts`, etc.) e verificar cobertura no novo sistema | Could | Matriz de utilitários com status implementado/não implementado | 🟢 |
| RF-12 | Gerar plano de transcrição com estimativa de esforço por módulo (páginas, componentes, properties, widgets, stores) | Must | Plano detalhado com dependências e prioridades | 🟢 |

## 6. Requisitos Não Funcionais

| Tipo | Requisito | Evidência ou justificativa | Confidência |
|------|-----------|----------------------------|-------------|
| Completude | 100% dos componentes e páginas legados devem ser cobertos pela análise | `focalboard-legacy/webapp/src/` tem estrutura completa e acessível | 🟢 |
| Rastreabilidade | Cada spec gerada deve referenciar o arquivo legado exato de origem | Metodologia do Reversa exige rastreabilidade `legado → spec` | 🟢 |
| Consistência | A transcrição deve manter o mesmo comportamento observável, não apenas a mesma aparência | Requisito de paridade funcional do Reversa | 🟢 |
| Modularidade | Cada componente transcrito deve ser autocontido e testável isoladamente | Arquitetura Vue 3 + Composition API favorece componentização | 🟢 |

## 7. Critérios de Aceitação

```gherkin
Cenário: Inventário completo do frontend legado
  Dado que o diretório focalboard-legacy/webapp/src/ existe
  Quando a reanálise for concluída
  Então deve existir um inventário em _reversa_sdd/frontend-inventory.md listando todos os componentes, páginas, stores, widgets, properties e utilitários legados com classificação de status

Cenário: Design tokens extraídos
  Dado que os arquivos SCSS do legado estão em focalboard-legacy/webapp/src/styles/
  Quando a extração de design system for concluída
  Então deve existir um documento de design tokens com cores, tipografia, espaçamentos, z-index e breakpoints

Cenário: Property editors documentados
  Dado que os 19 property editors estão em focalboard-legacy/webapp/src/properties/
  Quando a análise for concluída
  Então cada property editor deve ter uma spec individual com comportamento, validação, aparência e mapeamento Bootstrap 5.3

Cenário: Plano de transcrição gerado
  Dado que toda a análise do frontend legado foi concluída
  Quando o plano for gerado
  Então deve conter tarefas atômicas com dependências, prioridades e estimativa de esforço por módulo
```

## 8. Prioridade MoSCoW

| Item | MoSCoW | Justificativa |
|------|--------|---------------|
| RF-01 (páginas) | Must | Base da navegação do sistema |
| RF-02 (componentes) | Must | Núcleo da interface do usuário |
| RF-03 (design system) | Must | Fundamental para consistência visual |
| RF-04 (properties) | Must | Funcionalidade crítica de edição de cards |
| RF-05 (widgets) | Must | Componentes reutilizáveis essenciais |
| RF-12 (plano) | Must | Entregável final que habilita a execução |
| RF-06 (stores) | Should | Já existe implementação parcial |
| RF-07 (blocks) | Should | Já existe implementação parcial |
| RF-08 (ícones) | Should | Impacto visual, não funcional |
| RF-09 (hooks→composables) | Should | Refatoração de lógica |
| RF-10 (i18n) | Could | Pode ser feito incrementalmente |
| RF-11 (utilitários) | Could | Pode ser feito incrementalmente |

## 9. Esclarecimentos

### Sessão 2026-05-14

- **Q:** Quais componentes do legado devem ser excluídos da transcrição?
  **R:** Integrações com Mattermost e componentes específicos de desktop nativo (win-wpf, mac). Os demais 100% devem ser transcritos.

- **Q:** Qual abordagem usar para comportamentos complexos (Kanban DnD, menu aninhado, search)?
  **R:** Híbrido — Bootstrap 5.3 para Layout/Formulários, JS custom para interações complexas.

- **Q:** Qual a ordem de prioridade da transcrição?
  **R:** 1º Páginas e Layout (Workspace, Sidebar, CenterPanel), 2º Visualizações de Board (Kanban, Table, Calendar, Gallery), em seguida os demais módulos.

- **Q:** Como tratar os ícones SVG do legado?
  **R:** Migrar para Bootstrap Icons como biblioteca de ícones padrão.

- **Q:** Qual nível de documentação da re-análise?
  **R:** Detalhada — completa + revisão cruzada com o Reviewer e relatório de confiança.

## 10. Lacunas

Resolvidas na sessão de esclarecimentos de 2026-05-14. Nenhuma lacuna pendente.

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-05-14 | Versão inicial gerada por `/reversa-requirements` | reversa |
| 2026-05-14 | Sessão de esclarecimentos: respostas sobre exclusão (Mattermost/desktop), abordagem híbrida, prioridade páginas+boards, Bootstrap Icons, documentação detalhada | reversa |
