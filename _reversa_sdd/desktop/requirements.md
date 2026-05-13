# Desktop — Electron + Vue 3

## Visão Geral
Aplicação desktop cross-platform construída com Electron, substituindo os 3 aplicativos nativos do legado (macOS Swift/WKWebView, Windows C# WPF/WebView2, Linux Go/webview). Embute o servidor FastAPI como subprocesso e abre uma janela Vue 3.

## Stack

| Componente | Tecnologia |
|------------|-----------|
| Framework | Electron 30+ |
| Frontend | Vue 3 (mesmo webapp) |
| Backend embutido | FastAPI via subprocess |
| Build | electron-builder |

## Responsabilidades
- Iniciar servidor FastAPI em porta livre como subprocesso
- Abrir janela nativa com a SPA Vue 3
- Gerenciar ciclo de vida (startup, shutdown, cleanup)
- Suporte a single-user token (herdado do legado)
- Suporte a arrastar/soltar arquivos
- Atalhos de teclado (Cmd+Q, Cmd+W)

## Funcionalidades

| Funcionalidade | Descrição | Prioridade |
|---------------|-----------|-----------|
| Iniciar servidor Python embutido | Subprocesso uvicorn em porta livre | Must |
| Janela principal | BrowserWindow com SPA Vue 3 | Must |
| Single-user token | Token "su-" + UUID para auto-login | Must |
| Arrastar/soltar arquivos | Upload via drag-and-drop | Should |
| Auto-update | electron-updater | Could |
| Bandeja de sistema | System tray com menu | Could |

## Rastreabilidade

| Funcionalidade | Fonte legado | Confiança |
|---------------|-------------|-----------|
| Servidor embutido | `linux/main.go` | 🟢 |
| Porta livre | `mac/PortUtils.swift` | 🟢 |
| Single-user token | `linux/main.go:30` | 🟢 |
| Drag-and-drop | `mac/CustomWKWebView.swift` | 🟢 |
