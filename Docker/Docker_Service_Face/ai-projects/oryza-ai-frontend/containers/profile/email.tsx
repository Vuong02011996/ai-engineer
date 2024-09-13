import { Outline2Btn } from "@/components/common/button/outline-2-btn";
import { useAuth } from "@/hooks/auth-hook";
import Image from "next/image";
import { useState } from "react";

export interface IEmailComponentsProps {}

export function EmailComponents(props: IEmailComponentsProps) {
  const [isEdit, setIsEdit] = useState(false);
  const [inputValue, setInputValue] = useState("");
  const { profile } = useAuth();

  return (
    <div
      className={[
        "flex flex-row justify-between items-center py-3 border-b-2 transition-all duration-300",
        isEdit ? "border-[#78C6E7]" : "border-[#F8F8F8]",
      ].join(" ")}
    >
      <div>
        <p className="text-blackOz text-[18px] font-normal ">Địa chỉ email</p>
        {isEdit === false ? (
          <div className="h-7    items-center flex  ">
            <p className="text-[#8E95A9] text-[14px] font-normal ">
              Địa chỉ email liên kết với tài khoản của bạn.
            </p>
          </div>
        ) : (
          <input
            type="text"
            className="  outline-none text-blackOz font-normal text-base h-7"
            placeholder="Nhập email mới ..."
            autoFocus
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
          />
        )}
      </div>
      {isEdit === false ? (
        <div className="flex flex-row space-x-24 items-center ">
          <div className=" ">
            <p className="text-blackOz text-[18px] font-normal ">
              {profile?.email || ""}
            </p>
            <p className="text-[#22AE68] text-[14px] font-normal ">
              Đã xác thực
            </p>
          </div>
          {/* <Outline2Btn
            onClick={() => setIsEdit(true)}
            text={"Chỉnh sửa"}
            icon="/icons/edit-button.svg"
          /> */}
        </div>
      ) : (
        <div className="flex flex-row space-x-4 ">
          <Outline2Btn
            onClick={() => setIsEdit(false)}
            text={"Hủy thay đổi"}
            icon="/icons/cancel.svg"
          />
          <div className="h-10 flex flex-row items-center space-x-2 rounded-lg px-3 py-2 select-none transition-all duration-300 cursor-pointer bg-primary shadow-shadown1">
            <Image
              src="/icons/email.svg"
              alt="edit-btn"
              width={20}
              height={20}
            />
            <p className="text-white font-medium text-[14px]">Xác thực email</p>
          </div>
        </div>
      )}
    </div>
  );
}
