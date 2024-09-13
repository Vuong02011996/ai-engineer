import { plateNumberApi } from "@/api-client/setting_ai_process";
import { TableAction } from "@/components";
import { ConfigAIPlateNumberDialog } from "@/components/dialog/config-ai-plate-number";
import { ResultEnum } from "@/constants/enum";
import { useAuth } from "@/hooks/auth-hook";
import useHandleError from "@/hooks/useHandleError";
import { CameraPlateNumber } from "@/interfaces/identification-profile/plate-number";
import { Stack } from "@mui/material";
import { useRouter } from "next/navigation";
import { enqueueSnackbar } from "notistack";
import { useState } from "react";

export interface IPlateNumberTableItemProps {
  data: CameraPlateNumber;
  index: number;
  reload: any;
  // setTotal: any;
}

export function PlateNumberTableItem(props: IPlateNumberTableItemProps) {
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
          camera_id: data.id,
          id_company: profile?.company?.id,
          line: formData?.boundary,
          object_detect: formData?.object_detect,
          image_url: formData?.image_url,
        };
        await plateNumberApi.create(payload);
        enqueueSnackbar("Cấu hình AI nhận diện biển số thành công", {
          variant: "success",
        });
        props.reload();
        return ResultEnum.success;
      } catch (error) {
        handleError(error, "Cấu hình AI nhận diện biển số không thành công");
        return ResultEnum.error;
      }
    }
  };

  const handleUpdateCrow = async (formData: any) => {
    try {
      const payload = {
        line: formData?.boundary,
        object_detect: formData?.object_detect,
        image_url: formData?.image_url,
      };

      await plateNumberApi.update(payload, data.setting?.id ?? "");
      enqueueSnackbar("Cập nhật cấu hình AI nhận diện biển số thành công", {
        variant: "success",
      });
      props.reload();
      return ResultEnum.success;
    } catch (error) {
      handleError(error, "Cập nhật cấu hình AI nhận diện biển số không thành công");
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
      <div onClick={handleClick} className="w-[30%] py-6 flex justify-start">
        {_renderText(data?.ip_address)}
      </div>
      <div onClick={handleClick} className="w-[20%] py-6 flex justify-center">
        {_renderText(
          data?.setting?.object_detect === "plate"
            ? "Biển số"
            : data?.setting?.object_detect === "vehicle"
            ? "Biển số và loại xe"
            : ""
        )}
      </div>
      <div onClick={handleClick} className="w-[10%] py-6 flex justify-center">
        <TableAction
          onAIHandle={() => setOpenConfigDialog(true)}
          onRemove={() => {}}
        />
      </div>

      <ConfigAIPlateNumberDialog
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
