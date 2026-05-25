---
schemaVersion: 1
generatedAt: 2026-05-24T17:05:00-03:00
reversa:
  version: "1.0.0"
kind: migration_strategy
producedBy: strategist
hash: "sha256:strategist-migration-strategy-nexo"
---

# Migration Strategy

> Estratégias de migração avaliadas com trade-offs explícitos.
> A estratégia recomendada é a sugestão do Strategist; a decisão final é humana.

---

## Contexto sintetizado

| Dimensão | Valor |
|---|---|
| Tamanho do legado | ~345 arquivos projetados (80 backend, 200 frontend, 60 importadores, 5 desktop) |
| Status atual | Reescrita parcial iniciada — `webapp/` em rascunho, `nexo/` com estrutura de camadas mas implementação incompleta |
| Apetite derivado | **balanced** |
| Gap de paradigma | **NONE** — transição Go→Python e React+Redux→Vue3+Pinia já executada |
| Integrações externas | **nenhuma** (standalone, sem Mattermost, sem cloud) |
| Usuários em produção | **nenhum** — sistema não está em produção |
| Restrições de prazo | **indefinido** |
| Restrições regulatórias | **nenhuma** |
| Risco principal do brief | Sistema incompleto ou com fluxos ausentes |

---

## Estratégias avaliadas

### Estratégia A: Big Bang Controlado ⭐ RECOMENDADA

- **Descrição**: Implementar o sistema novo completo a partir das specs do Reversa, realizar testes de paridade abrangentes (via `parity_specs.md` do Inspector), e fazer o go-live em janela única após validação.
- **Quando aplica**: sistema não está em produção; sem integrações externas vivas; specs completas disponíveis; equipe pequena (1 desenvolvedor); sem usuários dependentes durante o desenvolvimento.
- **Custo**: baixo–médio (uma iteração de implementação, sem infraestrutura duplicada)
- **Risco**: médio → **baixo** (mitigado por: parity tests do Inspector, specs detalhadas do Reversa, ausência de usuários em produção, rollback simples pois o legado continua rodável)
- **Tempo**: curto–médio (implementação sequencial guiada pelos artefatos; sem overhead de dual-stack)
- **Adequação ao apetite derivado** (`balanced`): alta — o catálogo indica que "balanced" favorece Strangler Fig + Parallel Run, mas ambas assumem sistema em produção com usuários. O fator mais relevante aqui é o contexto: **o sistema novo não tem usuários para interromper**. Big Bang com testes abrangentes é mais eficiente neste cenário.
- **Trade-offs**:
  - Prós:
    - Sem overhead de manter dois sistemas em paralelo (nenhum proxy de roteamento, nenhuma migração incremental de schema)
    - Implementação guiada diretamente pelas specs do Reversa — o `reversa-reconstructor` pode executar artefato por artefato
    - Rollback trivial: legado (Focalboard original) continua funcional e não é deletado
    - Sem usuários em produção → janela de go-live flexível e sem pressão de SLA
    - Simplicidade operacional: Igor trabalha em um único codebase, sem split mental entre dois sistemas vivos
  - Contras:
    - Risco de descobrir edge cases comportamentais apenas em uso real (mitigado pelos parity tests)
    - Pressão psicológica de "tudo ou nada" no go-live (mitigada pelo rollback simples)
    - Webapp rascunho existente pode ser tentação de aproveitar código incorreto — exige disciplina de partir dos specs, não do rascunho

---

### Estratégia B: Strangler Fig por Módulo

- **Descrição**: Implementar e ativar um módulo funcional por vez (auth → boards → blocks → views → importadores), roteando gradualmente funcionalidades do legado para o sistema novo.
- **Quando aplica**: sistema em produção com usuários ativos; necessidade de rollback granular por domínio; possibilidade de proxy de roteamento entre legado e novo.
- **Custo**: médio–alto (manter dois sistemas em paralelo, roteamento entre legado e novo, sincronização de dados)
- **Risco**: baixo por módulo (mas médio acumulado por complexidade de integração)
- **Tempo**: longo (cada módulo tem seu próprio ciclo de implementação, teste, roteamento e validação)
- **Adequação ao apetite derivado** (`balanced`): média — adequado conceitualmente, mas sobre-engenheirado para o contexto onde o sistema não está em produção.
- **Trade-offs**:
  - Prós:
    - Rollback granular (um módulo por vez)
    - Validação incremental de paridade
  - Contras:
    - **Focalboard (Go) e Nexo (FastAPI) não compartilham banco** — sincronização de dados entre os dois seria complexa e propensa a inconsistências
    - Sem usuários em produção, o benefício principal do Strangler Fig (não interromper usuários) não se aplica
    - Overhead significativo de infraestrutura (proxy, sincronização) sem retorno proporcional
    - Complexidade de manter dois backends com schemas diferentes simultaneamente

