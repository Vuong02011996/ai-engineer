import { TypeServiceKey } from "@/constants/type-service";
import { IBrandCamera } from "@/interfaces/brand-camera";
import { ICameraAI } from "@/interfaces/identification-profile/camera-ai";
import { CameraCrowd } from "@/interfaces/identification-profile/crowd";
import { CameraLoiteringDetection } from "@/interfaces/identification-profile/loitering-detection";
import { CameraTripwire } from "@/interfaces/identification-profile/tripwire";
import { CameraIllegalParking } from "@/interfaces/identification-profile/illegal-parking";
import { IPerson } from "@/interfaces/identification-profile/person";
import { CameraPlateNumber } from "@/interfaces/identification-profile/plate-number";
import { EventData } from "@/interfaces/manage/event";
import { PorcessRes } from "@/interfaces/process";
import { ProcessEvent } from "@/interfaces/process-page";
import { TabInterface } from "@/interfaces/tab";
import { TypeServiceRes } from "@/interfaces/type-service";
import { UserRes } from "@/interfaces/user";
import { WebhookRes } from "@/interfaces/webhook";
import { InfoServer } from "@/models/redux.model";
import { convertToDate, uuidv4 } from "@/utils/global-func";
import { getIconActiveByKey, getIconByKey } from "./type-service";
import { CameraTraffictDetection } from "@/interfaces/identification-profile/camera-traffict";
import { CameraLaneViolation } from "@/interfaces/identification-profile/lane-violation";

export function formatTypeService(data: any) {
  let array: TypeServiceRes[] = data.map((serviceType: any) => {
    let item: TypeServiceRes = {
      name: serviceType?.name ?? "",
      key: serviceType?.key ?? "",
      id: serviceType?.id ?? "",
      created: serviceType?.created ?? new Date(),
      modified: serviceType?.modified ?? new Date(),
    };
    return item;
  });
  return array;
}
export function formatWebhook(data: any) {
  let array: WebhookRes[] = data.map((webhook: WebhookRes) => {
    let item: WebhookRes = {
      id: webhook?.id ?? "",
      created: webhook?.created ?? new Date(),
      modified: webhook?.modified ?? new Date(),
      company: webhook?.company ?? "",
      type_service: webhook?.type_service ?? "",
      status: webhook?.status ?? false,
      name: webhook?.name ?? "",
      endpoint: webhook?.endpoint ?? "",
      token: webhook?.token ?? "",
      auth_type: webhook?.auth_type ?? "",
    };
    return item;
  });
  return array;
}
export function formatUser(data: any) {
  let array: UserRes[] = data.map((user: any) => {
    let item: UserRes = {
      id: user?.id ?? "",
      username: user?.username ?? "",
      email: user?.email ?? "",
      company: user?.company ?? "",
      email_validated: user?.email_validated ?? false,
      is_admin: user?.is_admin ?? false,
      is_active: user?.is_active ?? false,
      is_superuser: user?.is_superuser ?? false,
      created: user?.created ?? new Date(),
      modified: user?.modified ?? new Date(),
      hash_password: user?.hash_password ?? "",
      avatar: user?.avatar ?? "",
    };
    return item;
  });
  return array;
}
export function formatProcess(data: any) {
  let array: PorcessRes[] = data.map((process: any) => {
    let item: PorcessRes = {
      id: process?.id ?? "",
      camera: process?.camera ?? "",
      service: process?.service ?? "",
      status: process?.status ?? "",
      created: process?.created ?? new Date(),
      modified: process?.modified ?? new Date(),
      isEnable: process?.isEnable ?? false,
      is_debug: process?.is_debug ?? false,
    };
    return item;
  });
  return array;
}

