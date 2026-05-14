# Onboarding — Fechamento de lacunas do frontend

> Feature: `002-frontend-gap-closure`
> Data: `2026-05-14`

## Pré-requisitos

- Ambiente Nexo rodando (backend + frontend dev)
- Feature `001-frontend-full-transcription` aplicada

## Setup

```bash
cd nexo/
# Terminal 1: backend
uv run uvicorn nexo.main:app --reload

# Terminal 2: frontend
cd webapp/
npm run dev
```

## Como testar cada módulo

### Kanban
1. Crie um board com cards em diferentes colunas
2. Arraste um card de uma coluna para outra
3. Verifique se o badge de contagem de comentários aparece
4. Verifique se o cálculo (count) aparece no header da coluna

### Table
1. Mude a view para Table
2. Clique no header de uma coluna e selecione "Group by this property"
3. Arraste a borda de um header para redimensionar
4. Verifique cálculos no footer

### Calendar
1. Mude a view para Calendar
2. Navegue entre meses
3. Clique em uma data para criar um card
4. Arraste um card para outra data

### Card Detail
1. Abra um card
2. Clique em "+ Text" e digite conteúdo
3. Adicione uma imagem (upload)
4. Reordene blocos via drag
5. Delete um bloco

### Filtros
1. No ViewHeader, clique no ícone de filtro
2. Adicione filtro por propriedade
3. Verifique se o board filtra corretamente
4. Limpe o filtro

### Views
1. Abra o menu de views no ViewHeader
2. Renomeie uma view
3. Duplique uma view
4. Delete uma view

## Comandos úteis

```bash
npm run dev    # frontend dev server
npm run test   # tests
npm run build  # production build
```

## Checklist de verificação

- [ ] Kanban DnD entre colunas
- [ ] Card badges (comentários, data)
- [ ] Cálculos no Kanban e Table
- [ ] Table row grouping
- [ ] Table column resize
- [ ] Calendar FullCalendar navegação
- [ ] Calendar criar card por clique
- [ ] Card detail editor de blocos CRUD
- [ ] Card detail upload de imagem
- [ ] Filtros funcionando no ViewHeader
- [ ] Renomear/duplicar/deletar views
- [ ] Modal/Dialog genérico
- [ ] Undo/redo via Ctrl+Z
