import axiosClient from "@/helper/call-center";

export const itemsForgottenApi = {
  getAll() {
    return axiosClient.get(`/setting_detect_items_forgotten/get_all`);
  },
  getAllInfo(params: any) {
    return axiosClient.get(`/setting_detect_items_forgotten/get_all_info`, {
      params: params,
    });
  },

  create(payload: any) {
    return axiosClient.post(`/setting_detect_items_forgotten/create`, payload);
  },

  update(payload: any, id: string) {
    return axiosClient.put(
      `/setting_detect_items_forgotten/update/${id}`,
      payload
    );
  },

  getByIdCamera(id_camera: string) {
    return axiosClient.get(
      `/setting_detect_items_forgotten/get_by_id_camera/${id_camera}`
    );
  },

  getImageByIdCamera(id_camera: string) {
    return axiosClient.get(
      `/setting_detect_items_forgotten/get_image_by_id_camera/${id_camera}`
    );
  },
  getCount(params: any) {
    return axiosClient.get(`/setting_detect_items_forgotten/get_count_info`, {
      params: params,
    });
  },
};
