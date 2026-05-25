import { spawn, ChildProcess } from "child_process";
import net from "net";
import path from "path";
import { v4 as uuidv4 } from "uuid";

let serverProcess: ChildProcess | null = null;

function getFreePort(): Promise<number> {
  return new Promise((resolve, reject) => {
    const server = net.createServer();
    server.listen(0, "127.0.0.1", () => {
      const addr = server.address() as net.AddressInfo;
      const port = addr.port;
      server.close(() => resolve(port));
    });
    server.on("error", reject);
  });
}

function generateSingleUserToken(): string {
  return `su-${uuidv4()}`;
}

async function startServer(): Promise<number> {
  const port = await getFreePort();
  const pythonCmd = process.platform === "win32" ? "python" : "python3";

  const projectRoot = path.resolve(__dirname, "..", "..");

  serverProcess = spawn(pythonCmd, [
    "-m", "uvicorn", "nexo.main:app",
    "--host", "127.0.0.1",
    "--port", String(port),
    "--log-level", "info",
  ], {
    cwd: projectRoot,
    stdio: ["ignore", "pipe", "pipe"],
  });

  serverProcess.stdout?.on("data", (data: Buffer) => {
    console.log(`[server] ${data.toString().trim()}`);
  });

  serverProcess.stderr?.on("data", (data: Buffer) => {
    console.error(`[server] ${data.toString().trim()}`);
  });

  serverProcess.on("exit", (code) => {
    console.log(`[server] exited with code ${code}`);
    serverProcess = null;
  });

  await new Promise<void>((resolve) => setTimeout(resolve, 2000));
  return port;
}

async function stopServer(): Promise<void> {
  if (serverProcess) {
    serverProcess.kill("SIGTERM");
    serverProcess = null;
  }
}

export { startServer, stopServer, generateSingleUserToken };