export function typeServiceToTab(data: TypeServiceRes[]) {
  let array: TabInterface[] = data.map((type: TypeServiceRes) => {
    let item: TabInterface = {
      id: type.id,
      name: type.name,
      icon: getIconByKey(type.key as TypeServiceKey),
      iconActive: getIconActiveByKey(type.key as TypeServiceKey),
      path: type.key.toLocaleLowerCase(),
    };
    return item;
  });
  return array;
}
export function formatEventData(data: any, withData?: boolean) {
  let array: EventData[] = data.map((o: any) => {
    let value = withData ? o?.data : o;
    let item: EventData = {
      camera_name: value?.camera_name ?? "",
      event_id: o?.id ?? "",
      uuid: uuidv4(),
      user_id: value?.user_id ?? "",
      timestamp: convertToDate(value.timestamp),
      image_url: value?.image_url ?? "",
      camera_ip: value?.camera_ip ?? "",
      name: value?.name ?? "",

      brand_name: value?.brand_name ?? "",
      license_plate: value?.license_plate ?? "",
      license_plate_bounding_boxes: value?.license_plate_bounding_boxes ?? [],
      vehicle_bounding_box: value?.vehicle_bounding_box ?? [],
      vehicle_color: value?.vehicle_color ?? "",
      vehicle_type: value?.vehicle_type ?? "",

      crowd_alert_threshold: value?.crowd_alert_threshold ?? "",
      crowd_members_count: value?.crowd_members_count ?? "",
      people_bounding_boxes: value?.people_bounding_boxes ?? "",
      total_people_detected: value?.total_people_detected ?? "",

      full_img: value?.full_img ?? "",
      crop_plate: value?.crop_plate ?? "",

      duration_time:
        value?.duration_time === -1 ? undefined : value?.duration_time ?? 0,
      end_time: convertToDate(value?.end_time === -1 ? "" : value?.end_time),
      image_end: value?.image_end ?? "",
      image_start: value?.image_start ?? "",
      start_time: convertToDate(
        value?.start_time === -1 ? "" : value?.start_time
      ),
      track_id: value?.track_id ?? 0,
      error_type: value?.error_type,

      signal: value?.signal || "",
      license_plate_url: value?.license_plate_url || "",
      status: value?.status || "",
      violation: value?.violation || "",
      violation_code: value?.violation_code || "",
      traffic_code: value?.traffic_code || "",
      safe_belt: value?.safe_belt || "",
      calling: value?.calling || "",
      smoking: value?.smoking || "",
      lane: value?.lane || "",
      plate_color: value?.plate_color || "",
      speed: value?.speed || "",

      // obj_attr 
      object_type: value?.object_type || "",
      attributes: value?.attributes || [],
    };
    return item;
  });
  return array;
}
export function formatCameraBrand(data: any) {
  let array: IBrandCamera[] = data.map((value: any) => {
    let item: IBrandCamera = {
      id: value?.id ?? "",
      name: value?.name ?? "",
      created: value?.created ?? new Date(),
      modified: value?.modified ?? new Date(),
      key: value?.key ?? "",
    };
    return item;
  });
  return array;
}

export function formatPerson(data: any, cameraPersonList?: any[]) {
  let array: IPerson[] = data.map((value: any) => {
    let idCameraPerson;

    if (cameraPersonList) {
      for (let i = 0; i < cameraPersonList.length; i++) {
        const element = cameraPersonList[i];
        if (element.person_id === value.id) {
          idCameraPerson = element.id;
          break;
        }
      }
    }

    let item: IPerson = {
      id: value?.id ?? "",
      name: value?.name ?? "",
      company_id: value?.company_id ?? "",
      other_info: value?.other_info,
      created: value?.created ?? new Date(),
      modified: value?.modified ?? new Date(),
      is_delete: value?.is_delete ?? false,
      images: value.images ?? [],
      idCameraPerson: idCameraPerson,
    };
    return item;
  });
  return array;
}
export function formatCameraAi(data: any, cameraPersonList: any) {
  let array: ICameraAI[] = data.map((value: ICameraAI) => {
    let idCameraPerson;

    for (let i = 0; i < cameraPersonList.length; i++) {
      const element = cameraPersonList[i];
      if (element.camera_id === value.id) {
        idCameraPerson = element.id;
        break;
      }
    }

    let item: ICameraAI = {
      brand_camera: value?.brand_camera,
      ip_address: value?.ip_address ?? "",
      is_ai: value?.is_ai ?? false,
      created: value?.created ?? new Date(),
      modified: value?.modified ?? new Date(),
      name: value?.name ?? "",
      other_info: value?.other_info,
      password: value?.password ?? "",
      port: value?.port ?? 0,
      rtsp: value?.rtsp ?? "",
      username: value?.username ?? "",
      id: value?.id ?? "",
      idCameraPerson: idCameraPerson,
      type_camera: value?.type_camera ?? "",
    };
    return item;
  });
  return array;
}

