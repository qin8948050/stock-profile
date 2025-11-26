// Compatibility shim: re-export generic client and resource-specific helpers
export { default as defaultApiClient } from "./apiClient";
export { default } from "./apiClient";
export * from "./companyApi";
export * from './financialApi';
