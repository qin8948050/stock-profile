"use client";

import client, { ApiResponse } from "./apiClient";
import type { Company } from "../types/company";

export const companies = client.resource("companies");

export const fetchCompanies = (skip = 0, limit = 100): Promise<Company[]> =>
	companies.list<Company[]>({ skip, limit });
export const fetchCompany = (id: number): Promise<Company> => companies.get<Company>(id);

// create/update/delete return the full ApiResponse<T> so callers can access backend `msg`.
export const createCompany = (payload: Partial<Company>): Promise<Company> =>
	companies.create<Company>(payload);

export const updateCompany = (id: number | string, payload: Partial<Company>): Promise<Company> =>
	companies.update<Company>(id, payload);

export const deleteCompany = (id: number | string): Promise<null> => companies.delete<null>(id);

// backward-compatible aliases
// removed aliases: use createCompany/updateCompany/deleteCompany directly

export default companies;
