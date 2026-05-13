# C4 Containers Diagram — nexo

> 🟢 CONFIRMADO

```
┌─────────────────────────────────────────────────────────────────────┐
│  Usuário (Browser / Electron)                                       │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────────┐
│                        nexo (Software System)                        │
│                                                                      │
│  ┌──────────────────────┐     ┌──────────────────────────────────┐   │
│  │  Vue 3 SPA            │◄───►│  FastAPI Server                 │   │
│  │  [Container]          │     │  [Container]                    │   │
│  │                       │     │  REST + WebSocket               │   │
│  │  • Vue 3 + Pinia      │     │  ┌────────────────────────┐    │   │
│  │  • Vue Router         │     │  │  FastAPI Routers       │    │   │
│  │  • Bootstrap 5.3      │     │  │  (REST handlers)       │    │   │
│  │  • Vite build         │     │  ├────────────────────────┤    │   │
│  │  • @fullcalendar/vue3 │     │  │  Services Layer        │    │   │
│  │  • vuedraggable       │     │  │  (business logic)      │    │   │
│  └───────────────────────┘     │  ├────────────────────────┤    │   │
│                                │  │  Repositories Layer    │    │   │
│  ┌──────────────────────┐      │  │  (SQLAlchemy)          │    │   │
│  │  Electron Desktop     │      │  ├────────────────────────┤    │   │
│  │  [Container]          │      │  │  SQLAlchemy Models     │    │   │
│  │                       │      │  └────────────────────────┘    │   │
│  │  • Electron 30+       │      └────────────────────────────────┘   │
│  │  • Embutido:          │                      │                    │
│  │    subprocess         │                      ▼                    │
│  │    FastAPI server     │     ┌──────────────────────────────────┐   │
│  │  • Janela Vue 3       │     │  Database                        │   │
│  └───────────────────────┘     │  [Container]                     │   │
│                                │  SQLite / PostgreSQL / MySQL     │   │
│  ┌───────────────────────┐     └──────────────────────────────────┘   │
│  │  Importadores CLI     │                                            │
│  │  [Container]          │                                            │
│  │  TypeScript (Node.js) │                                            │
│  │  Gera .boardarchive   │                                            │
│  └───────────────────────┘                                            │
└──────────────────────────────────────────────────────────────────────┘
```

## Notas

- O FastAPI Server serve tanto a API REST quanto os arquivos estáticos da SPA em produção
- Em desenvolvimento, o Vite dev server atua como proxy reverso para o FastAPI
- O Electron Desktop inicia o servidor FastAPI como subprocesso e abre uma janela apontando para `localhost`
- Os importadores CLI são independentes, rodam em Node.js e geram arquivos `.boardarchive`
