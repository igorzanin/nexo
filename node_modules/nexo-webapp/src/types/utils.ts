export function generateId(): string {
  return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0;
    const v = c === "x" ? r : (r & 0x3) | 0x8;
    return v.toString(16);
  });
}

export function currentTimestamp(): number {
  return Date.now();
}

export function clone<T>(obj: T): T {
  return JSON.parse(JSON.stringify(obj));
}
