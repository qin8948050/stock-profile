"use client";

import client from "./apiClient";

export const companies = client.resource("companies");

export const fetchCompanies = (skip = 0, limit = 100) => companies.list<any[]>({ skip, limit });
export const fetchCompany = (id: number) => companies.get<any>(id);
export const createCompany = (payload: any) => companies.create<any>(payload);
export const updateCompany = (id: number, payload: any) => companies.update<any>(id, payload);
export const deleteCompany = (id: number) => companies.delete<any>(id);

// helpers returning full ApiResponse so caller can use backend-provided `msg`
export const createCompanyWithMsg = (payload: any) => client.requestRaw<any>(`companies/`, {
	method: "POST",
	headers: { "Content-Type": "application/json" },
	body: JSON.stringify(payload),
});

export const updateCompanyWithMsg = (id: number | string, payload: any) => client.requestRaw<any>(`companies/${id}`, {
	method: "PUT",
	headers: { "Content-Type": "application/json" },
	body: JSON.stringify(payload),
});

export const deleteCompanyWithMsg = (id: number | string) => client.requestRaw<any>(`companies/${id}`, { method: "DELETE" });

export default companies;
