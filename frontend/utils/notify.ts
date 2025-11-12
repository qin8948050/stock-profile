import { message } from "antd";

function extractMessage(input: any, fallback?: string) {
  if (!input && fallback) return fallback;
  if (typeof input === "string") return input;
  if (input instanceof Error) return input.message || fallback || "操作失败";
  if (input && typeof input === "object") return input.message || fallback || String(input);
  return fallback || "操作失败";
}

export const notify = {
  success: (msg?: string) => {
    message.success(msg || "操作成功");
  },
  error: (err?: any, fallback?: string) => {
    const text = extractMessage(err, fallback);
    message.error(text);
    // optional: console.debug the error for developers
    if (err && err instanceof Error) console.debug(err.stack || err.message);
  },
  info: (msg?: string) => {
    message.info(msg || "提示");
  },
  warn: (msg?: string) => {
    message.warning(msg || "警告");
  },
};

export default notify;
