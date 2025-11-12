"use client";

import client from "./apiClient";

export const companies = client.resource("companies");

export const fetchCompanies = (skip = 0, limit = 100) => companies.list<any[]>({ skip, limit });
export const fetchCompany = (id: number) => companies.get<any>(id);
export const createCompany = (payload: any) => companies.create<any>(payload);
export const updateCompany = (id: number, payload: any) => companies.update<any>(id, payload);
export const deleteCompany = (id: number) => companies.delete<any>(id);

export default companies;
