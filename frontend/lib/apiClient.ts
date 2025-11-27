"use client";

export const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000/api";

export interface ApiResponse<T = any> {
  status: number;
  msg: string;
  data?: T | null;
}

async function parseApiResponse<T = any>(res: Response): Promise<T> {
  const contentType = res.headers.get("content-type") || "";
  if (!contentType.includes("application/json")) {
    throw new Error(`Unexpected content-type: ${contentType}`);
  }
  const body: ApiResponse<T> = await res.json();
  if (body.status !== 200) {
    const err = new Error(body.msg || "API error");
    // @ts-ignore attach status
    err.status = body.status;
    throw err;
  }
  return (body.data as T) ?? (null as any);
}

type RequestInitEx = RequestInit & { skipJsonParse?: boolean };

export class ApiClient {
  base: string;

  constructor(base = API_BASE) {
    this.base = base.replace(/\/$/, "");
  }

  private url(path: string) {
    if (path.startsWith("/")) path = path.slice(1);
    return `${this.base}/${path}`;
  }

  async request<T = any>(path: string, init?: RequestInitEx): Promise<T> {
    const res = await fetch(this.url(path), init);
    if (!res.ok) {
      try {
        const body = await res.json();
        throw new Error(body?.msg || `HTTP ${res.status}`);
      } catch (e) {
        throw new Error(`HTTP ${res.status}`);
      }
    }
    if (init?.skipJsonParse) {
      return (undefined as unknown) as T;
    }

    return parseApiResponse<T>(res);
  }

  /**
   * Fetch and return the raw ApiResponse object { status, msg, data }.
   * Does not throw when api.status !== 200; returns the parsed body for callers to inspect msg.
   */
  async requestRaw<T = any>(path: string, init?: RequestInitEx): Promise<ApiResponse<T>> {
    const res = await fetch(this.url(path), init);
    const contentType = res.headers.get("content-type") || "";
    if (!contentType.includes("application/json")) {
      throw new Error(`Unexpected content-type: ${contentType}`);
    }
    const body: ApiResponse<T> = await res.json();
    return body;
  }

  resource(name: string) {
    const base = name.replace(/^\//, "");
    return {
      list: <T = any>(params?: Record<string, any>) => {
        const qs = params
          ? "?" + new URLSearchParams(Object.entries(params).map(([k, v]) => [k, String(v)])).toString()
          : "";
        return this.request<T>(`${base}${qs}`);
      },
      get: <T = any>(id: number | string) => this.request<T>(`${base}/${id}`),
      create: <T = any>(payload: any) =>
        this.request<T>(`${base}/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),}),
      update: <T = any>(id: number | string, payload: any) =>{
        return this.request<T>(`${base}/${id}`, {
                  method: "PUT",
                  headers: { "Content-Type": "application/json" },
                  body: JSON.stringify(payload),
                })
      },
      delete: <T = any>(id: number | string) => this.request<T>(`${base}/${id}`, { method: "DELETE" }),
    };
  }
}

// default client instance
const defaultClient = new ApiClient(API_BASE);
export default defaultClient;
