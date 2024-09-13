import { uniformApi } from "@/api-client/identification-profile/uniform";
import { TableAction } from "@/components";
import { CongigUniformDialog } from "@/components/dialog/config-ai-uniform";
import { ResultEnum } from "@/constants/enum";
import { useAuth } from "@/hooks/auth-hook";
import useHandleError from "@/hooks/useHandleError";
import { Stack } from "@mui/material";
import { useRouter } from "next/navigation";
import { enqueueSnackbar } from "notistack";
import { useState } from "react";

export interface IUniformTableProps {
  data: any;
  index: number;
  reload: any;
}

export function UniformTable(props: IUniformTableProps) {
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
        await uniformApi.create(payload);
        enqueueSnackbar("Cấu hình AI nhận diện đồng phục thành công", {
          variant: "success",
        });
        props.reload();
        return ResultEnum.success;
      } catch (error) {
        handleError(error, "Cấu hình AI nhận diện đồng phục không thành công");
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

      await uniformApi.update(payload, data.setting?.id ?? "");
      enqueueSnackbar("Cập nhật cấu hình AI nhận diện đồng phục thành công", {
        variant: "success",
      });
      props.reload();
      return ResultEnum.success;
    } catch (error) {
      handleError(error, "Cập nhật cấu hình AI nhận diện đồng phục không thành công");
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

      <CongigUniformDialog
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
