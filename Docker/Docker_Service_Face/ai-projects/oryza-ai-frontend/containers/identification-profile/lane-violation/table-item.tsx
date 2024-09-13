import { TableAction } from "@/components";
import { ResultEnum } from "@/constants/enum";
import { useAuth } from "@/hooks/auth-hook";
import useHandleError from "@/hooks/useHandleError";
import { Stack } from "@mui/material";
import { enqueueSnackbar } from "notistack";
import { useState } from "react";

import { laneViolationApi } from "@/api-client/setting_ai_process";
import { ConfigAILaneViolationDialog } from "@/components/dialog/config-ai-lane-violation";
import { CameraLaneViolation } from "@/interfaces/identification-profile/lane-violation";

export interface ILaneViolationTableProps {
  data: CameraLaneViolation;
  index: number;
  reload: any;
}

export function LaneViolationTable(props: ILaneViolationTableProps) {
  const { data } = props;
  const { profile } = useAuth();

  const [openConfigDialog, setOpenConfigDialog] = useState(false);
  const handleError = useHandleError();

  const handleClick = () => {};

  const handleCreate = async (formData: any) => {
    if (data?.setting) {
      return await handleUpdate(formData);
    } else {
      try {
        const payload = {
          ...formData,
          camera_id: data.id,
          id_company: profile?.company?.id,
        };
        console.log("handleCreateLaneViolation payload", payload);
        await laneViolationApi.create(payload);
        enqueueSnackbar("Cấu hình AI phát hiện lấn làn thành công", {
          variant: "success",
        });
        props.reload();
        return ResultEnum.success;
      } catch (error) {
        handleError(error, "Cấu hình AI phát hiện lấn làn không thành công");
        return ResultEnum.error;
      }
    }
  };

  const handleUpdate = async (formData: any) => {
    try {
      const payload = {
        ...formData,
        camera_id: data.id,
        id_company: profile?.company?.id,
      };
      console.log("handleUpdateLaneViolation payload", payload);
      await laneViolationApi.update(payload, data.setting?.id ?? "");
      enqueueSnackbar("Cập nhật cấu hình AI phát hiện lấn làn thành công", {
        variant: "success",
      });
      props.reload();
      return ResultEnum.success;
    } catch (error) {
      handleError(error, "Cập nhật cấu hình AI phát hiện lấn làn không thành công");
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
      <div onClick={handleClick} className="w-[45%] py-6 flex justify-start">
        {_renderText(data?.name)}
      </div>
      <div onClick={handleClick} className="w-[45%] py-6 flex justify-start">
        {_renderText(data?.ip_address)}
      </div>
      <div onClick={handleClick} className="w-[10%] py-6 flex justify-center">
        <TableAction
          onAIHandle={() => setOpenConfigDialog(true)}
          onRemove={() => {}}
        />
      </div>

      <ConfigAILaneViolationDialog
        open={openConfigDialog}
        handleClose={() => setOpenConfigDialog(false)}
        submit={handleCreate}
        data={data}
      />
    </Stack>
  );
}

function _renderText(text?: any) {
  return <p className="font-medium text-grayOz text-sm">{text ?? "--"}</p>;
}
