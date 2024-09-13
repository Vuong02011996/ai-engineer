const list = [
  {
    name: "#",
    width: "60px",
    key: "INDEX",
  },
  {
    name: "Camera",
    width: "20%",
    key: "CAMERA_NAME",
  },
  {
    name: "Địa chỉ IP",
    width: "20%",
    key: "CAMERA_IP",
  },
  {
    name: "Server",
    width: "15%",
    key: "SERVER",
  },
  {
    name: "Service",
    width: "15%",
    key: "SERVICE",
  },
  {
    name: "Trạng thái",
    width: "15%",
    key: "STATUS",
  },
  {
    name: "Bật/Tắt AI",
    width: "8%",
    key: "SWITCH",
  },
  {
    name: "",
    width: "2%",
    key: "COPY",
  },
  {
    name: "",
    width: "5%",
    key: "ACTION",
  },
];
export default list.map((item, index) => {
  return {
    ...item,
    id: index,
  };
});
