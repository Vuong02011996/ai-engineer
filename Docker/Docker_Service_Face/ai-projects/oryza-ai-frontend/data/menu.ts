import { UserRole } from "@/constants/role";

export default [
  {
    id: 2,
    name: "Server",
    icon: "server",
    path: "server",
    role: UserRole.SUPER_ADMIN,
  },
  {
    id: 1,
    name: "Quản lý dữ liệu",
    icon: "manage",
    path: "manage",
    role: UserRole.USER,
  },
  {
    id: 5,
    name: "Hồ sơ nhận diện",
    icon: "identification-profile",
    path: "identification-profile/user",
    role: UserRole.ADMIN,
  },
  {
    id: 3,
    name: "Camera",
    icon: "camera",
    path: "camera",
    role: UserRole.ADMIN,
  },
  // {
  //   id: 4,
  //   name: "Lịch sử",
  //   icon: "history",
  //   path: "history",
  //   role: UserRole.USER,
  // },
  {
    id: 6,
    name: "Tiến trình",
    icon: "history",
    path: "process",
    role: UserRole.ADMIN,
  },
];
