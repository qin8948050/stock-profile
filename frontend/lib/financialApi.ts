import client from "@/lib/apiClient";
import { ApiResponse } from "@/types/api";

type StatementUploader = {
    company:number;
    type: string;
    file: File;
}

export const uploader = client.resource("financial-statements/upload");

export const uploadFinancialStatement = async (
    payload: Partial<StatementUploader>
) => {
    const { company, type, file } = payload;
    if (!file || !type || !company) {
        throw new Error("公司ID、报表类型和文件均为必填项。");
    }

    // 创建一个 FormData 对象以匹配 multipart/form-data 请求
    const formData = new FormData();
    formData.append("file", file);
    formData.append("type", type);
    formData.append("company_id", String(company));

    try {
        // 将 FormData 对象传递给 create 方法
        // axios (或类似的 http 客户端) 会自动设置正确的 Content-Type
        const response= await uploader.create(formData);
        return response;
    } catch (error: any) {
        console.error("Failed to upload financial statement:", error);
        throw error;
    }
};
