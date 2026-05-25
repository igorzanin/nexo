import { contextBridge, ipcRenderer } from "electron";

contextBridge.exposeInMainWorld("electronAPI", {
  getToken: () => ipcRenderer.invoke("get-token"),
  getPort: () => ipcRenderer.invoke("get-port"),
  onFileDrop: (callback: (files: string[]) => void) => {
    ipcRenderer.on("file-dropped", (_event, files: string[]) => callback(files));
  },
});
