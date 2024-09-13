import axiosClient from "@/helper/call-center";

export const personCameraApi = {
  create(payload: any) {
    return axiosClient.post(`/person_camera/create`, payload);
  },
  getByPersonId(person_id: string) {
    return axiosClient.get(`/person_camera/get_by_person_id/${person_id}`);
  },
  getByCameraId(camera_id: string) {
    return axiosClient.get(`/person_camera/get_by_camera_id/${camera_id}`);
  },
  remove(payload: any, id: string) {
    return axiosClient.post(`/person_camera/delete/${id}`, payload);
  },

  createMultipleCameraPerson(person_id: string) {
    return axiosClient.get(
      `/person_camera/create_multi_camera_user/${person_id}`
    );
  },
  createMultiplePersonCamera(camera_id: string) {
    return axiosClient.get(
      `/person_camera/create_multi_user_camera/${camera_id}`
    );
  },
  removeMultiplePersonCamera(camera_id: string) {
    return axiosClient.delete(
      `/person_camera/delete_multi_user_camera/${camera_id}`
    );
  },

  checkMultiplePersonCamera(camera_id: string) {
    return axiosClient.get(
      `/person_camera/check_create_multi_user_camera/${camera_id}`
    );
  },
};
