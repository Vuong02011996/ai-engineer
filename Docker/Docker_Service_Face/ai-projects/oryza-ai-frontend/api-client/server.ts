import axiosClient from "@/helper/call-center";
import { CreateServer } from "@/models/server";

export const serverApi = {
  getAll(params: { page: number; page_break: boolean }) {
    return axiosClient.get("/server/get_all", { params: params });
  },
  getTotal() {
    return axiosClient.get("/server/count");
  },
  getById(server_id: string) {
    return axiosClient.get(`/server/get_by_id/${server_id}`);
  },
  create(payload: CreateServer) {
    return axiosClient.post("/server/create", payload);
  },
  update(payload: CreateServer, server_id: string) {
    return axiosClient.put(`/server/update_by_id/${server_id}`, payload);
  },
  delete(server_id: string) {
    return axiosClient.delete(`/server/delete_by_id/${server_id}`);
  },
};
