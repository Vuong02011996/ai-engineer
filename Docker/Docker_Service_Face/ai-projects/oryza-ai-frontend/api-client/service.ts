import axiosClient from "@/helper/call-center";
import { CreateServer } from "@/models/server";

export const serviceApi = {
  getAll(params: { page?: number; page_break: boolean }) {
    return axiosClient.get("/service/get_all", { params: params });
  },

  getByServer(params: {
    server_id: string;
    page: number;
    page_break: boolean;
  }) {
    return axiosClient.get("/service/get_by_server", { params: params });
  },

  getCountByServer(params: { server_id: string }) {
    return axiosClient.get("/service/get_count_by_server", { params: params });
  },

  getById(server_id: string) {
    return axiosClient.get(`/service/get_by_id/${server_id}`);
  },
  getInfoById(service_id: string) {
    return axiosClient.get(`/service/get_info_by_id/${service_id}`);
  },
  create(payload: any) {
    return axiosClient.post("/service/create", payload);
  },
  update(payload: any, server_id: string) {
    return axiosClient.put(`/service/update_by_id/${server_id}`, payload);
  },
  delete(server_id: string) {
    return axiosClient.delete(`/service/delete_by_id/${server_id}`);
  },
};
