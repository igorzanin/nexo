---
schemaVersion: 1
generatedAt: 2026-05-24T18:05:00-03:00
reversa:
  version: "1.0.0"
kind: screen_modernization_decision
producedBy: screen-translator
decidedBy: igorzanin
decidedAt: 2026-05-24T18:05:00-03:00
mode: modernized
sourcePlatform: react-spa
targetPlatform: vue3-spa
hash: "sha256:screen-translator-decision-nexo-modernized"
---

# Decisão de Modernização de Telas

> Decisão consciente sobre como traduzir as telas do sistema legado: paridade observável byte-a-byte, redesign idiomático para a plataforma alvo, ou combinação tela-a-tela.
> Este artefato é leitura obrigatória do próprio Screen Translator (para gerar `target_screens.md`), do Inspector (para construir parity tests adequados ao modo) e do agente de codificação.

## Contexto

- **Plataforma origem detectada**: `react-spa` — React 17 + TypeScript + JSX (Focalboard fork, custom CSS)
- **Confiança**: 🟢 CONFIRMADO — `_reversa_sdd/architecture.md` §"Dívidas Técnicas T6" + `_reversa_sdd/inventory.md` §"webapp/" (JSX components, Redux Toolkit)
- **Plataforma alvo**: `vue3-spa` — Vue 3 + TypeScript + SFC + Bootstrap 5.3 + Pinia
- **Telas inventariadas**: 20 (15 documentadas com screenshot + 5 de "telas pendentes" identificadas pelo Visor)
- **Origem do inventário**: `_reversa_sdd/screens/inventory.json` + `_reversa_sdd/ui/inventory.md`
- **Adapter aplicado**: `web-spa → vue3-spa` (subclasse de `html-legacy__spa`; par não listado explicitamente em `adapter-pairs.md` mas semanticamente idêntico — ambos SPAs com arquitetura de componentes). Formato: `component-tree`.

> **Nota sobre o par não listado**: `react-spa → vue3-spa` não consta na tabela `adapter-pairs.md` v1, mas não é EC-01. Ambas são plataformas SPA baseadas em componentes, e o formato `component-tree` é diretamente aplicável. O adapter `html-legacy__spa` é o mais próximo na tabela e serve de referência.

---

## Modos avaliados

### Modo: literal

- **Definição**: paridade observável pixel-equivalente entre legado e novo.
- **Trade-offs**:
  - Custo de implementação: **alto** — o legado (Focalboard) usa CSS customizado completamente diferente do Bootstrap 5.3 adotado no alvo. Replicar pixel-a-pixel exigiria sobrescrever o Bootstrap com CSS legado.
  - Fidelidade visual: **baixa** — impossível sem recriar o Focalboard CSS. Bootstrap tem box-model, grids e espaçamentos diferentes.
  - Viabilidade de parity tests construtivos: **não** — sem screenshot completa para todas as 20 telas (5 estão pendentes) e sem oráculo executável do legado disponível localmente.
  - Aceitação esperada do usuário final: **baixa** — usuários do sistema novo esperarão UI moderna com Bootstrap 5.3, não replicação do Focalboard legado.
  - Débito técnico futuro: **alto** — manter CSS legado sobreposto ao Bootstrap cria conflitos crescentes.
- **Recomendado**: **não**
- **Justificativa**: CSS frameworks incompatíveis tornam pixel-perfect literal inviável. Sistema não está em produção, sem usuários esperando paridade visual exata.

---

### Modo: modernizado ⭐

- **Definição**: redesign idiomático para Vue 3 + Bootstrap 5.3, preservando hierarquia de informação, fluxo de navegação e conteúdo textual das screenshots como referência.
- **Trade-offs**:
  - Custo de implementação: **médio** — 20 telas especificadas como `component-tree` com vocabulário Bootstrap nativo (Modal, Dropdown, Card, Form). Codificador segue a spec sem inventar.
  - Fidelidade visual: **alta** — screenshots de 15 telas estão disponíveis como referência. Hierarquia de informação, labels, mensagens e fluxos são preservados literalmente. Apenas o CSS é modernizado (Bootstrap 5.3).
  - Viabilidade de parity tests construtivos: **sim** — parity tests semânticos por contrato (eventos, transições, conteúdo textual, estados), sem comparação visual byte-a-byte.
  - Aceitação esperada do usuário final: **alta** — UI moderna e consistente com Bootstrap 5.3 é mais ergonômica que o CSS legado.
  - Débito técnico futuro: **baixo** — Bootstrap 5.3 é manutenível, documentado e idiomático para o stack escolhido.
