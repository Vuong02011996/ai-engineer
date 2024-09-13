import { personCameraApi } from "@/api-client/identification-profile/person-camera";
import { useRouter } from "next/router";
import { enqueueSnackbar } from "notistack";
import { ConfirmDialogV2 } from "../confirm-dialog/v2";

export interface ICreateMultipleCameraProps {
  open: boolean;
  handleClose: () => void;
  presonId: string;
}

export function CreateMultipleCamera(props: ICreateMultipleCameraProps) {
  const { open, handleClose, presonId } = props;
  const router = useRouter();

  //* create multiple camera person
  const handleCreateAll = async () => {
    if (!presonId) return;

    try {
      await personCameraApi.createMultipleCameraPerson(presonId);
    } catch (error) {
      enqueueSnackbar("Bật tất cả camera không thành công", {
        variant: "error",
      });
    }
  };

  return (
    <>
      <ConfirmDialogV2
        open={open}
        handleClose={handleClose}
        title={"Xác Nhận Bật Tất Cả Camera"}
        summany={`Vui lòng xác nhận việc bật tất cả camera cho người dùng này. Hành động
      này sẽ kích hoạt tất cả các camera liên quan. Bạn có chắc chắn muốn
      tiếp tục không?`}
        submit={handleCreateAll}
      />
    </>
  );
}
