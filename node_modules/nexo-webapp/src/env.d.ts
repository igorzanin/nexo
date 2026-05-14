/// <reference types="vite/client" />

declare module "*.vue" {
  import type { DefineComponent } from "vue";
  const component: DefineComponent<object, object, unknown>;
  export default component;
}

interface Window {
  electronAPI?: {
    getToken: () => Promise<string>;
    getPort: () => Promise<number>;
    onFileDrop: (callback: (files: string[]) => void) => void;
  };
}