export function formatCrowdData(cameraList: any[]) {
  let array: any[] = cameraList.map((value: any) => {
    let item: CameraCrowd = {
      name: value?.name ?? "",
      ip_address: value?.ip_address ?? "",
      port: value?.port ?? 0,
      username: value?.username ?? "",
      password: value?.password ?? "",
      rtsp: value?.rtsp ?? "",
      id: value?.id ?? "",
      crowdData: value?.setting,
    };

    return item;
  });
  return array;
}

export function formatLaneViolationData(cameraList: any[]) {
  let array: any[] = cameraList.map((value: any) => {
    let item: CameraLaneViolation = {
      id: value?.id ?? "",
      name: value?.name ?? "",
      ip_address: value?.ip_address ?? "",
      port: value?.port ?? 0,
      username: value?.username ?? "",
      password: value?.password ?? "",
      rtsp: value?.rtsp ?? "",
      setting: value?.setting,
    };

    return item;
  });
  return array;
}
export function formatLoiteringData(cameraList: any[]) {
  let array: any[] = cameraList.map((value: any) => {
    let item: CameraLoiteringDetection = {
      name: value?.name ?? "",
      ip_address: value?.ip_address ?? "",
      port: value?.port ?? 0,
      username: value?.username ?? "",
      password: value?.password ?? "",
      rtsp: value?.rtsp ?? "",
      id: value?.id ?? "",
      setting: value?.setting,
    };

    return item;
  });
  return array;
}
export function formatTripwireData(cameraList: any[]) {
  let array: any[] = cameraList.map((value: any) => {
    let item: CameraTripwire = {
      name: value?.name ?? "",
      ip_address: value?.ip_address ?? "",
      port: value?.port ?? 0,
      username: value?.username ?? "",
      password: value?.password ?? "",
      rtsp: value?.rtsp ?? "",
      id: value?.id ?? "",
      setting: value?.setting,
    };

    return item;
  });
  return array;
}

export function formatIllegalParkingData(cameraList: any[]) {
  let array: any[] = cameraList.map((value: any) => {
    let item: CameraIllegalParking = {
      name: value?.name ?? "",
      ip_address: value?.ip_address ?? "",
      port: value?.port ?? 0,
      username: value?.username ?? "",
      password: value?.password ?? "",
      rtsp: value?.rtsp ?? "",
      id: value?.id ?? "",
      setting: value?.setting,
    };

    return item;
  });
  return array;
}

export function formatCameraTraffict(cameraList: any[]) {
  let array: any[] = cameraList.map((value: any) => {
    let item: CameraTraffictDetection = {
      name: value?.name ?? "",
      ip_address: value?.ip_address ?? "",
      port: value?.port ?? 0,
      username: value?.username ?? "",
      password: value?.password ?? "",
      rtsp: value?.rtsp ?? "",
      id: value?.id ?? "",
      setting: value?.setting,
    };

    return item;
  });
  return array;
}
export function formatPlateNumberData(cameraList: any[]) {
  let array: any[] = cameraList.map((value: any) => {
    let item: CameraPlateNumber = {
      name: value?.name ?? "",
      ip_address: value?.ip_address ?? "",
      port: value?.port ?? 0,
      username: value?.username ?? "",
      password: value?.password ?? "",
      rtsp: value?.rtsp ?? "",
      id: value?.id ?? "",
      setting: value?.setting,
    };

    return item;
  });
  return array;
}
export function formatInfoServer(data: any) {
  let item: InfoServer = {
    id: uuidv4(),
    ip: data?.ip ?? "",
    cpu_percent: Number(data?.cpu_percent) ?? 0,
    ram_total: Number(data?.ram_total) ?? 0,
    ram_used: Number(data?.ram_used) ?? 0,
    ram_percent: Number(data?.ram_percent) ?? 0,
    disk_total: Number(data?.disk_total) ?? 0,
    disk_used: Number(data?.disk_used) ?? 0,
    disk_percent: Number(data?.disk_percent) ?? 0,
    list_gpu: data?.list_gpu,
    current_freq_mhz: Number(data?.current_freq_mhz) ?? 0,
  };
  return item;
}
export function formatProcessEvent(data: any) {
  return data.map((item: any) => {
    let value: ProcessEvent = {
      camera: item?.camera,
      service: item?.service,
      status: item?.status,
      isEnable: item?.isEnable,
      pid: item?.pid,
      id_type_service: item?.id_type_service,
      id: item?.id,
      created: item?.created,
      modified: item?.modified,
      is_debug: item?.is_debug,
    };
    return value;
  });
}
