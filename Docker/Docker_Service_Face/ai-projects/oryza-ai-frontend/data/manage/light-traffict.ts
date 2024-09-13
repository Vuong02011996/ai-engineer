import { addIdToArray } from "@/utils/global-func";

const list = [
  {
    name: "#",
    width: "60px",
    key: "INDEX",
  },
  {
    name: "Camera",
    width: "25%",
    key: "CAMERA_IP",
  },
  {
    name: "Tín hiệu đèn",
    width: "30%",
    key: "CAMERA_IP",
  },
  {
    name: "Thời gian",
    width: "25%",
    key: "TIME",
  },

  {
    name: "Hình ảnh ghi nhận",
    width: "20%",
    key: "IMAGE",
  },
];

export default addIdToArray(list);
