interface Column {
  id: number;
  name: string;
  width: string;
  key: string;
}

export const getColumns = (role: string): Column[] => {
  let roleWidth = "15%";
  let emailWidth = "25%";
  let companyColumns: Column[] = []; // Explicitly typed as an array of Column
  let createTimeWidth = "20%";

  if (role === "SUPERUSER") {
    roleWidth = "10%";
    emailWidth = "20%";
    companyColumns = [
      {
        id: 5,
        name: "Công ty",
        width: "20%",
        key: "COMPANY",
      },
    ];
    createTimeWidth = "15%";
  }

  const columns: Column[] = [
    {
      id: 1,
      name: "#",
      width: "60px",
      key: "INDEX",
    },
    {
      id: 2,
      name: "Tên đăng nhập",
      width: "15%",
      key: "USERNAME",
    },
    {
      id: 3,
      name: "Loại quyền",
      width: roleWidth,
      key: "ROLE",
    },
    {
      id: 4,
      name: "Email",
      width: emailWidth,
      key: "EMAIL",
    },
    ...companyColumns,
    {
      id: 6,
      name: "Thời gian tạo",
      width: createTimeWidth,
      key: "TIME",
    },
    {
      id: 7,
      name: "Trạng thái",
      width: "10%",
      key: "STATUS",
    },
    {
      id: 8,
      name: "",
      width: "0%",
      key: "ACTION",
    },
  ];

  return columns;
}