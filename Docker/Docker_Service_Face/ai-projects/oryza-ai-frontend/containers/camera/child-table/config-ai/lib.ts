import { cameraTraffictApi } from "@/api-client/identification-profile/camera-traffict";
import { itemsForgottenApi } from "@/api-client/identification-profile/items-forgotten";
import { tamperingApi } from "@/api-client/identification-profile/tampering";
import { uniformApi } from "@/api-client/identification-profile/uniform";
import { 
  tripwireApi, 
  // intrusionApi, 
  leavingApi,
  loiteringApi,
  laneViolationApi,
  plateNumberApi,
  illegalParkingApi,
  crowdApi,
  objAttrApi,
} from "@/api-client/setting_ai_process";

export const getUniformSettings = async (cameraId: string) => {
  try {
    let { data } = await uniformApi.getByIdCamera(cameraId);
    return data;
  } catch (error) {
    return null;
  }
};

export const getForgottenSettings = async (cameraId: string) => {
  try {
    let { data } = await itemsForgottenApi.getByIdCamera(cameraId);
    return data;
  } catch (error) {
    return null;
  }
};
export const getTamperingSettings = async (cameraId: string) => {
  try {
    let { data } = await tamperingApi.getByIdCamera(cameraId);
    return data;
  } catch (error) {
    return null;
  }
};
export const getCameraTraffictSettings = async (cameraId: string) => {
  try {
    let { data } = await cameraTraffictApi.getByIdCamera(cameraId);
    return data;
  } catch (error) {
    return null;
  }
};


const getSettings = async (api: any, cameraId: string, params?: any) => {
  try {
    let { data } = params ? await api.getByCamera(cameraId, params) : await api.getByCamera(cameraId);
    return data;
  } catch (error) {
    return null;
  }
};

export const getTripwireSettings = (cameraId: string) => getSettings(tripwireApi, cameraId);
export const getLeavingSettings = (cameraId: string) => getSettings(leavingApi, cameraId);
export const getLoiteringSettings = (cameraId: string, keyAI: string) => getSettings(loiteringApi, cameraId, { key_ai: keyAI });
export const getLaneViolationSettings = (cameraId: string, keyAI: string) => getSettings(laneViolationApi, cameraId, { key_ai: keyAI });
export const getCrowdSettings = (cameraId: string) => getSettings(crowdApi, cameraId);
export const getIllegalParkingSettings = (cameraId: string) => getSettings(illegalParkingApi, cameraId);
export const getPlateNumberSettings = (cameraId: string) => getSettings(plateNumberApi, cameraId);
export const getObjAttrSettings = (cameraId: string) => getSettings(objAttrApi, cameraId);