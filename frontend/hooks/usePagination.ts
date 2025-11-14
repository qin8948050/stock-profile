"use client";

import { useState, useCallback, useEffect } from 'react';
import type { TablePaginationConfig } from 'antd/es/table';
import notify from '../utils/notify';

interface PaginatedResponse<T> {
  items: T[];
  total: number;
}

export type Fetcher<T> = (params: { page: number; size: number;[key: string]: any }) => Promise<PaginatedResponse<T>>;

export function usePagination<T>(fetcher: Fetcher<T>, initialPage=1,initialPageSize = 10) {
  const [data, setData] = useState<T[]>([]);
  const [loading, setLoading] = useState(false);
  const [pagination, setPagination] = useState<TablePaginationConfig>({
    current: initialPage,
    pageSize: initialPageSize,
    total: 0,
    showTotal: (total, range) => `${range[0]}-${range[1]} 共 ${total} 条`,
  });

  const load = useCallback(async (currentPagination: TablePaginationConfig, filters?: Record<string, any>) => {
    setLoading(true);
    try {
      const page = currentPagination.current || 1;
      const size = currentPagination.pageSize || initialPageSize;
      const response = await fetcher({ page, size, ...filters });
      setData(response.items);
      setPagination(prev => ({ ...prev, total: response.total, current: page, pageSize: size }));
    } catch (err: any) {
      notify.error(err, '加载列表失败');
    } finally {
      setLoading(false);
    }
  }, [fetcher, initialPageSize]);

  useEffect(() => {
    load(pagination);
  }, [load]);

  return { data, loading, pagination, load };
}
