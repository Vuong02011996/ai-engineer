import axiosClient from "@/helper/call-center";

export const webhookApi = {
  getAll(params: { page: number; page_break: boolean; data_search: String }) {
    return axiosClient.get("/webhook/get_all", { params: params });
  },
  getTokenType() {
    return axiosClient.get("/webhook/get_auth_type");
  },
  getCount(params?: any) {
    return axiosClient.get("/webhook/count", { params: params });
  },
  create(payload: any) {
    return axiosClient.post("/webhook/create", payload);
  },
  update(payload: any, webhook_id: string) {
    return axiosClient.put(`/webhook/update_by_id/${webhook_id}`, payload);
  },
  delete(webhook_id: string) {
    return axiosClient.delete(`/webhook/delete_by_id/${webhook_id}`);
  },
};
