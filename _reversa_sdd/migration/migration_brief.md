---
schemaVersion: 1
generatedAt: 2026-05-24T16:41:57-03:00
reversa:
  version: "1.0.0"
kind: migration_brief
producedBy: orchestrator
hash: "sha256:f015fd928f6167f53365b14462c908890819c68f989f5ac2b88d3b4c3c0fa0aa"
---

# Migration Brief

> Documento de critério de migração coletado em entrevista no início do `/reversa-migrate`.
> Consumido pelos seis agentes do Time de Migração.

## Objetivo da migração

A aplicação legada (Focalboard — React 17 + Redux Toolkit + servidor Go) está sendo substituída por uma nova stack moderna composta por **Vue 3 + Vite + Bootstrap 5.3** no frontend e **FastAPI (Python)** no backend.

A migração já foi iniciada, porém está incompleta: diversas telas ainda não foram documentadas, houve tentativas parciais de implementação sem especificação formal, e grande parte do código existente no `webapp/` precisa ser revisado e em boa parte refeito.

**Objetivo principal**: Ter o sistema novo **funcionalmente equivalente** ao Focalboard legado, porém **standalone** (sem qualquer dependência ou integração com o Mattermost), com máximo uso de **componentes nativos do Bootstrap 5.3** (modais, offcanvas, dropdowns, toasts, etc.). O design não precisa ser idêntico ao legado — melhorias, otimizações e modernizações de UX são bem-vindas, desde que o comportamento funcional seja preservado.

## Métricas de sucesso

- **Paridade funcional completa**: todos os fluxos do Focalboard (boards, cards, grupos, usuários, propriedades, filtros, ordenação, views) funcionam no sistema novo, exceto a integração com Mattermost.
- **Standalone**: aplicação roda de forma autônoma sem nenhuma dependência de plugin ou plataforma externa.
- **Bootstrap-nativo**: componentes de UI (modais, dropdowns, offcanvas, toasts, badges) usam as implementações Bootstrap 5.3 em vez de implementações customizadas.
- **Nenhuma tela crítica quebrada**: não existe fluxo funcional do legado que ficou sem equivalente no sistema novo.

## Restrições

- **Prazo**: sem restrição definida.
- **Orçamento**: sem restrição definida.
- **Técnicas**: nenhuma restrição de API externa, contrato ou regulatória.
- **Operacionais**: sem SLA ou janela de manutenção definidos.

## Fatores de risco conhecidos

- **Sistema incompleto**: o webapp atual (`webapp/`) tem implementações parciais que podem conflitar com as specs geradas pelos agentes. O maior risco é entregar um sistema não funcional ou com fluxos ausentes.
- **Divergência legado × novo**: as telas documentadas pelo `reversa-visor` mostram o Focalboard legado (dark sidebar, badges, kanban), enquanto o webapp atual usa Bootstrap light theme. Há gap de design e comportamento a reconciliar.
- **Dupla importação de Bootstrap** (CDN + npm) no `webapp/` — potencial bug de produção.
- **Lógica de negócio implícita**: regras de negócio do Focalboard (tipos de propriedade, views configuráveis, grupos dinâmicos) podem ter comportamentos não documentados que só aparecem em uso real.

## Stakeholders

| Nome / papel | Responsabilidade na migração |
|---|---|
| Time interno | Usuários finais e revisores do sistema novo |
| Igor Zanin (dev) | Implementação, decisões técnicas e arquiteturais |

## Stack alvo

- **Linguagem (frontend)**: JavaScript / TypeScript com Vue 3.4
- **Framework (frontend)**: Vue 3 + Vite 5 + Bootstrap 5.3.3 + Pinia
- **Linguagem (backend)**: Python 3.x
- **Framework (backend)**: FastAPI
- **Banco**: PostgreSQL 16 (via parâmetros `.env`) com fallback para SQLite quando não parametrizado
- **Mensageria**: nenhuma
- **Infra**: local / on-premise
- **Auth**: standalone — JWT ou session própria (sem Mattermost)
- **Outros**: sem cache externo, sem mensageria, sem gateway

## Escopo declarado

- **Incluído**: todos os módulos do Focalboard — boards, cards, grupos, propriedades customizadas, views (kanban, tabela, galeria), filtros, ordenação, templates, auth (login/registro), gerenciamento de usuários.
- **Excluído**: integração com Mattermost (plugin mode, webhooks, auth via Mattermost). A aplicação deve ser totalmente standalone.

## Notas livres

- O `webapp/` já existe mas está em estado de rascunho: código presente não deve ser considerado como "implementação correta" — os agentes devem trabalhar a partir das specs do `_reversa_sdd/` e gerar especificações do que o sistema **deve** ser, independentemente do que já foi codificado.
- Preferência explícita por componentes nativos Bootstrap 5.3 (modal, offcanvas, dropdown, toast, badge, form-switch) em vez de implementações Vue customizadas para os mesmos padrões.
- Design pode ser modernizado; comportamento deve ser preservado (exceto Mattermost).
- `reversa-visor` documentou 15 telas do legado em `_reversa_sdd/ui/inventory.md` e `_reversa_sdd/componentes/screens.md` — os agentes Screen Translator e Designer devem consumir esses artefatos.
- `reversa-design-system` documentou o Bootstrap 5.3 como sistema de design base em `_reversa_sdd/design-system/`.
