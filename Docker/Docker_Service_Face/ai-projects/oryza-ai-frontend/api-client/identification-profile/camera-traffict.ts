import axiosClient from "@/helper/call-center";

export const cameraTraffictApi = {
  getAll() {
    return axiosClient.get(`/setting_camera_traffic_detection/get_all`);
  },
  getAllInfo(params: any) {
    return axiosClient.get(`/setting_camera_traffic_detection/get_all_info`, {
      params: params,
    });
  },

  create(payload: any) {
    return axiosClient.post(
      `/setting_camera_traffic_detection/create`,
      payload
    );
  },

  update(payload: any, id: string) {
    return axiosClient.put(
      `/setting_camera_traffic_detection/update/${id}`,
      payload
    );
  },

  getByIdCamera(id_camera: string) {
    return axiosClient.get(
      `/setting_camera_traffic_detection/get_by_id_camera/${id_camera}`
    );
  },

  getImageByIdCamera(id_camera: string) {
    return axiosClient.get(
      `/setting_camera_traffic_detection/get_image_by_id_camera/${id_camera}`
    );
  },
  getCount(params: any) {
    return axiosClient.get(`/setting_camera_traffic_detection/get_count_info`, {
      params: params,
    });
  },
};
