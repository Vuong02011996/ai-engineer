import axiosClient from "@/helper/call-center";

export const personApi = {
  getByCompany(
    params: { page: number; page_break: boolean; data_search: string },
    company_id: string
  ) {
    return axiosClient.get(`/person/get_by_company/${company_id}`, {
      params: params,
    });
  },
  getById(id_person: string) {
    return axiosClient.get(`/person/get_by_id/${id_person}`);
  },
  getCount(params: any, id_company: string) {
    return axiosClient.get(`/person/get_count_by_company/${id_company}`, {
      params: params,
    });
  },

  create(formData: any) {
    return axiosClient.post(`/person/create`, formData);
  },
  update(payload: any, person_id: string) {
    return axiosClient.put(`/person/update/${person_id}`, payload);
  },
  delete(person_id: string) {
    return axiosClient.delete(`/person/delete/${person_id}`);
  },

  checkImage(formData: any) {
    return axiosClient.post(`/person_image/check_image_valid`, formData);
  },
  removeImage(person_id: string, id_image: string) {
    return axiosClient.delete(
      `/person_image/delete_image/${person_id}/${id_image}`
    );
  },
  addImage(formData: any, person_id: string) {
    return axiosClient.patch(`/person_image/create/${person_id}`, formData);
  },

  getPersionByCompanyCamera(params: any) {
    return axiosClient.get("/person/get_person_by_company_camera", {
      params: params,
    });
  },
};
