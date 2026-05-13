# Importador Asana, Design Técnico

## Interface

### CLI

| Parâmetro | Descrição | Obrigatório | Padrão |
|-----------|-----------|-------------|--------|
| `-i` | Caminho do JSON export do Asana | Sim | — |
| `-o` | Caminho do arquivo de saída `.boardarchive` | Não | `archive.boardarchive` |

### Tipos de Entrada

```ts
interface Asana {
    data: Datum[]
}

interface Datum {
    gid: string
    name: string
    notes: string
    projects: Workspace[]
    memberships: Membership[]
}

interface Membership {
    project: Workspace
    section: Workspace
}
```

## Fluxo Principal

1. Parsear argumentos CLI com minimist 🟢 — `importAsana.ts:34`
2. Validar `-i` presente e arquivo existe 🟢 — `importAsana.ts:39-46`
3. Ler arquivo JSON com `readFileSync` 🟢 — `importAsana.ts:49`
4. Extrair projetos únicos via `getProjects` 🟢 — `importAsana.ts:63-75`
5. Usar apenas o primeiro projeto (TODO: múltiplos) 🟢 — `importAsana.ts:99-100`
6. Extrair seções do projeto via `getSections` 🟢 — `importAsana.ts:77-90`
7. Criar board com propriedade Select "Section" e opções coloridas 🟢 — `importAsana.ts:106-134`
8. Criar BoardView 🟢 — `importAsana.ts:137-142`
9. Para cada card: criar CardBlock, mapear seção, anexar notas como TextBlock 🟢 — `importAsana.ts:145-178`
10. Serializar com `ArchiveUtils.buildBlockArchive` e escrever saída 🟢 — `importAsana.ts:57-58`

## Fluxos Alternativos

- **Arquivo não encontrado:** Exibe `File not found: <path>` e sai com código 2 🟢 — `importAsana.ts:43-46`
- **Nenhum projeto encontrado:** Exibe "No projects found", retorna arrays vazios 🟢 — `importAsana.ts:94-97`
- **Card sem membership:** Exibe warn, card é criado sem propriedade Section 🟢 — `importAsana.ts:162-164`

## Dependências

- `import/util/archive.ts` — ArchiveUtils.buildBlockArchive
- `import/asana/asana.ts` — Tipos do modelo Asana
- `import/asana/utils.ts` — Utils.createGuid
- `webapp/src/blocks/block.ts`, `board.ts`, `boardView.ts`, `card.ts`, `textBlock.ts` — Modelos Block/Board do Nexo

## Decisões de Design Identificadas

| Decisão | Evidência no código | Confiança |
|---------|---------------------|-----------|
| Apenas primeiro projeto processado (TODO aberto) | `importAsana.ts:99` | 🟢 |
| Seções viram Select property com cores cíclicas | `importAsana.ts:111-132` | 🟢 |
| Notas preservadas como TextBlock filho com contentOrder | `importAsana.ts:168-177` | 🟢 |
| Cores alternam em array fixo de 9 cores | `importAsana.ts:19-30` | 🟢 |

## Estado Interno

Nenhum — script one-shot sem estado entre execuções.

## Observabilidade

- `console.log` para progresso (board, cards, total encontrado) 🟢
- `console.warn` para cards sem seção 🟢
- `console.error` para erros fatais 🟢
