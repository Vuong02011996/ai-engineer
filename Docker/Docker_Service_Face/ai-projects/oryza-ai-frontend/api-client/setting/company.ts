import axiosClient from "@/helper/call-center";
import { CreateCompany } from "@/models/company";

export const companyApi = {
  getAll(params: { page: number; page_break: boolean; data_search: string }) {
    return axiosClient.get("/company/get_all", { params: params });
  },
  getCount(params?: any) {
    return axiosClient.get("/company/count", { params: params });
  },
  getById(company_id: string) {
    return axiosClient.get(`/company/get_by_id/${company_id}`);
  },
  create(payload: CreateCompany) {
    return axiosClient.post("/company/create", payload);
  },
  update(payload: CreateCompany, company_id: string) {
    return axiosClient.put(`/company/update_by_id/${company_id}`, payload);
  },
  delete(company_id: string) {
    return axiosClient.delete(`/company/delete_by_id/${company_id}`);
  },
};
