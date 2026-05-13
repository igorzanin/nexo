# Desktop, Design Técnico

## Estrutura

```
nexo/desktop/
├── package.json
├── electron/
│   ├── main.ts          # Electron main process
│   ├── preload.ts       # Preload script
│   └── server.ts        # FastAPI subprocess manager
├── build/
│   └── icon.png         # App icon
└── electron-builder.yml # Build config
```

## Main Process

```typescript
// electron/main.ts
import { app, BrowserWindow } from 'electron'
import { startServer, stopServer } from './server'

let mainWindow: BrowserWindow | null = null

async function createWindow() {
  const port = await startServer()
  const token = generateSingleUserToken()

  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
    }
  })

  mainWindow.loadURL(`http://localhost:${port}?token=${token}`)
}

app.on('ready', createWindow)
app.on('window-all-closed', async () => {
  await stopServer()
  app.quit()
})
```

## Server Manager

```typescript
// electron/server.ts
import { spawn, ChildProcess } from 'child_process'
import net from 'net'

let serverProcess: ChildProcess | null = null

async function getFreePort(): Promise<number> {
  return new Promise((resolve) => {
    const server = net.createServer()
    server.listen(0, () => {
      const port = (server.address() as net.AddressInfo).port
      server.close(() => resolve(port))
    })
  })
}

async function startServer(): Promise<number> {
  const port = await getFreePort()
  const pythonPath = process.platform === 'win32' ? 'python' : 'python3'

  serverProcess = spawn(pythonPath, [
    '-m', 'uvicorn', 'nexo.main:app',
    '--host', 'localhost',
    '--port', String(port),
  ])

  return port
}

async function stopServer() {
  if (serverProcess) {
    serverProcess.kill()
    serverProcess = null
  }
}

function generateSingleUserToken(): string {
  return `su-${uuidv4()}`
}
```

## Dependências Node.js
- `electron`
- `electron-builder`
- `uuid`

## Build

```yaml
# electron-builder.yml
appId: com.nexo.desktop
productName: Nexo
directories:
  output: dist
files:
  - electron/**/*
  - "!node_modules"
mac:
  target: dmg
win:
  target: nsis
linux:
  target: AppImage
```
