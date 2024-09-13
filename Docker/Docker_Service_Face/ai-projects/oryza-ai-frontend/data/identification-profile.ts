import { TypeServiceKey } from "@/constants/type-service";
import { getIconActiveByKey, getIconByKey } from "@/libs/type-service";

export default [
  {
    id: "1",
    name: "Đối tượng",
    icon: "/icons/user.svg",
    iconActive: "/icons/user-active.svg",
    path: "/identification-profile/user",
  },
  {
    id: "2",
    name: "Camera nhận diện",
    icon: "/icons/camera.svg",
    iconActive: "/icons/camera-active.svg",
    path: "/identification-profile/camera",
  },
  {
    id: "3",
    name: "Biển số",
    icon: getIconByKey(TypeServiceKey.plate_number),
    iconActive: getIconActiveByKey(TypeServiceKey.plate_number),
    path: "/identification-profile/plate-number",
  },
  {
    id: "4",
    name: "Bỏ rơi",
    icon: getIconByKey(TypeServiceKey.DETECT_ITEMS_FORGOTTEN_EXCHANGES),
    iconActive: getIconActiveByKey(
      TypeServiceKey.DETECT_ITEMS_FORGOTTEN_EXCHANGES
    ),
    path: "/identification-profile/detect-items-forgotten",
  },
  {
    id: "5",
    name: "Đám đông",
    icon: getIconByKey(TypeServiceKey.CROWD_DETECTION_EXCHANGES),
    iconActive: getIconActiveByKey(TypeServiceKey.CROWD_DETECTION_EXCHANGES),
    path: "/identification-profile/crowd",
  },
  {
    id: "7",
    name: "Đồng phục",
    icon: getIconByKey(TypeServiceKey.IDENTIFY_UNIFORMS_EXCHANGES),
    iconActive: getIconActiveByKey(TypeServiceKey.IDENTIFY_UNIFORMS_EXCHANGES),
    path: "/identification-profile/identify-uniform",
  },
  {
    id: "9",
    name: "Hàng rào ảo",
    icon: getIconByKey(TypeServiceKey.tripwire),
    iconActive: getIconActiveByKey(
      TypeServiceKey.tripwire
    ),
    path: "/identification-profile/tripwire",
  },
  {
    id: "10",
    name: "Lảng vảng",
    icon: getIconByKey(TypeServiceKey.loitering),
    iconActive: getIconActiveByKey(
      TypeServiceKey.loitering
    ),
    path: "/identification-profile/loitering-detection",
  },
  // {
  //   id: "15",
  //   name: "Xâm nhập",
  //   icon: getIconByKey(TypeServiceKey.intrusion),
  //   iconActive: getIconActiveByKey(
  //     TypeServiceKey.intrusion
  //   ),
  //   path: "/identification-profile/intrusion",
  // },
  {
    id: "11",
    name: "Phá hoại",
    icon: getIconByKey(TypeServiceKey.CAMERA_TAMPERING_EXCHANGES),
    iconActive: getIconActiveByKey(TypeServiceKey.CAMERA_TAMPERING_EXCHANGES),
    path: "/identification-profile/tampering",
  },

  {
    id: "6",
    name: "Đèn giao thông",
    icon: getIconByKey(TypeServiceKey.CAMERA_TRAFFIC_SIGNAL_EXCHANGES),
    iconActive: getIconActiveByKey(
      TypeServiceKey.CAMERA_TRAFFIC_SIGNAL_EXCHANGES
    ),
    path: "/identification-profile/detect-camera-traffict",
  },
  {
    id: "8",
    name: "Đậu đỗ trái phép",
    icon: getIconByKey(TypeServiceKey.illegal_parking),
    iconActive: getIconActiveByKey(
      TypeServiceKey.illegal_parking
    ),
    path: "/identification-profile/illegal-parking",
  },
  {
    id: "12",
    name: "Lấn làn",
    icon: getIconByKey(TypeServiceKey.lane_violation),
    iconActive: getIconActiveByKey(
      TypeServiceKey.lane_violation
    ),
    path: "/identification-profile/lane-violation",
  },
  {
    id: "13",
    name: "Lấn vạch",
    icon: getIconByKey(TypeServiceKey.line_violation),
    iconActive: getIconActiveByKey(
      TypeServiceKey.line_violation
    ),
    path: "/identification-profile/line-violation",
  },
  {
    id: "14",
    name: "Đi ngược chiều",
    icon: getIconByKey(TypeServiceKey.wrong_way),
    iconActive: getIconActiveByKey(
      TypeServiceKey.wrong_way
    ),
    path: "/identification-profile/wrong-way",
  },
];

export const headData = [
  {
    id: 1,
    name: "#",
    width: "60px",
    key: "INDEX",
  },
  {
    id: 2,
    name: "Tên đối tượng",
    width: "15%",
    key: "NAME",
  },

  {
    id: 3,
    name: "Giới tính",
    width: "10%",
    key: "NAME",
  },
  {
    id: 4,
    name: "Địa chỉ",
    width: "15%",
    key: "NAME",
  },
  {
    id: 5,
    name: "Hình ảnh",
    width: "30%",
    key: "NAME",
  },
  // {
  //   id: 8,
  //   name: "Số camera đang dùng",
  //   width: "15%",
  //   key: "NAME",
  // },
  {
    id: 6,
    name: "Thời gian tạo",
    width: "10%",
    key: "NAME",
  },
  {
    id: 7,
    name: "ID đối tượng",
    width: "15%",
    key: "NAME",
  },
  {
    id: 8,
    name: "",
    width: "5%",
    key: "ACTION",
  },
];
export const headSlugData = [
  // {
  //   id: 0,
  //   name: "#",
  //   width: "60px",
  //   key: "CHECKBOX",
  // },
  {
    id: 1,
    name: "#",
    width: "60px",
    key: "INDEX",
  },
  {
    id: 2,
    name: "Tên camera",
    width: "30%",
    key: "NAME",
  },

  {
    id: 3,
    name: "Loại",
    width: "20%",
    key: "NAME",
  },
  {
    id: 4,
    name: "Địa chỉ IP",
    width: "30%",
    key: "NAME",
  },
  {
    id: 5,
    name: "Bật/Tắt giám sát",
    width: "20%",
    key: "NAME",
  },
  // {
  //   id: 8,
  //   name: "Trạng thái",
  //   width: "20%",
  //   key: "NAME",
  // },
];
