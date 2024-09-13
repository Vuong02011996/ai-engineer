import axiosClient from "@/helper/call-center";

export const processApi = {
  getAll(params: { page: number; page_break: boolean }) {
    return axiosClient.get("/process/get_all", { params: params });
  },
  getByCameraId(camera_id: string) {
    return axiosClient.get("/process/get_by_camera_id/" + camera_id);
  },
  create(payload: any) {
    return axiosClient.post("/process/create", payload);
  },
  update(payload: any, process_id: string) {
    return axiosClient.put(`/process/update_by_id/${process_id}`, payload);
  },
  delete(process_id: string) {
    return axiosClient.delete(`/process/delete_by_id/${process_id}`);
  },
  run(payload: { process_id: string; is_debug: boolean }) {
    return axiosClient.post("/process/run", payload);
  },
  kill(payload: { process_id: string }) {
    return axiosClient.post(`/process/kill/${payload.process_id}`);
  },
  // event
  getProcessEvent(id_type_service: string, params: any) {
    return axiosClient.get(
      `/process/get_by_id_type_service/${id_type_service}`,
      { params: params }
    );
  },
  getProcessEventCount(id_type_service: string, params: any) {
    return axiosClient.get(
      `/process/get_count_by_id_type_service/${id_type_service}`,
      { params: params }
    );
  },
  getPreviewImage(process_id: string) {
    return axiosClient.get(`/process/preview_image_process/${process_id}`);
  }
};
