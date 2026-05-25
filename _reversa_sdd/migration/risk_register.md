---
schemaVersion: 1
generatedAt: 2026-05-24T17:05:00-03:00
reversa:
  version: "1.0.0"
kind: risk_register
producedBy: strategist
hash: "sha256:strategist-risk-register-nexo"
---

# Risk Register

> Registro de riscos da migração com probabilidade, impacto, mitigação e responsável.
> Baseado na estratégia recomendada: Big Bang Controlado.

---

## Riscos

### RISK-001 — Fluxos funcionais ausentes no sistema novo
- **Descrição**: Com 43 regras de negócio a migrar e 15 telas documentadas, existe risco de que algum fluxo funcional crítico (ex: property types, view configuration, group-by dinâmico) fique sem implementação equivalente no novo sistema.
- **Categoria**: técnico
- **Probabilidade**: alta
- **Impacto**: alto
- **Severidade combinada**: 🔴 CRÍTICA
- **Trigger / sinal de alerta**: parity tests do Inspector falhando em > 10% dos cenários Gherkin; usuário reportando fluxo não funcional em testes de aceitação.
- **Mitigação**: seguir rigorosamente os artefatos do Reversa (target_business_rules.md + parity_specs.md); não iniciar go-live com falhas de paridade em fluxos críticos; usar `reversa-reconstructor` para implementação rastreável artefato por artefato.
- **Plano de contingência**: identificar fluxos ausentes via checklist antes do go-live; reverter para Focalboard legado se fluxos críticos não estiverem prontos na janela planejada.
- **Owner**: Igor Zanin (dev / product owner)
- **Status**: aberto

---

### RISK-002 — Webapp rascunho introduzindo comportamento incorreto
- **Descrição**: O `webapp/` atual tem implementações parciais que podem divergir das specs. Se o agente de codificação reusar código do rascunho sem validar contra as specs, podem surgir comportamentos incorretos silenciosos.
- **Categoria**: técnico
- **Probabilidade**: média
- **Impacto**: alto
- **Severidade combinada**: 🟠 ALTA
- **Trigger / sinal de alerta**: comportamento de UI diverge do documentado nas telas do reversa-visor; parity tests falhando em componentes de UI específicos.
- **Mitigação**: tratar `webapp/` como referência, não como base. Specs do `_reversa_sdd/` são a fonte de verdade. Não fazer merge de código do rascunho sem verificação de conformidade.
- **Plano de contingência**: descartar componentes Vue do rascunho problemático e reescrever a partir das specs do Screen Translator.
- **Owner**: Igor Zanin
- **Status**: aberto

---

### RISK-003 — Lógica de negócio implícita não documentada
- **Descrição**: Regras de negócio do Focalboard que nunca foram documentadas (edge cases de propriedades, comportamento de ordenação com valores nulos, grupos dinâmicos vazios) podem só aparecer em uso real, após o go-live.
- **Categoria**: técnico
- **Probabilidade**: média
- **Impacto**: médio
- **Severidade combinada**: 🟡 MÉDIA
- **Trigger / sinal de alerta**: usuário reportando comportamento inesperado em features de board/card após go-live; comparação entre Focalboard e Nexo revelando inconsistências não previstas nos parity tests.
- **Mitigação**: incluir testes exploratórios (não apenas Gherkin) na fase de validação; usar Focalboard legado como oráculo durante os testes (rodar ambos simultaneamente e comparar output para os mesmos inputs).
- **Plano de contingência**: patches pós-go-live — o sistema novo é o único em uso, então correções não precisam de coordenação com sistema legado.
- **Owner**: Igor Zanin + time interno (usuários como testadores)
- **Status**: aberto

---

