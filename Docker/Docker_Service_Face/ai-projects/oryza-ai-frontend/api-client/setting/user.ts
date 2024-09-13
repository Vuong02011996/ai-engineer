import axiosClient from "@/helper/call-center";

export const userApi = {
    getAll(params: {page: number; page_break: boolean, data_search: string}) {
        return axiosClient.get("/user/get_all", {params: params});
    },
    getCount(params?: any) { 
        return axiosClient.get("/user/count", { params: params });
    },
    create(payload: any) {
        return axiosClient.post("/user/create", payload);
    },
    update(payload: any, user_id: string) {
        return axiosClient.put(`/user/update_by_id/${user_id}`, payload);
    },
    delete(user_id: string) {
        return axiosClient.delete(`/user/delete_by_id/${user_id}`);
    },
};
