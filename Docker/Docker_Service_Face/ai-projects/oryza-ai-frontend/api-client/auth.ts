import axiosClient from "@/helper/call-center";

export const authApi = {
  login(payload: { username: string; password: string }) {
    return axiosClient.post("/login/access-token", payload);
  },

  logout(token: string) {
    return axiosClient.delete(`/login/logout/${token}`);
  },
  getProfile() {
    return axiosClient.get("/user/get/me");
  },
  delelteUser(user_id: string) {
    return axiosClient.delete(`/user/delete_by_id/${user_id}`, {
      params: { user_id: user_id },
    });
  },
  updateMe(payload: any) {
    return axiosClient.put("/user/update/me", payload);
  },
};
