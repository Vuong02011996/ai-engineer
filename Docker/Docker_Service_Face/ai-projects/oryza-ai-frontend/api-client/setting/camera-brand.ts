import axiosClient from "@/helper/call-center";

export const cameraBrandApi = {
  getAll(params: { page: number; page_break: boolean; data_search: string }) {
    return axiosClient.get("/brand_camera/get_all", { params: params });
  },
  getById(brand_id: string) {
    return axiosClient.get(`/brand_camera/get_by_id/${brand_id}`);
  },
  getCount(params: any) {
    return axiosClient.get("/brand_camera/count", { params: params });
  },
  create(payload: any) {
    return axiosClient.post("/brand_camera/create", payload);
  },
  update(payload: any, brand_camera_id: string) {
    return axiosClient.put(
      `/brand_camera/update_by_id/${brand_camera_id}`,
      payload
    );
  },
  delete(brand_camera_id: string) {
    return axiosClient.delete(`/brand_camera/delete_by_id/${brand_camera_id}`);
  },
};
