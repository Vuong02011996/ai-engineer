import { StatusState } from "./interface";
import { BASE_STATUS_STYLE } from "./style";

export const statusMap = {
  ONLINE: {
    ...BASE_STATUS_STYLE.green,
    text: "Đang hoạt động",
  },
  NOT_ERROR: {
    ...BASE_STATUS_STYLE.green,
    text: "Không vi phạm",
  },
  OFFLINE: {
    ...BASE_STATUS_STYLE.red,
    text: "Không hoạt động",
  },
  ERROR: {
    ...BASE_STATUS_STYLE.red,
    text: "Vi phạm",
  },
  ADDED: {
    ...BASE_STATUS_STYLE.green,
    text: "Đã được thêm",
  },
  NOT_ADDED: {
    ...BASE_STATUS_STYLE.red,
    text: "Chưa được thêm",
  },
  ACTIVE: {
    ...BASE_STATUS_STYLE.green,
    text: "Đã kích hoạt",
  },
  INACTIVE: {
    ...BASE_STATUS_STYLE.gray,
    text: "Chưa kích hoạt",
  },
  UNKNOWN_ERROR: {
    ...BASE_STATUS_STYLE.gray,
    text: "Không xác định",
  },
  STOP: {
    ...BASE_STATUS_STYLE.red,
    text: "Đã dừng",
  },
  PROCESSING: {
    ...BASE_STATUS_STYLE.blue,
    text: "Đang chạy",
  },
};
export function getStatus(status: StatusState) {
  return statusMap[status];
}