### RISK-004 — Bootstrap double import causando bug de produção
- **Descrição**: Bootstrap 5.3 está sendo importado via CDN (index.html) e via npm (main.ts). Em produção, isso causa: estilos duplicados, JS conflitante (tooltips/dropdowns inicializados duas vezes), e builds maiores que o necessário.
- **Categoria**: técnico
- **Probabilidade**: alta (já existente)
- **Impacto**: médio
- **Severidade combinada**: 🟠 ALTA
- **Trigger / sinal de alerta**: componentes Bootstrap (tooltips, dropdowns, modais) se comportando erraticamente; console.warn de inicialização duplicada; bundle size anômalo.
- **Mitigação**: remover import CDN do `index.html` antes do primeiro sprint de frontend. Manter apenas npm para builds reproduzíveis. Ação imediata e de baixo custo.
- **Plano de contingência**: se já tiver causado divergências de estilo, executar `npm run build` e inspecionar bundle para confirmar single source.
- **Owner**: Igor Zanin
- **Status**: aberto (REF-006 em ambiguity_log.md)

---

### RISK-005 — Dependency única: desenvolvedor solo
- **Descrição**: Igor é o único desenvolvedor. Qualquer ausência prolongada ou sobrecarga paralela pode atrasar ou bloquear a migração indefinidamente.
- **Categoria**: organizacional
- **Probabilidade**: baixa
- **Impacto**: crítico
- **Severidade combinada**: 🟠 ALTA
- **Trigger / sinal de alerta**: ausência de commits por > 2 semanas; mudança de prioridades de negócio; restrições de tempo externas.
- **Mitigação**: manter specs Reversa atualizadas (qualquer novo desenvolvedor pode retomar a partir dos artefatos); checkpoints frequentes para que o estado seja retomável; não deixar estado "mental" fora dos artefatos documentados.
- **Plano de contingência**: onboarding de segundo desenvolvedor usando os artefatos do Reversa como único documento de entrada; Focalboard legado como fallback operacional enquanto o time não estiver completo.
- **Owner**: Time / Igor Zanin
- **Status**: aceito (risco conhecido de equipe pequena)

---

### RISK-006 — Editor markdown sem library definida
- **Descrição**: AMB-004 resolveu que live-markdown-plugin será substituído por melhor library, mas a library específica ainda não foi escolhida. Atrasar essa decisão pode bloquear implementação de cards com conteúdo rich e criar retrabalho se a library escolhida tardiamente for incompatível com a arquitetura de componentes Vue já implementada.
- **Categoria**: técnico
- **Probabilidade**: média
- **Impacto**: médio
- **Severidade combinada**: 🟡 MÉDIA
- **Trigger / sinal de alerta**: fase de frontend iniciada sem library escolhida; componente de edição de card implementado com textarea simples como placeholder e nunca substituído.
- **Mitigação**: decidir library antes de iniciar fase de frontend (Designer deve recomendar baseado nas features necessárias: texto, imagens, headings, checkbox lists, code blocks). Candidatos: `tiptap` (Vue-native, extensível), `md-editor-v3` (Vue 3, Bootstrap-friendly), `milkdown` (ProseMirror-based, Vue plugin).
- **Plano de contingência**: se library escolhida apresentar problemas de integração com Bootstrap 5.3, fallback para `textarea` com preview via `marked.js` (funcional, se não ideal em UX).
- **Owner**: Igor Zanin
- **Status**: aberto (pendente decisão no Designer)

---

### RISK-007 — Scheduler de sessões não implementado
- **Descrição**: AMB-002 resolveu implementar scheduler de cleanup, mas se não for feito, a tabela `sessions` cresce indefinidamente com tokens expirados, podendo causar degradação de performance em queries de auth em longo prazo.
- **Categoria**: técnico
- **Probabilidade**: baixa (problema latente, não imediato)
- **Impacto**: médio (performance gradual, não crash)
- **Severidade combinada**: 🟡 MÉDIA
- **Trigger / sinal de alerta**: tabela `sessions` com > 10.000 registros; tempo de response dos endpoints de auth aumentando.
- **Mitigação**: implementar no mesmo sprint de auth (`lifespan` FastAPI + `asyncio.create_task`). Simples e não bloqueante.
- **Plano de contingência**: migração Alembic para adicionar TTL ou índice em `expires_at`; script manual de cleanup.
- **Owner**: Igor Zanin
- **Status**: aberto

