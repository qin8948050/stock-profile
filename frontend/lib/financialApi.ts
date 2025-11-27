import defaultClient from "@/lib/apiClient";

type StatementUploader = {
    company_id:number;
    type: string;
    file: File;
}


export const uploadFinancialStatement = async (
    payload: StatementUploader
) => {
    const { company_id, type, file } = payload;
    if (!file || !type || !company_id) {
        throw new Error("公司ID、报表类型和文件均为必填项。");
    }

    // 创建一个 FormData 对象以匹配 multipart/form-data 请求
    const formData = new FormData();
    formData.append("file", file);
    formData.append("type", type);
    formData.append("company_id", String(company_id));
    console.log(formData);
    try {
        return defaultClient.request<null>("financial-statements/upload",{
            method: "POST",
            body: formData});
    } catch (error: any) {
        console.error("Failed to upload financial statement:", error);
        throw error;
    }
};
