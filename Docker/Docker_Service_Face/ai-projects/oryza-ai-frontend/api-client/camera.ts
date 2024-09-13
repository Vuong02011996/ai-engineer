import axiosClient from "@/helper/call-center";
import { CreateCamera, GenerateRTSP } from "@/models/camera";

export const cameraApi = {
  getAll(params: { page: number; page_break: boolean; data_search: string }) {
    return axiosClient.get("/camera/get_all", { params: params });
  },
  getCameraAi() {
    return axiosClient.get("/camera/get_camera_face_ai");
  },
  getCount(params: { data_search: string }) {
    return axiosClient.get("/camera/count", { params: params });
  },
  getById(camera_id: string) {
    return axiosClient.get(`/camera/get_by_id/${camera_id}`);
  },

  getByCompanyId(company_id: string) {
    return axiosClient.get(`/api/v1/camera/get_by_company_id/${company_id}`);
  },
  create(payload: CreateCamera) {
    return axiosClient.post("/camera/create", payload);
  },
  update(payload: CreateCamera, camera_id: string) {
    return axiosClient.put(`/camera/update_by_id/${camera_id}`, payload);
  },
  delete(camera_id: string) {
    return axiosClient.delete(`/camera/delete_by_id/${camera_id}`);
  },
  cameraTypeMapping(camera_id: string) {
    return axiosClient.get(`/camera_type_ai_mapping/get_by_id/${camera_id}`);
  },
  generateRtsp(payload: GenerateRTSP) {
    return axiosClient.post("/camera/generate_rtsp", payload);
  },
  generateRtspVms(camera_id: string) {
    return axiosClient.get(`/camera/generate_rtsp_vms/${camera_id}`);
  },
  getListRtsp(camera_id: string) {
    return axiosClient.get(`/camera/get_list_rtsp/${camera_id}`);
  }
};
