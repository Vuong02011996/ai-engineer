import axiosClient from "@/helper/call-center";

export const eventApi = {
  getRecord(event_id: string) {
    return axiosClient.get(`/event/record/${event_id}`);
  },

  getAll(params: {
    type_service_id: string;
    page: number;
    page_break: boolean;
    data_search: string;
    end_time: string;
    start_time: string;
    filter: string;
  }) {
    return axiosClient.get(
      `/event/get_by_type_service/${params.type_service_id}`,
      {
        params: params,
      }
    );
  },

  getCount(params: {
    type_service_id: string;
    data_search: string;
    end_time: string;
    start_time: string;
  }) {
    return axiosClient.get(
      `/event/get_count_by_type_service/${params.type_service_id}`,
      {
        params: params,
      }
    );
  },

  updateFaceRecognition(payload: any) {
    return axiosClient.put("/event/face_recognition", payload);
  },
};

export const watchVideo = async (event_id: string) => {
  try {
    // Example API call
    const response = await eventApi.getRecord(event_id);
    const data = response.data;
    const videoUrl = data.data;
    console.log("url", data);

    window.open(videoUrl, "_blank");
  } catch (error) {
    console.error("Error fetching video URL:", error);
  }
};
