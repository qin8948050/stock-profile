/**
 * 通用 API 响应模型
 * @template T - data 字段的类型
 */
export type ApiResponse<T> = {
  status: number; // 业务状态码, 200 表示成功
  msg: string; // 响应消息
  data: T | null; // 响应数据
};