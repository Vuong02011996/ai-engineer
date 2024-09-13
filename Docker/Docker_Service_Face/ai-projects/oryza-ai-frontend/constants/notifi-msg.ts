import { ResultEnum } from "./enum";

export enum NotifiMsg {
  createCompany = "Thêm công ty thành công",
  createCompanyErr = "Đã xãy ra lỗi khi thêm công ty",
  updateCompany = "Cập nhật công ty thành công",
  updateCompanyErr = "Đã xãy ra lỗi khi cập nhật công ty",
  deleteCompany = "Xóa công ty thành công",
  deleteCompanyErr = "Đã xãy ra lỗi khi xóa công ty",
  // createCamera = getNotifi("camera", Method.create, ResultEnum.success),
}

enum Method {
  create = "CREATE",
  update = "UPDATE",
  remove = "REMOVE",
}

function getNotifi(title: string, method: Method, status: ResultEnum) {
  let methodString = getMethod(method);
  let statusString = getStatus(status);
  let result = `${methodString} ${title} ${statusString}`;
  let capitalizedStr = result.charAt(0).toUpperCase() + result.slice(1);
  return capitalizedStr;
}

function getMethod(method: Method) {
  switch (method) {
    case Method.create:
      return "thêm mới";
    case Method.remove:
      return "xóa";
    case Method.update:
      return "cập nhật";

    default:
      return "";
  }
}
function getStatus(status: ResultEnum) {
  switch (status) {
    case ResultEnum.error:
      return "thành công";
    case ResultEnum.success:
      return "không thành công";
    default:
      return "";
  }
}