- **Recomendado**: **sim**
- **Justificativa**: screenshots disponíveis garantem fidelidade de hierarquia de informação. Bootstrap 5.3 é o design system já adotado. O par react-spa→vue3-spa não tem barreira de paradigma — apenas reorganização de sintaxe (JSX→SFC) e de estado (Redux→Pinia).

---

### Modo: híbrido

- **Definição**: telas críticas com máxima fidelidade visual às screenshots; telas secundárias com redesign livre.
- **Trade-offs**:
  - Custo de implementação: **alto** — exige gerenciar dois padrões de spec no mesmo sistema; telas "críticas" ainda sofrem do problema do CSS incompatível.
  - Fidelidade visual mista: alta para críticas (se tiverem screenshots), baixa a média para secundárias.
  - Viabilidade de parity tests: parcial — críticas teriam parity visual, secundárias apenas semântico.
  - Custo de manutenção da separação: **alto** — o codificador precisa alternar entre dois padrões de implementação.
- **Recomendado**: **não**
- **Justificativa**: sem benefício claro sobre modernizado puro, pois mesmo as telas "críticas" não poderiam ser pixel-perfect devido ao CSS incompatível. Adiciona complexidade sem ganho real.

---

## Decisão

- **Modo escolhido**: **modernizado**
- **Justificativa do humano**: recomendação do Screen Translator aceita
- **Alternativas descartadas**:
  - Literal: CSS frameworks incompatíveis (Focalboard CSS → Bootstrap 5.3). Pixel-perfect inviável.
  - Híbrido: sem benefício claro sobre modernizado puro; literal ainda seria inviável para telas "críticas".
- **Decidido em**: 2026-05-24T18:05:00-03:00
- **Decidido por**: igorzanin

---

## Implicações pendentes para a Fase 2

| Etapa | Implicação | Como honrar |
|---|---|---|
| Geração de `target_screens.md` | 20 telas em formato `component-tree`; 4 estados por tela (idle, loading, error, success) | Gerar uma seção por tela com hierarquia de componentes Bootstrap, tokens, eventos e estados explícitos |
| Captura de golden files | Oráculo legado React não está disponível localmente para execução automatizada | Emitir `manifest.yaml` com comando sugerido por tela; captura manual quando disponível |
| Tokens do design-system | Bootstrap 5.3 tokens em `_reversa_sdd/design-system/tokens.md` cobrem o alvo | Referenciar tokens via vocabulário Bootstrap; criar `tokens-derived.md` para valores sem token correspondente |
| Conteúdo textual | Labels, mensagens, prompts e erros copiados literalmente das screenshots e do código legado | Preservar strings exatamente; nenhuma revisão linguística foi aprovada |
| Telas sem screenshot (SCR-002, SCR-003, SCR-018, SCR-019, SCR-020) | 5 telas sem captura disponível; specs derivadas do código legado + fluxo documentado em `flow.md` | Marcar como `DEV-XXX` deviation tipo `plataforma` (sem screenshot de referência); aceite explícito do modo modernizado é suficiente per RF-13 |

---

## Implicações para o Inspector

- **Estratégia de paridade**: modo modernizado → contrato semântico (eventos, transições, conteúdo textual, estados), sem comparação visual byte-a-byte.
  - Inspector deve gerar cenários Gherkin baseados em comportamento de UI: "Dado que o usuário está na tela de Login, quando preenche credenciais inválidas, então vê mensagem de erro".
  - Nenhum golden file visual é obrigatório para parity tests. Se golden files forem capturados manualmente, são complementares.
- **Deviations conhecidas a propagar**: ver `screen_deviation_log.md` (a ser criado na Fase 2).

---

## Notas

- O modo modernizado neste contexto NÃO significa liberdade de redesign visual completo — as screenshots disponíveis são a referência canônica para hierarquia de informação, labels e fluxos. O codificador deve implementar o equivalente Bootstrap das mesmas telas.
- O par `react-spa → vue3-spa` compartilha o mesmo paradigma SPA e a mesma filosofia de componentes, tornando a tradução direta de JSX para SFC idiomática. A maior diferença é estado (Redux → Pinia) e template (JSX → template Vue 3 com `v-if`, `v-for`, etc.).
- `webapp/` atual é rascunho e deve ser ignorado. As specs deste agente substituem os componentes Vue existentes no rascunho.
- 5 telas pendentes de screenshot são especificadas com base em `_reversa_sdd/ui/flow.md` + código legado Focalboard inferido — confiança 🟡 INFERIDO para essas telas.
