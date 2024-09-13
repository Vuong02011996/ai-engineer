import { crowdApi } from "@/api-client/setting_ai_process";
import { TableAction } from "@/components";
import { ConfigAICrowdDialog } from "@/components/dialog/config-ai-crowd";
import { ResultEnum } from "@/constants/enum";
import { useAuth } from "@/hooks/auth-hook";
import useHandleError from "@/hooks/useHandleError";
import { CameraCrowd } from "@/interfaces/identification-profile/crowd";
import { Stack } from "@mui/material";
import { useRouter } from "next/navigation";
import { enqueueSnackbar } from "notistack";
import { useState } from "react";

export interface ICrowdTableItemProps {
  data: CameraCrowd;
  index: number;
  reload: any;
  // setTotal: any;
}

export function CrowdTableItem(props: ICrowdTableItemProps) {
  const { data } = props;
  const { profile } = useAuth();

  const router = useRouter();
  const [openConfigDialog, setOpenConfigDialog] = useState(false);
  const handleError = useHandleError();

  const handleClick = () => {};

  const handleCreateCrow = async (formData: any) => {
    if (data?.crowdData) {
      return await handleUpdateCrow(formData);
    } else {
      try {
        const payload = {
          ...formData,
          camera_id: data.id,
          id_company: profile?.company?.id,
        };
        await crowdApi.create(payload);
        enqueueSnackbar("Cấu hình AI phát diện đám đông thành công", {
          variant: "success",
        });
        props.reload();
        return ResultEnum.success;
      } catch (error) {
        handleError(error, "Cấu hình AI phát diện đám đông không thành công");
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

      await crowdApi.update(payload, data.crowdData?.id ?? "");
      enqueueSnackbar("Cập nhật cấu hình AI phát hiện đám đông thành công", {
        variant: "success",
      });
      props.reload();
      return ResultEnum.success;
    } catch (error) {
      handleError(error, "Cập nhật cấu hình AI phát hiện đám đông không thành công");
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
      <div onClick={handleClick} className="w-[20%] py-6 flex justify-start">
        {_renderText(data?.name)}
      </div>
      <div onClick={handleClick} className="w-[10%] py-6 flex justify-start">
        {_renderText(data?.ip_address)}
      </div>
      <div onClick={handleClick} className="w-[25%] py-6 flex justify-center">
        {_renderText(data?.crowdData?.min_human_count)}
      </div>
      <div onClick={handleClick} className="w-[25%] py-6 flex justify-center">
        {_renderText(data?.crowdData?.min_neighbours)}
      </div>
      <div onClick={handleClick} className="w-[10%] py-6 flex justify-center">
        {_renderText(data?.crowdData?.distance_threshold)}
      </div>
      <div onClick={handleClick} className="w-[10%] py-6 flex justify-center">
        <TableAction
          onAIHandle={() => setOpenConfigDialog(true)}
          onRemove={() => {}}
        />
      </div>

      <ConfigAICrowdDialog
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
