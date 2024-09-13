import { leavingApi } from "@/api-client/setting_ai_process";
import { TableAction } from "@/components";
import { ConfigAILeavingDialog } from "@/components/dialog/config-ai-leaving";
import { ResultEnum } from "@/constants/enum";
import { useAuth } from "@/hooks/auth-hook";
import useHandleError from "@/hooks/useHandleError";
import { Stack } from "@mui/material";
import { enqueueSnackbar } from "notistack";
import { useState } from "react";

export interface ILeavingTableProps {
  data: any;
  index: number;
  reload: any;
}

export function LeavingTable(props: ILeavingTableProps) {
  const { data } = props;
  const { profile } = useAuth();

  const [openConfigDialog, setOpenConfigDialog] = useState(false);
  const handleError = useHandleError();

  const handleClick = () => {};

  const handleCreateLeaving = async (formData: any) => {
    if (data?.setting) {
      return await handleUpdateLeaving(formData);
    } else {
      try {
        const payload = {
          ...formData,
          camera_id: data.id,
          id_company: profile?.company?.id,
        };
        await leavingApi.create(payload);
        enqueueSnackbar("Cập nhật cấu hình AI phát hiện đối tượng rời vị trí thành công", {
          variant: "success",
        });
        props.reload();
        return ResultEnum.success;
      } catch (error) {
        handleError(error, "Cập nhật cấu hình AI phát hiện đối tượng rời vị trí không thành công");
        return ResultEnum.error;
      }
    }
  };

  const handleUpdateLeaving = async (formData: any) => {
    try {
      const payload = {
        ...formData,
        camera_id: data.id,
        id_company: profile?.company?.id,
      };

      await leavingApi.update(payload, data.setting?.id ?? "");
      enqueueSnackbar("Cập nhật cấu hình AI phát hiện đối tượng rời vị trí thành công", {
        variant: "success",
      });
      props.reload();
      return ResultEnum.success;
    } catch (error) {
      handleError(error, "Cập nhật cấu hình AI phát hiện đối tượng rời vị trí không thành công");
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
      <div onClick={handleClick} className="w-[40%] py-6 flex justify-start">
        {_renderText(data?.ip_address)}
      </div>
      <div onClick={handleClick} className="w-[10%] py-6 flex justify-center">
        {_renderText(data?.setting?.waiting_time)}
      </div>

      <div onClick={handleClick} className="w-[10%] py-6 flex justify-center">
        <TableAction
          onAIHandle={() => setOpenConfigDialog(true)}
          onRemove={() => {}}
        />
      </div>

      <ConfigAILeavingDialog
        open={openConfigDialog}
        handleClose={() => setOpenConfigDialog(false)}
        submit={handleCreateLeaving}
        data={data}
      />
    </Stack>
  );
}

function _renderText(text?: any) {
  return <p className="font-medium text-grayOz text-sm">{text ?? "--"}</p>;
}
