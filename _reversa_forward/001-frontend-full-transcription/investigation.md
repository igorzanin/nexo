# Investigation — Transcrição completa do frontend legado

> Feature: `001-frontend-full-transcription`
> Data: `2026-05-14`

## 1. Estrutura do frontend legado

O frontend legado em `focalboard-legacy/webapp/src/` está organizado em:

| Diretório | Conteúdo | Tamanho |
|-----------|----------|---------|
| `pages/` | Componentes de página React (boardPage, login, register, changePassword, error, welcome) | 10 entries |
| `components/` | Componentes de UI React (kanban, table, calendar, gallery, cardDetail, sidebar, viewHeader, search, etc.) | 92 entries |
| `properties/` | Property editors (text, number, select, multiSelect, date, person, checkbox, etc.) | 19 entries |
| `widgets/` | Widgets reutilizáveis (menu, tooltip, emojiPicker, switch, label, editable, modal, etc.) | 30 entries |
| `store/` | Redux state management (boards, cards, views, users, teams, comments, etc.) | 19 entries |
| `blocks/` | Modelos de dados TypeScript (Block, Board, Card, BoardView, factories) | 24 entries |
| `hooks/` | React hooks customizados (permissions, sortable, websockets) | 4 entries |
| `styles/` | SCSS variables, typography, main styles | 9 entries |
| `svg/` | Ícones SVG | múltiplos |
| `i18n/` | Internacionalização | múltiplos idiomas |

### Tecnologias do legado
- React 16+ com JSX/TSX
- Redux para estado global
- SCSS para estilos (com variáveis customizadas)
- Webpack para build
- React DnD para drag-and-drop

## 2. Stack alvo (existente)

O frontend atual do Nexo em `webapp/src/` usa:
- Vue 3 + Composition API + `<script setup>`
- Pinia para estado global
- Bootstrap 5.3 para UI framework
- Vite para build
- vuedraggable (sortablejs) para drag-and-drop
- vue-i18n para internacionalização
- Vue Router para roteamento

### Cobertura atual vs legado

Com base no `_reversa_sdd/`, a reconstrução atual cobre:
- **Páginas:** 6 de 6 (Login, Register, ChangePassword, Error, BoardPage, BoardPage com rotas) 🟢
- **Componentes:** ~31 componentes documentados. O legado tem ~92 entries. **Lacuna estimada: ~60 componentes**
- **Stores:** 14 Pinia stores. O legado tem 19 Redux slices. **Lacuna: ~5 stores** (attachments, channels, limits, searchText, globalTemplates)
- **Property editors:** 0 no novo sistema. O legado tem 19. **Lacuna: 19 editors**
- **Widgets:** 0 como biblioteca reutilizável. O legado tem 30. **Lacuna: 30 widgets**
- **Block models:** Parcial. Factories para h1, h2, h3, attachmentBlock podem estar faltando.

## 3. Alternativas avaliadas

### Abordagem de transcrição
| Alternativa | Vantagens | Desvantagens |
|-------------|-----------|--------------|
| **Reescrever do zero** | Liberdade total, sem dívida técnica do legado | Perde comportamento refinado, prazo longo |
| **Transcrição 1:1** (literal) | Fidelidade comportamental garantida | Ignora benefícios do Bootstrap, retrabalho de interações |
| **Híbrida** (escolhida) | Bootstrap cobre 80%, JS custom cobre comportamentos complexos | Requer decisão caso a caso sobre o que é "complexo" |

### Biblioteca de ícones
| Alternativa | Vantagens | Desvantagens |
|-------------|-----------|--------------|
| **Manter SVGs legados** | Zero migração | Bundle grande, sem padronização |
| **Bootstrap Icons** (escolhido) | Já incluso no ecossistema Bootstrap, consistência | Requer mapeamento de cada ícone |
| **Phosphor Icons** | Mais opções de estilo | Dependência externa extra |
| **Heroicons** | Popular no ecossistema Vue | Dependência externa extra |

### Drag-and-drop
- **vuedraggable** (já presente no projeto) — wrapper Vue para SortableJS. Adequado para Kanban e Table
- @vueuse/gesture — alternativa mais leve mas sem suporte a lista sortable
- HTML5 Drag and Drop nativo — sem dependência, mas mais verboso

### Property editors
Cada property editor legado é um componente React que gerencia:
- Exibição do valor atual
- Edição inline (clique → input)
- Validação do valor
- Persistência via API (patch block)

A reimplementação em Vue 3 seguirá o padrão:
```vue
<script setup lang="ts">
// Props: propertyValue, propertyTemplate, readonly
// Emits: update:propertyValue
// Validação local antes de emitir
</script>
```

## 4. Padrões aplicáveis

### Padrão de componente de propriedade
Cada property editor seguirá a interface:
```
Props: { propertyValue, propertyTemplate, readonly?, boardId, cardId }
Emits: update:propertyValue
Slots: display (default), edit (when editing)
```

### Padrão de widget reutilizável
Cada widget seguirá o padrão de componente Bootstrap 5.3:
- Classes CSS Bootstrap como base
- Props para variantes e estados
- Slots para conteúdo customizado

### Padrão de store
Novas stores Pinia seguirão o mesmo padrão das existentes:
- `defineStore` com composition API
- Acesso via `storeToRefs`
- Mutação via Mutator (API + dispatch)

## 5. Dependências a adicionar

Nenhuma nova dependência npm é necessária:
- `bootstrap-icons` — já incluso no Bootstrap 5.3 (ou instalável via `npm i bootstrap-icons`)
- `vuedraggable` — já presente
- `@fullcalendar/*` — já presente

## 6. Fontes de referência

| Recurso | Link |
|---------|------|
| Bootstrap 5.3 Components | https://getbootstrap.com/docs/5.3/components/ |
| Bootstrap Icons | https://icons.getbootstrap.com/ |
| vuedraggable | https://github.com/SortableJS/vue.draggable.next |
| Vue 3 Composition API | https://vuejs.org/guide/extras/composition-api-faq |
| Pinia | https://pinia.vuejs.org/ |
