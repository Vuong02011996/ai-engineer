import { TypeServiceKey as key } from "@/constants/type-service";

const defaultUrl = "/icons/services.svg";
const defaultUrlActive = "/icons/services-active.svg";

const iconMap: Record<key, string> = {
  [key.CHECK_STATUS_SERVER_EXCHANGES]: defaultUrl, // kiểm tra trạng thái máy chủ
  [key.CROWD_DETECTION_EXCHANGES]: "/icons/user-group.svg", // phát hiện đám đông
  [key.DETECT_ITEMS_FORGOTTEN_EXCHANGES]: "/icons/forgot-item.svg", // đồ bỏ rơi
  [key.FACE_RECOGNITION_EXCHANGES]: "/icons/face.svg", // nhận dạng khuôn mặt
  [key.IDENTIFY_UNIFORMS_EXCHANGES]: "/icons/icon-ai.svg", // nhận diện đồng phục
  [key.plate_number]: "/icons/place-no.svg", // biển số
  [key.WEAPON_IDENTIFICATION_EXCHANGES]: "/icons/knight.svg", // vũ khí
  [key.loitering]: "/icons/loitering.svg", // lang vang
  [key.intrusion]: "/icons/loitering.svg", // xâm nhập
  [key.CAMERA_TAMPERING_EXCHANGES]: defaultUrl, // phá hoại
  [key.CAMERA_TRAFFIC_SIGNAL_EXCHANGES]: defaultUrl, // tín hiệu đèn giao thông
  [key.illegal_parking]: "/icons/camera.svg", // đỗ xe trái phép
  [key.tripwire]: "/icons/tripwire.svg", // tripwire
  [key.lane_violation]: "/icons/camera.svg", // vi phạm làn đường
  [key.line_violation]: "/icons/camera.svg", // vi phạm vach đường
  [key.wrong_way]: "/icons/camera.svg", // đi ngược chiều
  [key.leaving]: "/icons/tripwire.svg", // rời khỏi
  [key.obj_attr]: "/icons/camera.svg"
};

const iconActiveMap: Record<key, string> = {
  [key.CHECK_STATUS_SERVER_EXCHANGES]: defaultUrlActive, // kiểm tra trạng thái máy chủ
  [key.CROWD_DETECTION_EXCHANGES]: "/icons/user-group-active.svg", // phát hiện đám đông
  [key.DETECT_ITEMS_FORGOTTEN_EXCHANGES]: "/icons/forgot-item-active.svg", // đồ bỏ rơi
  [key.FACE_RECOGNITION_EXCHANGES]: "/icons/face-active.svg", // nhận dạng khuôn mặt
  [key.IDENTIFY_UNIFORMS_EXCHANGES]: "/icons/icon-ai-active.svg", // nhận diện đồng phục
  [key.plate_number]: "/icons/place-no-active.svg", // biển số
  [key.WEAPON_IDENTIFICATION_EXCHANGES]: "/icons/knight-active.svg", // vũ khí
  [key.loitering]: "/icons/loitering-active.svg", // lang vang
  [key.intrusion]: "/icons/loitering-active.svg", // xâm nhập
  [key.CAMERA_TAMPERING_EXCHANGES]: defaultUrlActive, // phá hoại
  [key.CAMERA_TRAFFIC_SIGNAL_EXCHANGES]: defaultUrlActive, // tín hiệu đèn giao thông
  [key.illegal_parking]: "/icons/camera-active.svg", // đỗ xe trái phép
  [key.tripwire]: "/icons/tripwire-active.svg", // tripwire
  [key.lane_violation]: "/icons/camera-active.svg", // vi phạm làn đường
  [key.line_violation]: "/icons/camera-active.svg", // vi phạm vach đường
  [key.wrong_way]: "/icons/camera-active.svg", // đi ngược chiều
  [key.leaving]: "/icons/tripwire-active.svg", // rời khỏi
  [key.obj_attr]: "/icons/camera-active.svg",
};

export const getIconByKey = (key: key): string => {
  return iconMap[key] || defaultUrl;
};

export const getIconActiveByKey = (key: key): string => {
  return iconActiveMap[key] || defaultUrlActive;
};