---

### Estratégia C: Incremental Big Bang por Camadas (Híbrida)

- **Descrição**: Implementar o sistema novo em fases verticais (backend completo → frontend completo → desktop + importadores), com testes de aceitação ao final de cada fase. Cada fase é um "mini Big Bang" com critérios de go para a próxima.
- **Quando aplica**: equipe pequena trabalhando em sequência; sem paralelismo de trabalho entre camadas; apetite balanced.
- **Custo**: baixo (sem infraestrutura dual, mas com overhead de planejamento de fases)
- **Risco**: baixo–médio (falha em fase não contamina as outras)
- **Tempo**: médio
- **Adequação ao apetite derivado** (`balanced`): alta — preserva a progressividade do balanced sem o overhead do Strangler Fig.
- **Trade-offs**:
  - Prós:
    - Validação progressiva sem manter dois sistemas vivos em paralelo
    - Backend funcional e testado antes do frontend (reduz debug de causa raiz)
    - Natural para desenvolvedor solo: foco de atenção em uma camada por vez
  - Contras:
    - O frontend não pode ser validado end-to-end antes do backend estar completo
    - Pode criar a ilusão de progresso em uma camada enquanto outra está bloqueante
    - Distinguir as fases requer disciplina de não avançar frontend antes do backend estar sólido

---

## Comparativo

| Critério | A — Big Bang Controlado | B — Strangler Fig | C — Incremental por Camadas |
|---|---|---|---|
| Custo | baixo–médio | médio–alto | baixo |
| Risco total | médio→baixo | médio | baixo–médio |
| Tempo | curto–médio | longo | médio |
| Aderência ao apetite balanced | alta | média | alta |
| Adequação ao contexto (sem produção) | **ótima** | baixa | boa |
| Complexidade de infraestrutura | baixa | alta | baixa |
| Adequação para Igor solo | ótima | baixa | boa |
| Rollback | simples (legado intacto) | granular por módulo | simples por fase |

---

## Recomendação do Strategist

- **Estratégia recomendada**: **A — Big Bang Controlado**
- **Justificativa**:
  1. **Contexto de desenvolvimento, não de produção**: o sistema não tem usuários ativos. O principal argumento contra Big Bang (interrupção de usuários) não existe aqui. O legado permanece funcional e acessível durante todo o desenvolvimento.
  2. **Specs Reversa como guia completo**: os artefatos do Writer + Curator + Designer + Inspector fornecem um roteiro de implementação completo. O `reversa-reconstructor` pode executar artefato por artefato, o que torna o Big Bang tão controlado quanto qualquer estratégia incremental.
  3. **Ausência de integrações externas**: sem APIs de terceiros, sem banco compartilhado, sem SLA — os fatores de risco do Big Bang que motivam Strangler Fig estão ausentes.
  4. **Apetite balanced honrado via testes**: o equilíbrio entre velocidade e segurança é garantido pelo `parity_specs.md` (Inspector), não por arquitetura de transição incremental.
  5. **Eficiência para desenvolvedor solo**: manter dois sistemas em paralelo (Strangler Fig) dobraria a carga cognitiva de Igor sem benefício proporcional.

- **Variante recomendada**: **Big Bang Controlado em ordem lógica de módulos** (não por "roteamento incremental", mas por sequência de implementação):
  1. Backend core (auth, boards, blocks, cards, permissions)
  2. WebSocket + real-time
  3. Frontend (páginas, stores, componentes)
  4. Views especializadas (kanban, tabela, galeria, calendário)
  5. Importadores + Desktop (Electron)
  6. Parity tests + go-live

---

## Sinais de alerta específicos

- **Webapp rascunho**: o `webapp/` existente deve ser tratado como descartável. O agente de codificação deve resistir à tentação de "aproveitar" código incorreto — partir das specs é mais rápido do que refatorar rascunho não especificado.
- **Editor markdown (AMB-004)**: library não escolhida ainda. Deve ser decidida antes ou durante a fase de frontend. Atrasar esta decisão bloqueia a implementação de cards com conteúdo rich.
- **Bootstrap double import (REF-006)**: deve ser corrigido no início da fase de frontend — é um bug de produção latente.
- **Paradigma sem gap**: o maior risco não é paradigma, é **completude** — garantir que nenhum fluxo do Curator (43 regras MIGRAR) fique sem implementação.

---

## Decisão humana

- **Estratégia escolhida**: A — Big Bang Controlado
- **Quem decidiu**: Igor Zanin
- **Quando**: 2026-05-24T17:11:36-03:00
- **Justificativa do decisor**: Sistema não está em produção; legado permanece como fallback; specs Reversa fornecem guia completo de implementação.
