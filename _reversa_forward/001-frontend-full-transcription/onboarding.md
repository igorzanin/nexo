# Onboarding — Transcrição completa do frontend legado

> Feature: `001-frontend-full-transcription`
> Data: `2026-05-14`

## Pré-requisitos

- Ambiente Nexo rodando (backend + frontend em dev mode)
- Editor com suporte a TypeScript + Vue 3 (VSCode + Volar recomendado)
- Acesso ao diretório `focalboard-legacy/webapp/src/` para consulta

## Setup inicial

```bash
# 1. Iniciar backend
cd nexo/
uv run uvicorn nexo.main:app --reload

# 2. Em outro terminal, iniciar frontend
cd webapp/
npm run dev
```

## Como testar cada fase

### Fase 1: Re-análise do frontend legado

1. Navegue por `focalboard-legacy/webapp/src/pages/` e abra cada componente React
2. Compare com as páginas Vue em `webapp/src/pages/`
3. Documente diferenças de comportamento, props, estados

### Fase 2: Extração do design system

1. Abra `focalboard-legacy/webapp/src/styles/variables.scss`
2. Extraia todas as variáveis SCSS (cores, fonts, spacing, border-radius, shadows)
3. Mapeie cada uma para o equivalente Bootstrap 5.3:
   - `$primary` → `$primary` (BS) ou `var(--bs-primary)`
   - `$font-family` → `$font-family-base`
   - etc.

### Fase 3: Property editors

1. Abra cada subdiretório em `focalboard-legacy/webapp/src/properties/`
2. Entenda o comportamento de cada tipo:
   - **Text:** input simples com validação de caractere
   - **Number:** input numérico com validação
   - **Select:** dropdown com opções customizáveis do board
   - **MultiSelect:** combo box com múltipla seleção
   - **Date:** date picker
   - **Person:** seletor de usuários
   - **Checkbox:** toggle
   - **URL/Email/Phone:** input com validação de formato
   - **CreatedBy/CreatedTime/UpdatedBy/UpdatedTime:** read-only
3. Implemente cada editor em `webapp/src/components/properties/`

### Fase 4: Visualizações de Board

1. Abra o Kanban legado em `focalboard-legacy/webapp/src/components/kanban/`
2. Teste: arrastar cards entre colunas, criar coluna, renomear coluna, filtrar
3. Compare com `webapp/src/components/kanban/Kanban.vue` existente
4. Implemente as funcionalidades faltantes

## Comandos úteis

```bash
# Rodar testes do frontend
cd webapp/
npm run test

# Build de produção
npm run build

# Lint
npm run lint

# Verificar tipos
npm run typecheck
```

## Critérios de verificação rápida

- [ ] Login/registro funcionando (página + API)
- [ ] BoardPage carrega boards e categorias na sidebar
- [ ] Kanban: arrastar cards entre colunas
- [ ] Table: editar células inline
- [ ] Card dialog: abrir, editar propriedades, adicionar conteúdo
- [ ] Property editors: todos os 18 tipos funcionando
- [ ] Busca: debounce + resultados
- [ ] Compartilhamento: modal + geração de link público
- [ ] Onboarding: tour guiado aparece para novo usuário
- [ ] Internacionalização: troca de idioma reflete em toda UI
