import axiosClient from "@/helper/call-center";

export const uniformApi = {
  getAll() {
    return axiosClient.get(`/setting_uniforms_detection/get_all`);
  },
  getAllInfo(params: any) {
    return axiosClient.get(`/setting_uniforms_detection/get_all_info`, {
      params: params,
    });
  },

  create(payload: any) {
    return axiosClient.post(`/setting_uniforms_detection/create`, payload);
  },

  update(payload: any, id: string) {
    return axiosClient.put(`/setting_uniforms_detection/update/${id}`, payload);
  },

  getByIdCamera(id_camera: string) {
    return axiosClient.get(
      `/setting_uniforms_detection/get_by_id_camera/${id_camera}`
    );
  },

  getImageByIdCamera(id_camera: string) {
    return axiosClient.get(
      `/setting_uniforms_detection/get_image_by_id_camera/${id_camera}`
    );
  },
  getCount(params: any) {
    return axiosClient.get(`/setting_uniforms_detection/get_count_info`, {
      params: params,
    });
  },
  createSettingUniform(fromData: any) {
    return axiosClient.post(`/setting_uniform_config_company/create`, fromData);
  },
  updateSettingCompanyRgb(id: string, payload: any) {
    return axiosClient.put(
      `/setting_uniform_config_company/update/${id}`,
      payload
    );
  },
  updateSettingCompanyImage(formData: any, id: string) {
    return axiosClient.put(
      `/setting_uniform_config_company/update_image/${id}`,
      formData
    );
  },
  deleteSettingCompanyImage(id: string, imageUrl: any) {
    return axiosClient.delete(
      `/setting_uniform_config_company/delete_image/${id}`,
      {
        data: {
          image_url: imageUrl,
        },
      }
    );
  },

  getALlUniformConfig(params: any) {
    return axiosClient.get(`/setting_uniform_config_company/get_by_company`, {
      params: params,
    });
  },
};
