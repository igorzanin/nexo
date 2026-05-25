# Legacy Impact — Transcrição completa do frontend legado

> Feature: `001-frontend-full-transcription`
> Data: `2026-05-14`
> 🟢 CONFIRMADO | 🟡 INFERIDO | 🔴 LACUNA

---

## Impact Summary

Esta feature **adiciona e altera** componentes do frontend Vue 3, sem modificar o backend. Nenhuma regra do backend em `_reversa_sdd/domain.md` é alterada ou removida.

---

## Arquivos afetados

| Arquivo afetado | Componente | Tipo | Severidade | Justificativa |
|----------------|-----------|------|------------|---------------|
| `webapp/src/pages/WelcomePage.vue` | Páginas | componente-novo | LOW | Nova página de onboarding |
| `webapp/src/components/sidebar/` | Componentes de Layout | regra-alterada | MEDIUM | Novos sub-componentes (sidebarCategory, sidebarBoardItem, etc.) |
| `webapp/src/components/viewHeader/` | ViewHeader | regra-alterada | MEDIUM | Múltiplos sub-menus e search sendo adicionados |
| `webapp/src/components/kanban/` | Visualizações de Board | regra-alterada | HIGH | Comportamento de DnD, columns, cards sendo completado |
| `webapp/src/components/table/` | Visualizações de Board | regra-alterada | HIGH | Edição inline, header, groups, resize sendo adicionados |
| `webapp/src/components/calendar/` | Visualizações de Board | regra-alterada | MEDIUM | Integração FullCalendar sendo completada |
| `webapp/src/components/gallery/` | Visualizações de Board | regra-alterada | MEDIUM | Layout de cards sendo completado |
| `webapp/src/components/cardDetail/` | Card Detail | regra-alterada | HIGH | CardDetail, Properties, Contents, Comments sendo adicionados |
| `webapp/src/components/properties/` | Property Editors | componente-novo | MEDIUM | 19 novos property editor components |
| `webapp/src/components/widgets/` | Widgets | componente-novo | MEDIUM | 30 novos widgets reutilizáveis |
| `webapp/src/components/content/` | Content Blocks | regra-alterada | MEDIUM | Novos block elements (text, image, checkbox, divider, h1-h3, attch) |
| `webapp/src/stores/` | Stores | regra-alterada | MEDIUM | Verificação e completude de stores (limits, attachments, etc.) |
| `webapp/src/composables/` | Hooks/Composables | regra-alterada | MEDIUM | Novos composables: usePermissions, useSortable, useWebSocket completo |
| `webapp/src/utils/` | Utilitários | regra-alterada | LOW | csvExporter, archiver, cardFilter |
| `webapp/src/types/` | Block Models | regra-alterada | LOW | Verificação de factories e interfaces faltantes |
| `webapp/src/` (ícones) | Ícones | componente-extinto | LOW | SVGs substituídos por Bootstrap Icons |

---

## Preservadas

Todas as regras de negócio em `_reversa_sdd/domain.md` (R1-R44) permanecem intactas:
- Regras de Board (R1-R9)
- Regras de Card e Block (R10-R20)
- Regras de Membro e Permissão (R21-R26)
- Regras de Categoria (R27-R29)
- Regras de Subscription (R30-R31)
- Regras de Autenticação (R32-R37)
- Regras de Soft-Delete (R38-R40)
- Regras de WebSocket (R41-R44)

## Modificadas

Nenhuma regra de `_reversa_sdd/domain.md` foi modificada. As mudanças são exclusivamente no frontend:
- Novos componentes Vue (páginas, property editors, widgets, content elements)
- Comportamento existente completado (Kanban DnD, Table inline edit, Calendar FullCalendar)
- Novos composables (usePermissions, useSortable)
- Ícones migrados para Bootstrap Icons

---

## Riscos identificados

| Risco | Severidade | Mitigação |
|-------|-----------|-----------|
| Kanban DnD pode quebrar com alterações | HIGH | vuedraggable já presente; testar após completar |
| Property editors podem ter validação diferente do legado | MEDIUM | Seguir spec individual por editor |
| Performance com muitos widgets carregados | LOW | Lazy loading via defineAsyncComponent |
