# Servidor Web — obsoleto (fundido no FastAPI)

## Status

**Unit obsoleta.** O servidor web não é mais um componente separado.

No Go legado, `server/web/` era um wrapper HTTP que servia arquivos estáticos da SPA React. No novo stack, o **próprio FastAPI** serve os arquivos estáticos do frontend Vue 3 em produção.

## Substituição

| Função legada | Novo componente |
|--------------|----------------|
| Servir arquivos estáticos (`/static/*`) | `FastAPI.mount("/static", StaticFiles(directory="dist"), ...)` |
| Servir SPA index.html com BaseURL injetada | Vue Router history mode + FastAPI catch-all |
| Registrar rotas via RoutedService | FastAPI routers (incluídos diretamente) |
| SSL/TLS opcional | Uvicorn + `--ssl-keyfile` / `--ssl-certfile` |
| ReadHeaderTimeout | Configurado no uvicorn (`--timeout-keep-alive`) |

## Configuração Uvicorn

```python
# main.py
app.mount("/static", StaticFiles(directory="../webapp/dist"), name="static")

@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    return FileResponse("../webapp/dist/index.html")
```

```bash
# Produção
uvicorn nexo.main:app --host 0.0.0.0 --port 8000 --timeout-keep-alive 5
```

## Decisões
- SSL/TLS mantido (via uvicorn)
- ReadHeaderTimeout implementado via uvicorn
- localOnly (bind localhost) mantido via arg --host
