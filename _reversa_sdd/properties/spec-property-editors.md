# Spec: Property Editors

> Gerado por `/reversa-coding` (T009)
> Fonte legado: `focalboard-legacy/webapp/src/properties/`
> Stack alvo: Vue 3 + Composition API + Bootstrap 5.3 + TypeScript
> 🟢 CONFIRMADO | 🟡 INFERIDO | 🔴 LACUNA

---

## Padrão de implementação

```vue
<script setup lang="ts">
interface Props {
  propertyValue: string | string[] | number | boolean | null
  propertyTemplate: IPropertyTemplate
  readonly?: boolean
  boardId: string
  cardId: string
}
const emit = defineEmits<{
  'update:propertyValue': [value: string | string[] | number | boolean | null]
}>()
</script>
<template>
  <!-- Exibição -->
  <div v-if="readonly" class="property-value-display">
    {{ displayValue }}
  </div>
  <!-- Edição -->
  <component :is="editorComponent" v-else v-bind="editorProps" @update="emit('update:propertyValue', $event)" />
</template>
```

## 1. TextProperty

| Atributo | Valor |
|----------|-------|
| Tipo | `text` |
| Editor | `<input type="text" class="form-control form-control-sm">` |
| Validação | Máximo 255 caracteres |
| Display | Texto puro em `<span>` |

## 2. NumberProperty

| Atributo | Valor |
|----------|-------|
| Tipo | `number` |
| Editor | `<input type="number" class="form-control form-control-sm" step="any">` |
| Validação | Número válido (inteiro ou decimal) |
| Display | Número formatado |

## 3. EmailProperty

| Atributo | Valor |
|----------|-------|
| Tipo | `email` |
| Editor | `<input type="email" class="form-control form-control-sm">` |
| Validação | Email válido (regex) |
| Display | Link `mailto:` |

## 4. UrlProperty

| Atributo | Valor |
|----------|-------|
| Tipo | `url` |
| Editor | `<input type="url" class="form-control form-control-sm">` |
| Validação | URL válida (regex) |
| Display | Link clicável (abre nova aba) |

## 5. PhoneProperty

| Atributo | Valor |
|----------|-------|
| Tipo | `phone` |
| Editor | `<input type="tel" class="form-control form-control-sm">` |
| Validação | Formato de telefone |
| Display | Link `tel:` |

## 6. CheckboxProperty

| Atributo | Valor |
|----------|-------|
| Tipo | `checkbox` |
| Editor | `<div class="form-check"><input type="checkbox" class="form-check-input"></div>` |
| Validação | Booleano |
| Display | `bi-check-square` se true, `bi-square` se false |

## 7. SelectProperty

| Atributo | Valor |
|----------|-------|
| Tipo | `select` |
| Editor | Bootstrap 5.3 dropdown com opções do `propertyTemplate.options` |
| Opções | Array `{id, value, color}` do board `cardProperties` |
| Display | Badge colorido com label |
| Vazio | "Empty" (placeholder) |

## 8. MultiSelectProperty

| Atributo | Valor |
|----------|-------|
| Tipo | `multiSelect` |
| Editor | Dropdown multi-seleção com checkboxes |
| Opções | Array `{id, value, color}` |
| Display | Múltiplos badges coloridos |
| Vazio | "Empty" |

## 9. DateProperty

| Atributo | Valor |
|----------|-------|
| Tipo | `date` |
| Editor | `<input type="date">` ou Bootstrap datepicker |
| Formato | ISO (`YYYY-MM-DD`) no valor, localizado na exibição |
| Display | Data formatada (`DD/MM/YYYY` por exemplo) |
| Vazio | "No date" |

## 10. PersonProperty

| Atributo | Valor |
|----------|-------|
| Tipo | `person` |
| Editor | Seletor de usuário com busca |
| Dados | Users do board (via `useUserStore`) |
| Display | Avatar + nome |
| Vazio | "No one" |

## 11. MultiPersonProperty

| Atributo | Valor |
|----------|-------|
| Tipo | `multiPerson` |
| Editor | Seletor multi-usuário com busca |
| Display | Avatares + nomes |
| Vazio | "No one" |

## 12. CreatedByProperty (read-only)

| Atributo | Valor |
|----------|-------|
| Tipo | `createdBy` |
| Display | Nome do usuário que criou o card |
| Fonte | `card.createAt` → lookup user |

## 13. CreatedTimeProperty (read-only)

| Atributo | Valor |
|----------|-------|
| Tipo | `createdTime` |
| Display | Data/hora de criação do card |
| Fonte | `card.createAt` (timestamp) |

## 14. UpdatedByProperty (read-only)

| Atributo | Valor |
|----------|-------|
| Tipo | `updatedBy` |
| Display | Nome do último usuário que editou o card |
| Fonte | Histórico de mudanças (se disponível) |

## 15. UpdatedTimeProperty (read-only)

| Atributo | Valor |
|----------|-------|
| Tipo | `updatedTime` |
| Display | Data/hora da última atualização |
| Fonte | `card.updateAt` |

## 16. UnknownProperty (fallback)

| Atributo | Valor |
|----------|-------|
| Tipo | `unknown` |
| Display | Valor bruto como texto |
| Editor | Input de texto genérico |

## 17. BaseTextEditor

Utilitário base para edição de texto inline. Usado internamente por text, email, url, phone.
```vue
<script setup lang="ts">
// Props: value, placeholder, validator, multiline
// Emits: save, cancel
// Comportamento: Enter salva, Escape cancela, click fora salva
</script>
```

## 18. Property Types Registry

Arquivo central `types.ts` que mapeia string de tipo → componente editor:

```typescript
export const propertyEditorMap: Record<string, Component> = {
  text: TextProperty,
  number: NumberProperty,
  select: SelectProperty,
  multiSelect: MultiSelectProperty,
  date: DateProperty,
  person: PersonProperty,
  multiPerson: MultiPersonProperty,
  checkbox: CheckboxProperty,
  url: UrlProperty,
  email: EmailProperty,
  phone: PhoneProperty,
  createdBy: CreatedByProperty,
  createdTime: CreatedTimeProperty,
  updatedBy: UpdatedByProperty,
  updatedTime: UpdatedTimeProperty,
  unknown: UnknownProperty,
}
```

## Histórico

| Data | Alteração |
|------|-----------|
| 2026-05-14 | Spec gerada por `/reversa-coding` |
