import path from "path";
import { app, BrowserWindow, ipcMain, globalShortcut } from "electron";
import { startServer, stopServer, generateSingleUserToken } from "./server";

let mainWindow: BrowserWindow | null = null;
let serverPort = 0;
let singleUserToken = "";

async function createWindow() {
  serverPort = await startServer();
  singleUserToken = generateSingleUserToken();

  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    minWidth: 800,
    minHeight: 600,
    title: "Nexo",
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      nodeIntegration: false,
      contextIsolation: true,
    },
  });

  mainWindow.loadURL(`http://127.0.0.1:${serverPort}/?token=${singleUserToken}`);

  mainWindow.on("closed", () => {
    mainWindow = null;
  });

  ipcMain.handle("get-token", () => singleUserToken);
  ipcMain.handle("get-port", () => serverPort);
}

app.on("ready", () => {
  createWindow();

  globalShortcut.register("CommandOrControl+Q", () => {
    app.quit();
  });
});

app.on("window-all-closed", async () => {
  globalShortcut.unregisterAll();
  await stopServer();
  app.quit();
});

app.on("activate", () => {
  if (mainWindow === null) {
    createWindow();
  }
});

app.on("will-quit", async () => {
  await stopServer();
});
