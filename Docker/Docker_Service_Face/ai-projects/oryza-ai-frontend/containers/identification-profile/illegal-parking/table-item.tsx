import { illegalParkingApi } from "@/api-client/setting_ai_process";
import { TableAction } from "@/components";
import { ConfigAIIllegalParkingDialog } from "@/components/dialog/config-ai-illegal-parking";
import { ResultEnum } from "@/constants/enum";
import { useAuth } from "@/hooks/auth-hook";
import useHandleError from "@/hooks/useHandleError";
import { CameraIllegalParking } from "@/interfaces/identification-profile/illegal-parking";
import { Stack } from "@mui/material";
import { useRouter } from "next/navigation";
import { enqueueSnackbar } from "notistack";
import { useState } from "react";

export interface IIllegalParkingTableProps {
  data: CameraIllegalParking;
  index: number;
  reload: any;
}

export function IllegalParkingTable(props: IIllegalParkingTableProps) {
  const { data } = props;
  const { profile } = useAuth();

  const router = useRouter();
  const [openConfigDialog, setOpenConfigDialog] = useState(false);
  const handleError = useHandleError();

  const handleClick = () => {};

  const handleCreateCrow = async (formData: any) => {
    if (data?.setting) {
      return await handleUpdateCrow(formData);
    } else {
      try {
        const payload = {
          ...formData,
          camera_id: data.id,
          id_company: profile?.company?.id,
        };
        await illegalParkingApi.create(payload);
        enqueueSnackbar("Cấu hình AI phát hiện đậu đỗ trái phép thành công", {
          variant: "success",
        });
        props.reload();
        return ResultEnum.success;
      } catch (error) {
        handleError(error, "Cấu hình AI phát hiện đậu đỗ trái phép không thành công");
        return ResultEnum.error;
      }
    }
  };

  const handleUpdateCrow = async (formData: any) => {
    try {
      const payload = {
        ...formData,
        camera_id: data.id,
        id_company: profile?.company?.id,
      };

      await illegalParkingApi.update(payload, data.setting?.id ?? "");
      enqueueSnackbar("Cập nhật cấu hình AI Đậu đỗ trái phép thành công", {
        variant: "success",
      });
      props.reload();
      return ResultEnum.success;
    } catch (error) {
      handleError(error, "Cập nhật cấu hình AI Đậu đỗ trái phép không thành công");
      return ResultEnum.error;
    }
  };

  return (
    <Stack
      className=" table-row-custom"
      sx={{
        minWidth: "1200px",
        alignItems: "center",
        display: "flex",
        flexDirection: "row",
      }}
    >
      <div onClick={handleClick} className="w-[60px] py-6 flex justify-center">
        {_renderText(props.index.toString())}
      </div>
      <div onClick={handleClick} className="w-[30%] py-6 flex justify-start">
        {_renderText(data?.name)}
      </div>
      <div onClick={handleClick} className="w-[30%] py-6 flex justify-start">
        {_renderText(data?.ip_address)}
      </div>
      <div onClick={handleClick} className="w-[15%] py-6 flex justify-center">
        {_renderText(data?.setting?.waiting_time)}
      </div>
      <div onClick={handleClick} className="w-[15%] py-6 flex justify-center">
        {_renderText(data?.setting?.alert_interval)}
      </div>

      <div onClick={handleClick} className="w-[10%] py-6 flex justify-center">
        <TableAction
          onAIHandle={() => setOpenConfigDialog(true)}
          onRemove={() => {}}
        />
      </div>

      <ConfigAIIllegalParkingDialog
        open={openConfigDialog}
        handleClose={() => setOpenConfigDialog(false)}
        submit={handleCreateCrow}
        data={data}
      />
    </Stack>
  );
}

function _renderText(text?: any) {
  return <p className="font-medium text-grayOz text-sm">{text ?? "--"}</p>;
}
