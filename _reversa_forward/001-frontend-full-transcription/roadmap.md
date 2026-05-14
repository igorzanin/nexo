# Roadmap: Transcrição completa do frontend legado

> Identificador: `001-frontend-full-transcription`
> Data: `2026-05-14`
> Requirements: `_reversa_forward/001-frontend-full-transcription/requirements.md`
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA

## 1. Resumo da abordagem

A transcrição será conduzida em 4 fases sequenciais:

1. **Re-análise do frontend legado** — percorrer `focalboard-legacy/webapp/src/` módulo a módulo (páginas, componentes, properties, widgets, store, blocks, hooks, utilitários), documentando cada item com comportamento, estados, props e rastreabilidade
2. **Extração do design system** — catalogar todas as variáveis SCSS, cores, tipografia, z-index, breakpoints e shadows do legado, mapeando para tokens Bootstrap 5.3 + CSS custom properties
3. **Geração de especificações** — produzir `requirements.md` + `design.md` + `tasks.md` por módulo frontend (formato SDD do Reversa)
4. **Transcrição em código** — reimplementar cada módulo em Vue 3 + Composition API + Pinia + Bootstrap 5.3, seguindo a ordem: Páginas → Componentes de Layout → Visualizações de Board → Card Detail → Property Editors → Widgets → Stores

Exclusões confirmadas: integrações Mattermost e componentes desktop nativo. Ícones migrados para Bootstrap Icons.

## 2. Princípios aplicados

Nenhum arquivo `.reversa/principles.md` encontrado. Nenhum princípio a verificar.

## 3. Decisões técnicas

| ID | Decisão | Justificativa | Alternativas descartadas | Confidência |
|----|---------|----------------|--------------------------|-------------|
| D-01 | Abordagem híbrida: Bootstrap 5.3 para layout/formulários, JS custom para interações complexas (DnD, menus aninhados) | A decisão veio do esclarecimento com o usuário. Bootstrap cobre 80% dos casos; interações complexas do Kanban/Table exigem JS específico | Literal (replicar 1:1 todo o comportamento React) geraria retrabalho; modernizado puro (só Bootstrap) perderia comportamentos críticos | 🟢 |
| D-02 | Bootstrap Icons como biblioteca de ícones padrão, com mapeamento dos SVG legados para equivalentes | Decisão do usuário. Elimina necessidade de manter sprite ou componentes SVG próprios | Manter SVGs legados como componentes Vue inline; usar sprite único | 🟢 |
| D-03 | Prioridade de transcrição: 1º Páginas/Layout, 2º Visualizações de Board, 3º Card Detail + Properties, 4º Widgets + Stores + demais | Decisão do usuário. Páginas e Layout são a base da navegação; Visualizações são o núcleo funcional visível | Ordem alfabética; por complexidade decrescente; por dependências bottom-up | 🟢 |
| D-04 | Documentação detalhada com revisão cruzada obrigatória | Decisão do usuário. Garante qualidade e detecta lacunas antes da codificação | Documentação essencial; documentação completa sem revisão | 🟢 |
| D-05 | Re-análise do frontend legado como pré-requisito antes de qualquer transcrição | Sem a re-análise completa não é possível saber o que existe, o que falta e o que mudou desde a primeira extração | Confiar apenas na extração reversa original (que já se mostrou incompleta para o frontend) | 🟢 |

## 4. Premissas

Nenhuma dúvida pendente. Todas as premissas foram validadas na sessão de esclarecimentos.

## 5. Delta arquitetural

