import axiosClient from "@/helper/call-center";

export const geoApi = {
  getList(params: { 
    keyword: string, 
    parent_id: string | null,
    type: string | null,
  }) {
    return axiosClient.get("/geo_unit", { params: params });
  },
  getById(unit_id: string) {
    return axiosClient.get(`/geo_unit/${unit_id}`);
  }
};