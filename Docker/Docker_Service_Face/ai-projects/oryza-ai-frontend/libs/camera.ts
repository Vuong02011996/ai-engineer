import { CameraRes } from "@/interfaces/camera";

export function formatCameraData(data: any) {
  let array: CameraRes[] = data.map((camera: any) => {
    let item: CameraRes = {
      name: camera?.name ?? "",
      ip_address: camera?.ip_address ?? "",
      port: camera?.port ?? 0,
      username: camera?.username ?? "",
      password: camera?.password ?? "",
      rtsp: camera?.rtsp ?? "",
      rtsp_vms: camera?.rtsp_vms ?? "",
      company: camera?.company ?? "",
      id: camera?.id ?? "",
      created: camera?.created,
      modified: camera?.modified,
      is_ai: camera?.is_ai ?? false,
      other_info: camera?.other_info ?? "",
      brand_camera: camera?.brand_camera ?? "",
      ward_id: camera?.ward_id ?? "",
    };
    return item;
  });
  return array;
}
export function formatServiceToCamera(data: any) {
  let array: CameraRes[] = data.map((camera: any) => {
    let item: CameraRes = {
      name: camera?.name ?? "",
      ip_address: camera?.server?.id ?? "",
      port: camera?.port ? Number(camera?.port) : 0,
      username: "",
      password: "",
      rtsp: "",
      rtsp_vms: "",
      company: "",
      id: camera?.id ?? "",
      created: camera?.created,
      modified: camera?.modified,
      is_ai: true,
      other_info: "",
      brand_camera: { key: "FACE_SERVICE" },
      ward_id: "",
    };
    return item;
  });
  return array;
}
