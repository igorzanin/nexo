# C4 Context Diagram — nexo

> 🟢 CONFIRMADO

```
┌─────────────────────────────────────────────────────────────┐
│                     nexo (Software System)                   │
│  Workspace colaborativo auto-hospedado para organização      │
│  de projetos e gerenciamento de tarefas                      │
└──────────┬────────────────────────────────┬──────────────────┘
           │                                │
           ▼                                ▼
┌──────────────────────┐    ┌──────────────────────────┐
│   Usuário            │    │   Administrador           │
│   [Person]           │    │   [Person]                │
│   Acessa boards,     │    │   Gerencia config,        │
│   cards e views      │    │   métricas e usuários     │
│   via browser ou     │    │   via API admin           │
│   Electron desktop   │    │                           │
└──────────────────────┘    └──────────────────────────┘
           │
           ▼
┌──────────────────────────┐
│   Importadores CLI       │
│   [Software System]      │
│   6 tools (TypeScript)   │
│   Trello, Jira, Asana,   │
│   Todoist, Notion,       │
│   Nextcloud Deck         │
└──────────────────────────┘
```

## Integrações Externas

| Sistema | Tipo | Descrição |
|---------|------|-----------|
| Prometheus | API / Metrics | Coleta métricas do servidor via `/metrics` |
| SQLite / PostgreSQL / MySQL | Database | Armazenamento persistente via SQLAlchemy |
| Importadores CLI | CLI | Ferramentas autônomas para importar de 6 plataformas |
