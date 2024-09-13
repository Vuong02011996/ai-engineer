import axiosClient from "@/helper/call-center";
import { CreateCompany } from "@/models/company";

export const serviceTypeApi = {
  getAll(params: { page: number; page_break: boolean; data_search: string }) {
    return axiosClient.get("/type_service/get_all", { params: params });
  },

  getCount(params?: any) {
    return axiosClient.get("/type_service/count", { params: params });
  },

  getById(type_service_id: string) {
    return axiosClient.get(`/type_service/get_by_id/${type_service_id}`);
  },

  create(payload: any) {
    return axiosClient.post("/type_service/create", payload);
  },
  update(payload: CreateCompany, type_service_id: string) {
    return axiosClient.put(
      `/type_service/update_by_id/${type_service_id}`,
      payload
    );
  },
  delete(type_service_id: string) {
    return axiosClient.delete(`/type_service/delete_by_id/${type_service_id}`);
  },
};
