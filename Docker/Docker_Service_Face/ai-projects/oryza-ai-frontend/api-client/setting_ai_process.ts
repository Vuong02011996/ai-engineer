import axiosClient from "@/helper/call-center";

const getApi = (settingName: string) => ({
  getAll(params: any) {
    return axiosClient.get(`/${settingName}/get_all/`, {
      params: params,
    });
  },
  getAllInfo(params?: any) {
    return axiosClient.get(`/${settingName}/get_all_info`, {
      params: params,
    });
  },
  create(payload: any) {
    return axiosClient.post(`/${settingName}/create`, payload);
  },
  update(payload: any, id: string) {
    return axiosClient.put(`/${settingName}/update/${id}`, payload);
  },
  getByCamera(camera_id: string, params?: any) {
    return axiosClient.get(`/${settingName}/get_by_camera/${camera_id}`, {
      params: params
    });
  },
  getCount(params?: any) {
    return axiosClient.get(`/${settingName}/get_count_info`, {
      params: params,
    });
  },
});

// export const intrusionApi = getApi("setting_intrusion");
export const tripwireApi = getApi("setting_tripwire");
export const leavingApi = getApi("setting_leaving");
export const loiteringApi = getApi("setting_loitering");
export const laneViolationApi = getApi("setting_lane_violation");
export const plateNumberApi = getApi("setting_plate_number");
export const illegalParkingApi = getApi("setting_illegal_parking");
export const crowdApi = getApi("setting_crowd");
export const objAttrApi = getApi("setting_obj_attr");

