# Servidor Web, Tarefas de Implementação

## Tarefa

- [ ] T-01, Configurar FastAPI static files + SPA catch-all
  - Fonte legado: `server/web/webserver.go`
  - Critério: `/static/*` serve arquivos do diretório dist; fallback para index.html

## Decisões
- ReadHeaderTimeout: implementado via uvicorn (`--timeout-keep-alive`) ✅
- SSL/TLS: mantido via uvicorn (`--ssl-keyfile`/`--ssl-certfile`)
- localOnly: mantido via `--host localhost`