| Componente | Arquivo de origem no legado | Tipo de mudança | Resumo |
|------------|------------------------------|-----------------|--------|
| Páginas | `focalboard-legacy/webapp/src/pages/` | componente-novo | Página Welcome (onboarding) não existia na primeira reconstrução. Página boardPage pode ter sub-rotas ou estados não cobertos |
| Componentes de Layout | `_reversa_sdd/componentes/requirements.md` | regra-alterada | Workspace, Sidebar, CenterPanel existem mas podem ter sub-componentes não implementados (ex: BoardsSwitcher, SidebarSettingsMenu, UserMenu) |
| Visualizações de Board | `_reversa_sdd/componentes/requirements.md` | regra-alterada | Kanban, Table, Calendar, Gallery existem mas comportamento pode diferir do legado (DnD, filtros, agrupamento, ordenação) |
| Property Editors | `focalboard-legacy/webapp/src/properties/` | componente-novo | 19 editors: text, number, select, multiSelect, date, person, checkbox, url, email, phone, createdBy, createdTime, updatedBy, updatedTime, etc. Não existem na reconstrução atual |
| Widgets | `focalboard-legacy/webapp/src/widgets/` | componente-novo | 30 widgets (menu, tooltip, modal, emojiPicker, switch, label, editable, personSelector, iconSelector, etc.) |
| Ícones | `focalboard-legacy/webapp/src/svg/` | componente-extinto | SVGs legados substituídos por Bootstrap Icons |
| Stores | `_reversa_sdd/store/requirements.md` | regra-alterada | 14 Pinia stores existentes vs 19 Redux slices legados. Lacunas como attachments, channels, limits, searchText podem não ter cobertura |
| Block Models | `_reversa_sdd/blocos/requirements.md` | regra-alterada | Tipos existentes mas podem faltar factories ou subtipos (h1, h2, h3, attachmentBlock, etc.) |
| Hooks/Composables | `focalboard-legacy/webapp/src/hooks/` | componente-novo | permissions, sortable, websockets, useGetAllTemplates podem não ter equivalentes Vue |
| Utilitários | `focalboard-legacy/webapp/src/` | componente-novo | cardFilter, mutator, octoClient, octoUtils, csvExporter, archiver, etc. |

## 6. Delta no modelo de dados

- Resumo das mudanças: Nenhuma mudança no modelo de dados do backend. O delta é exclusivamente no frontend: novos tipos de componente Vue, novos composables, novos stores e tipos faltantes.
- Detalhe completo em: `_reversa_forward/001-frontend-full-transcription/data-delta.md`

## 7. Delta de contratos externos

Nenhum contrato externo (API REST, WebSocket, fila) é afetado. A transcrição do frontend consome os mesmos endpoints da API existente.

## 8. Plano de migração

n/a — A transcrição é incremental e convive com o código existente. Componentes novos são adicionados sem remover os existentes. Componentes existentes que precisarem de ajuste são modificados in-place.

## 9. Riscos e mitigações

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| Comportamentos complexos do legado (DnD Kanban, menu aninhado) não têm equivalente direto em Bootstrap 5.3 | alto | médio | Abordagem híbrida aprovada: usar vuedraggable + JS custom onde Bootstrap não cobre |
| Número de componentes subestimado | médio | médio | RF-02 exige inventário exaustivo antes de qualquer transcrição; o plano de tasks será ajustado após o inventário |
| Property editors (18 tipos) podem ter comportamentos de validação e edge cases não documentados | médio | alto | RF-04 exige spec individual por editor. Revisão cruzada com o Reviewer captura lacunas |
| Stores Redux legadas podem ter getters/lógica de negócio que não foi transportada para as Pinia stores | médio | médio | RF-06 exige matriz de paridade. Cada getter/action sem equivalente vira task |
| Dependência de bibliotecas legadas sem equivalente Vue (ex: plugin de markdown, emoji picker) | baixo | médio | Investigation.md lista alternativas. Decisão técnica por componente |

## 10. Critério de pronto

- [ ] Inventário completo do frontend legado gerado em `_reversa_sdd/frontend-inventory.md`
- [ ] Design system extraído e mapeado para tokens Bootstrap 5.3
- [ ] Todos os 19 property editors com spec individual gerada
- [ ] Todos os 30 widgets com spec individual gerada
- [ ] Matriz de paridade stores + blocks gerada
- [ ] Plano de tasks (`actions.md`) aprovado
- [ ] Cross-check via `/reversa-audit` sem CRITICAL nem HIGH
- [ ] `regression-watch.md` gerado
- [ ] Re-extração reversa executada e sem regressão vermelha

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-05-14 | Versão inicial gerada por `/reversa-plan` | reversa |
