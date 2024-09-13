import axiosClient from "@/helper/call-center";

export const tamperingApi = {
  getAll() {
    return axiosClient.get(`/setting_tampering/get_all`);
  },
  getAllInfo(params: any) {
    return axiosClient.get(`/setting_tampering/get_all_info`, {
      params: params,
    });
  },

  create(payload: any) {
    return axiosClient.post(`/setting_tampering/create`, payload);
  },

  update(payload: any, id: string) {
    return axiosClient.put(`/setting_tampering/update/${id}`, payload);
  },

  getByIdCamera(id_camera: string) {
    return axiosClient.get(`/setting_tampering/get_by_id_camera/${id_camera}`);
  },

  getImageByIdCamera(id_camera: string) {
    return axiosClient.get(
      `/setting_tampering/get_image_by_id_camera/${id_camera}`
    );
  },
  getCount(params: any) {
    return axiosClient.get(`/setting_tampering/get_count_info`, {
      params: params,
    });
  },
};
