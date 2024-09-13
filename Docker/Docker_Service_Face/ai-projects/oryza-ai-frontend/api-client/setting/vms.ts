import axiosClient from "@/helper/call-center";

export const vmsApi = {
  create(payload: any) {
    return axiosClient.post("/vms/create", payload);
  },
  update(payload: any) {
    return axiosClient.put(`/vms/update_my_company_vms`, payload);
  },
  getByCompany() {
    return axiosClient.get("/vms/get_my_company_vms");
  },
  syncCamera() {
    return axiosClient.get("/camera/sync-from-vms");
  },
};
