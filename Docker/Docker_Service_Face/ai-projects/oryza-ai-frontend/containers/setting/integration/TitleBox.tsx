import { vmsApi } from "@/api-client/setting/vms";
import { LoadingPopup } from "@/components/common/loading/loading-popup";
import useHandleError from "@/hooks/useHandleError";
import Image from "next/image";
import { enqueueSnackbar } from "notistack";
import { useState } from "react";
import { ITitleBoxProps } from "./title-box";

export function TitleBox(props: ITitleBoxProps) {
  const [loading, setloading] = useState(false);
  const handleError = useHandleError();

  const handleSync = async () => {
    setloading(true);
    try {
      await vmsApi.syncCamera();
      enqueueSnackbar("Đồng bộ thành công", {
        variant: "success",
      });
    } catch (error) {
      // handleError(error, "Đồng bộ không thành công");
    } finally {
      setloading(false);
    }
  };

  return (
    <div className="w-full bg-grayOz flex flex-row justify-between items-center px-8 py-4 ">
      <LoadingPopup open={loading} />
      <div className="text-white text-[14px] font-normal ">
        <p className="text-white text-[24px] font-medium pb-3">Tích hợp VMS</p>
        <p>
          Nhập thông tin kết nối theo bên dưới và mật khẩu tài khoản quản trị
          viên để kết nối Oryza AI với Oryza VMS Server.
        </p>
        <p>
          Đảm bảo rằng bạn đã cài đặt chương trình [ Oryza AI Nx Plugin ] trước
          khi tiếp tục.
        </p>
      </div>
      <div
        onClick={handleSync}
        className=" flex flex-row p-3 rounded-[4px] bg-[#FFAC47] space-x-2  items-center select-none cursor-pointer hover:opacity-85 transition-all duration-300 "
      >
        <div className="bg-black  w-4 h-4 rounded-[4px] flex items-center justify-center p-[2px] ">
          <Image src="/icons/sync.svg" width={16} height={16} alt="sync-icon" />
        </div>
        <p className="text-black font-normal text-[14px]">Đồng bộ</p>
      </div>
    </div>
  );
}
