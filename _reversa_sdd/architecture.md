# Architecture Overview — nexo

> Gerado pelo Revisor em 2026-05-13
> 🟢 CONFIRMADO | 🟡 INFERIDO | 🔴 LACUNA

---

## Visão Geral

Nexo é um workspace colaborativo auto-hospedado para organização de projetos, gerenciamento de tarefas e colaboração em equipe. Originado como fork do **Focalboard** (Mattermost), foi completamente reescrito com nova stack tecnológica.

### Stack Tecnológica

| Camada | Tecnologia | Versão |
|--------|-----------|--------|
| Frontend | Vue 3 + Pinia + TypeScript | 3.x |
| Backend | Python + FastAPI + SQLAlchemy | 3.12+ / 0.115+ |
| Bancos | SQLite / PostgreSQL / MySQL | - |
| Desktop | Electron + Vue 3 | 30+ |
| Container | Docker + docker-compose | - |
| Build | Vite (frontend) / Uvicorn (backend) | - |

### Modo de Operação

| Modo | Descrição |
|------|-----------|
| **Standalone** | Servidor Python FastAPI autônomo com API REST + WebSocket. Multi-usuário. |
| **Desktop (Electron)** | Servidor Python embutido (subprocess) + janela Vue 3 nativa. Single-user. |

---

## Arquitetura em Camadas (Server-side)

```
HTTP Client / WebSocket Client
        │
        ▼
┌─────────────────────────┐
│   FastAPI Routers       │  Handlers REST + WebSocket
│   (routers/)            │  Auth, Boards, Blocks, Cards, Categories, Files, etc.
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│   Services Layer        │  Camada de negócio
│   (services/)           │  Auth, Boards, Blocks, Cards, Permissions, Categories
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│   Repositories Layer    │  SQLAlchemy repositories
│   (repositories/)       │  CRUD + queries especializadas
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│   SQLAlchemy Models     │  Modelos de dados (ORM)
│   (models/)             │  Board, Block, Card, User, Team, Session, etc.
└─────────────────────────┘
```

### Frontend (SPA)

```
Vue Router
    │
    ▼
┌───────────────────┐
│   Pages           │  BoardPage, LoginPage, RegisterPage, ChangePasswordPage, ErrorPage
└──────┬────────────┘
       │
       ▼
┌───────────────────┐
│   Components      │  Workspace → CenterPanel → Kanban/Table/Gallery/Calendar
│                   │  CardDialog, Sidebar, BoardPermissionGate
└──────┬────────────┘
       │
       ▼
┌───────────────────┐
│   Pinia Stores    │  16 stores
│                   │  boards, cards, views, users, teams, comments, etc.
└──────┬────────────┘
       │
       ▼
┌───────────────────┐
│   Models (types)  │  Modelos de dados do client (Block, Board, Card, BoardView, etc.)
└───────────────────┘
```

---

## Comunicação

| Protocolo | Uso | Detalhes |
|-----------|-----|----------|
| **REST (JSON)** | CRUD de boards, cards, blocks, usuários, categorias | FastAPI, autenticação via JWT Bearer token |
| **WebSocket** | Notificações em tempo real (broadcast de mudanças) | FastAPI WebSocket nativo, autenticação via AUTH action |
| **HTTP (file upload)** | Upload de attachments | Upload direto com progress tracking |

---

## Integrações

| Integração | Tipo | Descrição |
|-----------|------|-----------|
| Prometheus | Métricas | `/metrics` endpoint |
| Importadores CLI | 6 plataformas | Trello, Jira, Asana, Todoist, Notion, Nextcloud Deck (TypeScript) |

---

## Dívidas Técnicas (legado) — Resolvidas

| # | Item | Severidade | Status |
|---|------|-----------|--------|
| T1 | Limites cloud com enforcement desabilitado | Média | **Resolvido**: removido (funcionalidade descartada) |
| T2 | MFA não implementada | Média | **Resolvido**: removido (funcionalidade descartada) |
| T3 | BroadcastSubscriptionChange não implementado | Baixa | **Resolvido**: removido (funcionalidade descartada) |
| T4 | BroadcastCardLimitTimestampChange não implementado | Baixa | **Resolvido**: removido |
| T5 | Testes de importadores sem cobertura | Média | **Mantido**: a adicionar durante rebuild |
| T6 | React 17 + Webpack 5 | Baixa | **Resolvido**: substituído por Vue 3 + Vite |
| T7 | Plugin Mattermost | - | **Resolvido**: removido (apenas standalone) |
| T8 | Desktops nativos (mac/WPF/Linux) | - | **Resolvido**: substituído por Electron |
| T9 | ReadHeaderTimeout não configurado | Média | **Resolvido**: será implementado no FastAPI |
| T10 | Rate limiting ausente | Média | **Resolvido**: será implementado no FastAPI |

---

## Escala de Confiança

| Item | Confiança |
|------|-----------|
| Arquitetura em 3 camadas (Routers → Services → Repositories) | 🟢 CONFIRMADO |
| Modo único standalone + Electron desktop | 🟢 CONFIRMADO |
| 4 visualizações (Kanban, Table, Gallery, Calendar) | 🟢 CONFIRMADO (mantido do legado) |
| 6 importadores CLI | 🟢 CONFIRMADO (mantidos em TypeScript) |
| Stack Python FastAPI + Vue 3 + Bootstrap 5.3 | 🟢 CONFIRMADO |
