# Desktop, Tarefas de Implementação

## Tarefas

- [ ] T-01, Configurar projeto Electron com TypeScript
  - package.json, tsconfig, electron-builder.yml

- [ ] T-02, Implementar ServerManager (start, stop, getFreePort, singleUserToken)
  - Fonte legado: `linux/main.go`, `mac/PortUtils.swift`

- [ ] T-03, Implementar MainWindow (BrowserWindow + load SPA)
  - Fonte legado: `mac/ViewController.swift`, `win-wpf/MainWindow.xaml.cs`

- [ ] T-04, Implementar auto-login com single-user token
  - Fonte legado: `linux/main.go` (token "su-" + UUID)

- [ ] T-05, Implementar drag-and-drop de arquivos
  - Fonte legado: `mac/CustomWKWebView.swift`

- [ ] T-06, Implementar atalhos de teclado (Cmd+Q, Cmd+W)
  - Fonte legado: `mac/AppDelegate.swift`

- [ ] T-07, Configurar build para macOS, Windows e Linux
  - electron-builder com targets dmg, nsis, AppImage