---

### RISK-008 — Testes de sharing (readToken) ausentes
- **Descrição**: AMB-001 resolveu implementar `test_sharing.py`, mas se a cobertura não for criada durante o sprint de auth/sharing, o fluxo de board sharing pode ter regressões silenciosas não detectadas.
- **Categoria**: técnico
- **Probabilidade**: baixa (se a decisão for honrada)
- **Impacto**: médio
- **Severidade combinada**: 🟡 MÉDIA
- **Trigger / sinal de alerta**: merge de auth sem `test_sharing.py`; link de sharing gerando 404/403 inesperado.
- **Mitigação**: incluir `test_sharing.py` como critério de go no checklist de go/no-go para o módulo de auth.
- **Plano de contingência**: regressão manual do fluxo antes de go-live usando Focalboard como referência de comportamento esperado.
- **Owner**: Igor Zanin
- **Status**: aberto

---

### RISK-009 — Nextcloud Deck: implementação de token auth mais complexa que o esperado
- **Descrição**: AMB-003 resolveu implementar suporte a token API para Nextcloud Deck. O formato exato do token e o endpoint de auth do Nextcloud podem variar entre versões, tornando a implementação mais trabalhosa que o previsto.
- **Categoria**: técnico
- **Probabilidade**: baixa
- **Impacto**: baixo
- **Severidade combinada**: 🟢 BAIXA
- **Trigger / sinal de alerta**: documentação Nextcloud API inconsistente entre versões; auth por token funcionando em uma versão mas não em outra.
- **Mitigação**: testar contra Nextcloud 28.x+ (versão atual). Usar `Authorization: Bearer <token>` como padrão (suportado desde NC 27). Documentar versão mínima suportada.
- **Plano de contingência**: documentar limitação e manter user/password como fallback — já funcional.
- **Owner**: Igor Zanin
- **Status**: aberto

---

### RISK-010 — Divergência design legado vs. novo (UX regression)
- **Descrição**: O Focalboard usa dark sidebar + kanban visual com cards coloridos. O webapp atual usa Bootstrap light theme. Usuários que migrarem do Focalboard podem ter dificuldade de adaptação, ou funcionalidades de UX (drag-drop, hover states, keyboard navigation) podem ter regressão comportamental.
- **Categoria**: operacional
- **Probabilidade**: média
- **Impacto**: médio
- **Severidade combinada**: 🟡 MÉDIA
- **Trigger / sinal de alerta**: usuários reportando dificuldade em localizar funcionalidades após go-live; drag-and-drop de cards com comportamento diferente do esperado.
- **Mitigação**: Screen Translator documenta mapeamento tela-por-tela legado→novo; desvios intencionais são registrados em `screen_deviation_log.md`; testar UX com usuários antes de go-live.
- **Plano de contingência**: ajustes de UX pós-go-live são de baixo risco (não afetam dados ou lógica de negócio).
- **Owner**: Igor Zanin + time interno
- **Status**: aberto

---

## Resumo por severidade

| Severidade | Quantidade | IDs |
|---|---|---|
| Crítica 🔴 | 1 | RISK-001 |
| Alta 🟠 | 3 | RISK-002, RISK-004, RISK-005 |
| Média 🟡 | 4 | RISK-003, RISK-006, RISK-007, RISK-010 |
| Baixa 🟢 | 2 | RISK-008, RISK-009 |

---

## Riscos relacionados ao paradigma alvo

> O Paradigm Advisor confirmou **gap = NONE**. Não há riscos derivados diretamente de mudança de paradigma nesta migração.
>
> A transição Go→Python e React+Redux→Vue3+Pinia foi decisão anterior ao pipeline e já está parcialmente executada. O risco técnico associado à mudança de paradigma está **absorvido** pelo RISK-002 (webapp rascunho com código parcial que pode divergir do paradigma OO com DI correto).

| ID | Descrição |
|---|---|
| — | Nenhum risco de paradigma identificado |
