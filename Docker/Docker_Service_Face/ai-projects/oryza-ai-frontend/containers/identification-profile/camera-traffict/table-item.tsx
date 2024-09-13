import { cameraTraffictApi } from "@/api-client/identification-profile/camera-traffict";
import { TableAction } from "@/components";
import { ConfigCameraTraffictDialog } from "@/components/dialog/config-ai-camera-traffict";
import { ResultEnum } from "@/constants/enum";
import { useAuth } from "@/hooks/auth-hook";
import useHandleError from "@/hooks/useHandleError";
import { CameraTraffictDetection } from "@/interfaces/identification-profile/camera-traffict";
import { Stack } from "@mui/material";
import { enqueueSnackbar } from "notistack";
import { useState } from "react";

export interface ICameraTraffictTableProps {
  data: CameraTraffictDetection;
  index: number;
  reload: any;
}

export function CameraTraffictTable(props: ICameraTraffictTableProps) {
  const { data } = props;
  const { profile } = useAuth();
  const [openConfigDialog, setOpenConfigDialog] = useState(false);
  const handleError = useHandleError();

  /**
   * Asynchronous function to create a camera traffic configuration.
   */
  async function createCameraTraffict(formData: any) {
    try {
      const payload = {
        camera_id: data.id,
        id_company: profile?.company?.id,
        light_boundary: formData.boundary,
        image_url: formData.image_url,
      };

      await cameraTraffictApi.create(payload);
      const msg = "Cấu hình AI nhận diện tín hiệu đèn giao thông thành công";
      enqueueSnackbar(msg, { variant: "success" });
      props.reload();
      return ResultEnum.success;
    } catch (error) {
      const msg = "Cấu hình AI nhận diện tín hiệu đèn giao thông không thành công";
      handleError(error, msg);
      return ResultEnum.error;
    }
  }

  /**
   * Asynchronous function to update a camera traffic configuration.
   */
  const updateCameraTraffict = async (formData: any) => {
    try {
      const payload = {
        light_boundary: formData.boundary,
        image_url: formData.image_url,
        camera_id: data.id,
        id_company: profile?.company?.id,
      };

      await cameraTraffictApi.update(payload, data.setting?.id ?? "");
      const msg = "Cập nhật cấu hình AI nhận diện tín hiệu đèn giao thông thành công";
      enqueueSnackbar(msg, { variant: "success" });
      props.reload();
      return ResultEnum.success;
    } catch (error) {
      const msg =
        "Cập nhật cấu hình AI nhận diện tín hiệu đèn giao thông không thành công";
      handleError(error, msg);
      return ResultEnum.error;
    }
  };

  /**
   * Asynchronous function to submit a camera traffic configuration.
   */
  const submit = async (formData: any) => {
    if (data?.setting) {
      return await updateCameraTraffict(formData);
    } else {
      return await createCameraTraffict(formData);
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
      <div className="w-[60px] py-6 flex justify-center">
        {_renderText(props.index.toString())}
      </div>
      <div className="w-[40%] py-6 flex justify-start">
        {_renderText(data?.name)}
      </div>
      <div className="w-[40%] py-6 flex justify-start">
        {_renderText(data?.ip_address)}
      </div>

      <div className="w-[20%] py-6 flex justify-center">
        <TableAction
          onAIHandle={() => setOpenConfigDialog(true)}
          onRemove={() => {}}
        />
      </div>

      <ConfigCameraTraffictDialog
        open={openConfigDialog}
        handleClose={() => setOpenConfigDialog(false)}
        submit={submit}
        data={data}
      />
    </Stack>
  );
}

function _renderText(text?: any) {
  return <p className="font-medium text-grayOz text-sm">{text ?? "--"}</p>;
}
