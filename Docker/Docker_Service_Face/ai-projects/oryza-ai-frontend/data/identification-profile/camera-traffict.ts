const list = [
  {
    name: "#",
    width: "60px",
    key: "INDEX",
  },
  {
    name: "Tên camera",
    width: "40%",
    key: "CAMERA_NAME",
  },
  {
    name: "Địa chỉ IP",
    width: "40%",
    key: "IP_ADDRESS",
  },
  {
    name: "",
    width: "20%",
    key: "ACTION",
  },
];

export default list.map((item, index) => {
  return {
    ...item,
    id: index,
  };
});
