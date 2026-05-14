# Regression Watch — Transcrição completa do frontend legado

> Feature: `001-frontend-full-transcription`
> Data: `2026-05-14`

---

## Watch Items

| ID | Origem | Regra esperada após mudança | Tipo de verificação | Sinal de violação |
|----|--------|-----------------------------|---------------------|-------------------|
| W001 | Kanban View | Drag-and-drop de cards entre colunas funciona preservando ordem | presença | Card não persiste após drag, ordem não é mantida |
| W002 | Kanban View | Collapse/expand de colunas oculta/mostra cards | presença | Coluna não colapsa, cards não somem |
| W003 | Table View | Edição inline de propriedade salva ao pressionar Enter | presença | Edição não persiste, valor volta ao original |
| W004 | Table View | Reordenação de linhas por drag | presença | Drag não funciona, ordem não persiste |
| W005 | Calendar View | Criação de card por clique em data | presença | Clique não abre criação |
| W006 | Calendar View | Navegação mês/semana/dia | presença | Navegação não funciona ou quebra layout |
| W007 | Card Detail | Abertura de CardDialog modal via Teleport | presença | Modal não abre, ou abre sem overlay |
| W008 | Card Detail | Edição de propriedades salva via Mutator | presença | Propriedade não persiste após edição |
| W009 | Property Editors | Todos os 18 tipos renderizam e editam corretamente | presença | Tipo não renderiza, edição não funciona |
| W010 | Comments | Criação de comentário via WebSocket notifica em tempo real | presença | Comentário não aparece sem refresh |
| W011 | Sidebar | Drag-and-drop de boards entre categorias | presença | Board não move entre categorias |
| W012 | Sidebar | Criação de categoria customizada | presença | Categoria não aparece na sidebar |
| W013 | Search | Busca com debounce retorna resultados | presença | Busca não retorna resultados, ou sem debounce |
| W014 | WebSocket | Reconexão automática exibe banner de alerta | presença | Banner não aparece, reconexão não ocorre |
| W015 | Onboarding | Tour guiado aparece na primeira vez | presença | Tour não aparece, ou aparece sempre |
| W016 | Flash Messages | Notificações toast aparecem e somem | presença | Toast não aparece, ou não desaparece |
| W017 | BoardPermissionGate | UI se adapta conforme role do usuário | presença | Botão de editar visível para viewer |
| W018 | i18n | Troca de idioma reflete em toda UI | presença | Partes da UI permanecem no idioma anterior |
| W019 | Undo/Redo | Ctrl+Z desfaz última ação | presença | Ação não é desfeita |
| W020 | Icons | Todos os ícones Bootstrap Icons carregam corretamente | presença | Ícone quebrado ou ausente |

---

## Observações

Itens com confidência 🟡/🔴 na spec original (não afetam regressão):
- Factories de H1, H2, H3 blocks: serão verificadas durante implementação
- Stores limits, searchText: serão verificadas durante implementação
- csvExporter, archiver: utilidades secundárias

---

## Histórico de re-extrações

### Re-extração 2026-05-14 11:35

| ID | Veredito | Observação |
|----|----------|------------|
| W001 | 🟢 verde | regra preservada em `_reversa_sdd/componentes/requirements.md#35` |
| W002 | 🟢 verde | Spec atualizada em `_reversa_sdd/componentes/requirements.md` |
| W003 | 🟢 verde | Spec atualizada em `_reversa_sdd/componentes/requirements.md` |
| W004 | 🟢 verde | Spec atualizada em `_reversa_sdd/componentes/requirements.md` |
| W005 | 🟢 verde | Spec atualizada em `_reversa_sdd/componentes/requirements.md` |
| W006 | 🟢 verde | Spec atualizada em `_reversa_sdd/componentes/requirements.md` |
| W012 | 🟢 verde | Spec atualizada em `_reversa_sdd/componentes/requirements.md` |
| W014 | 🟡 amarelo | Reconexão WebSocket implementada em `useWebSocket.ts`, sem banner visível — mantido amarelo até implementação de banner na UI |
| W015 | 🟢 verde | regra documentada em `_reversa_sdd/paginas/spec-pages.md` |
| W016 | 🟢 verde | regra preservada em `_reversa_sdd/componentes/requirements.md` (FlashMessages na árvore) |
| W017 | 🟢 verde | regra preservada em `_reversa_sdd/componentes/requirements.md#34` |
| W018 | 🟢 verde | regra preservada em `_reversa_sdd/store/requirements.md` (languageStore) |
| W019 | 🟢 verde | regra documentada em `_reversa_sdd/paginas/spec-pages.md` (Undo/Redo) |
| W020 | 🟢 verde | regra documentada em `_reversa_sdd/design-system/icon-map.md` |

## Arquivadas

*Itens movidos para cá quando não mais aplicáveis.*
