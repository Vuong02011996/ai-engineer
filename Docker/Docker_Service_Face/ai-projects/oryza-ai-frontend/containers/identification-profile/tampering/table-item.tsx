import { tamperingApi } from "@/api-client/identification-profile/tampering";
import { TableAction } from "@/components";
import { ConfigAITamperingDialog } from "@/components/dialog/config-ai-tampering";
import { ResultEnum } from "@/constants/enum";
import { useAuth } from "@/hooks/auth-hook";
import useHandleError from "@/hooks/useHandleError";
import { CameraLoiteringDetection } from "@/interfaces/identification-profile/loitering-detection";
import { Stack } from "@mui/material";
import { useRouter } from "next/navigation";
import { enqueueSnackbar } from "notistack";
import { useState } from "react";

export interface ITamperingTableProps {
  data: CameraLoiteringDetection;
  index: number;
  reload: any;
}

export function TamperingTable(props: ITamperingTableProps) {
  const { data } = props;
  const { profile } = useAuth();

  const router = useRouter();
  const [openConfigDialog, setOpenConfigDialog] = useState(false);
  const handleError = useHandleError();

  const handleClick = () => {};

  const handleCreateTampering = async (formData: any) => {
    if (data?.setting) {
      return await handleUpdateTampering(formData);
    } else {
      try {
        const payload = {
          ...formData,
          camera_id: data.id,
          id_company: profile?.company?.id,
        };
        await tamperingApi.create(payload);
        enqueueSnackbar("Cấu hình AI phát hiện phát hiện phá hoại thành công", {
          variant: "success",
        });
        props.reload();
        return ResultEnum.success;
      } catch (error) {
        handleError(error, "Cấu hình AI phát hiện phá hoại không thành công");
        return ResultEnum.error;
      }
    }
  };

  const handleUpdateTampering = async (formData: any) => {
    try {
      const payload = {
        ...formData,
        camera_id: data.id,
        id_company: profile?.company?.id,
      };

      await tamperingApi.update(payload, data.setting?.id ?? "");
      enqueueSnackbar("Cập nhật cấu hình AI phát hiện phá hoại thành công", {
        variant: "success",
      });
      props.reload();
      return ResultEnum.success;
    } catch (error) {
      handleError(error, "Cập nhật cấu hình AI phát hiện phá hoại không thành công");
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
      <div onClick={handleClick} className="w-[40%] py-6 flex justify-start">
        {_renderText(data?.name)}
      </div>
      <div onClick={handleClick} className="w-[20%] py-6 flex justify-start">
        {_renderText(data?.ip_address)}
      </div>
      <div onClick={handleClick} className="w-[30%] py-6 flex justify-center">
        {_renderText(data?.setting?.alarm_interval)}
      </div>

      <div onClick={handleClick} className="w-[10%] py-6 flex justify-center">
        <TableAction
          onAIHandle={() => setOpenConfigDialog(true)}
          onRemove={() => {}}
        />
      </div>

      <ConfigAITamperingDialog
        open={openConfigDialog}
        handleClose={() => setOpenConfigDialog(false)}
        submit={handleCreateTampering}
        data={data}
      />
    </Stack>
  );
}

function _renderText(text?: any) {
  return <p className="font-medium text-grayOz text-sm">{text ?? "--"}</p>;
}
