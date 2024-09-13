import { Outline2Btn } from "@/components/common/button/outline-2-btn";
import { useState } from "react";
import Image from "next/image";
import { authApi } from "@/api-client";
import { enqueueSnackbar } from "notistack";

export interface IPasswordComponentsProps {}

export function PasswordComponents(props: IPasswordComponentsProps) {
  const [isEdit, setIsEdit] = useState(false);

  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");

  const handleUpdateMe = () => {
    let payload = {
      current_password: currentPassword,
      new_password: newPassword,
    };
    authApi
      .updateMe(payload)
      .then((res) => {
        enqueueSnackbar("Đổi mật khẩu thành công", { variant: "success" });
        setNewPassword("");
        setCurrentPassword("");
        setIsEdit(false);
      })
      .catch((error: any) => {
        enqueueSnackbar("Đổi mật khẩu không thành công", {
          variant: "error",
        });
      });
  };

  return (
    <div
      className={[
        "flex flex-row justify-between items-center py-3 border-b-2 transition-all duration-300",
        isEdit ? "border-[#78C6E7]" : "border-[#F8F8F8]",
      ].join(" ")}
    >
      {isEdit === false ? (
        <div>
          <p className="text-blackOz text-[18px] font-normal ">Mật khẩu</p>
          <div className="h-7    items-center flex  ">
            <p className="text-[#8E95A9] text-[14px] font-normal ">
              Cài mật khẩu khác biệt để bảo vệ an toàn cho tài khoản của bạn.
            </p>
          </div>
        </div>
      ) : (
        <div className="flex flex-row">
          <div>
            <p className="text-blackOz text-[18px] font-normal ">Mật khẩu củ</p>
            <input
              type="password"
              className="  outline-none text-blackOz font-normal text-base h-7"
              placeholder="Nhập mật khẩu mới ..."
              autoFocus
              value={currentPassword}
              onChange={(e) => setCurrentPassword(e.target.value)}
            />
          </div>
          <div>
            <p className="text-blackOz text-[18px] font-normal ">
              Mật khẩu mới
            </p>
            <input
              type="password"
              className="  outline-none text-blackOz font-normal text-base h-7"
              placeholder="Nhập lại mật khẩu mới..."
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
            />
          </div>
        </div>
      )}

      {isEdit === false ? (
        <div className="flex flex-row space-x-24 items-center ">
          <Outline2Btn
            onClick={() => setIsEdit(true)}
            text={"Đổi mật khẩu"}
            icon="/icons/edit-button.svg"
          />
        </div>
      ) : (
        <div className="flex flex-row space-x-4 ">
          <Outline2Btn
            onClick={() => {
              setIsEdit(false);
              setNewPassword("");
              setCurrentPassword("");
            }}
            text={"Hủy thay đổi"}
            icon="/icons/cancel.svg"
          />
          <div
            onClick={() => {
              if (currentPassword.trim() !== "" && newPassword.trim() != "") {
                handleUpdateMe();
              }
            }}
            className={[
              "h-10 flex flex-row items-center space-x-2 rounded-lg px-3 py-2 select-none transition-all duration-300 cursor-pointer bg-primary shadow-shadown1",
              currentPassword.trim() !== "" && newPassword.trim() != ""
                ? "opacity-100"
                : "opacity-10",
            ].join(" ")}
          >
            <Image
              src="/icons/email.svg"
              alt="edit-btn"
              width={20}
              height={20}
            />
            <p className="text-white font-medium text-[14px]">Lưu mật khẩu</p>
          </div>
        </div>
      )}
    </div>
  );
}
