import { cameraBrandApi } from "@/api-client/setting/camera-brand";
import { TableAction } from "@/components";
import { LoadingPopup } from "@/components/common/loading/loading-popup";
import { DialogConfirm } from "@/components/dialog/confirm-dialog";
import { SettingCameraBrandDialog } from "@/components/dialog/create-setting-brand-camera";
import { ResultEnum } from "@/constants/enum";
import useHandleError from "@/hooks/useHandleError";
import { IBrandCamera } from "@/interfaces/brand-camera";
import moment from "moment";
import { enqueueSnackbar } from "notistack";
import { useState } from "react";

export interface ITableItemSettingBrandCameraProps {
  data: IBrandCamera;
  index: number;
  reload: () => void;
  setTotal: () => void;
}

export function TableItemSettingBrandCamera(
  props: ITableItemSettingBrandCameraProps
) {
  const { data, index } = props;
  const [openEditDialog, setOpenEditDialog] = useState(false);
  const [openRemoveDialog, setOpenRemoveDialog] = useState(false);
  const handleError = useHandleError();
  const [loading, setloading] = useState(false);

  const handleUpdate = async (formData: any) => {
    try {
      let newPayload = {
        ...formData,
      };
      if (formData?.name && data.name.trim() !== newPayload?.name.trim()) {
        newPayload.name = formData?.name.trim();
      } else {
        delete newPayload.name;
      }
      if (formData?.key && data.key.trim() !== newPayload?.key.trim()) {
        newPayload.key = formData?.key.trim();
      } else {
        delete newPayload.key;
      }

      if (Object.keys(newPayload).length === 0) {
        enqueueSnackbar("Cập nhật hãng camera thành công", {
          variant: "success",
        });
        return ResultEnum.success;
      }
      await cameraBrandApi.update(newPayload, props.data.id);
      props.reload();
      enqueueSnackbar("Cập nhật hãng camera thành công", {
        variant: "success",
      });
      return ResultEnum.success;
    } catch (error) {
      handleError(error, "Cập nhật hãng camera không thành công");
      return ResultEnum.error;
    }
  };

  const handleRemove = () => {
    setloading(true);
    cameraBrandApi
      .delete(props.data.id)
      .then((res) => {
        props.reload();
        props.setTotal();
        enqueueSnackbar("Xóa hãng camera thành công", { variant: "success" });
      })
      .catch((error) => {
        enqueueSnackbar("Xóa hãng camera không thành công", {
          variant: "error",
        });
      })
      .finally(() => {
        setloading(false);
      });
  };

  return (
    <div className="w-full flex flex-row min-w-[1200px] table-row-custom items-center">
      <div className="w-[60px] py-6 flex justify-center">
        {_renderText(index.toString())}
      </div>

      <div className="w-[30%] py-6 flex justify-start">
        {_renderText(data?.name ?? "")}
      </div>
      <div className="w-[30%] py-6 flex justify-start">
        {_renderText(data?.key ?? "")}
      </div>
      <div className="w-[30%] py-6 flex justify-start">
        {_renderText(moment(data?.created).format("DD/MM/yyyy HH:mm"))}
      </div>
      <div className="w-[10%] py-6 flex justify-center">
        <TableAction
          onEdit={() => setOpenEditDialog(true)}
          onRemove={() => setOpenRemoveDialog(true)}
        />
      </div>

      {openEditDialog && (
        <SettingCameraBrandDialog
          open={openEditDialog}
          handleClose={() => setOpenEditDialog(false)}
          submit={handleUpdate}
          data={data}
        />
      )}

      {/* remove dialog */}
      {openRemoveDialog && (
        <DialogConfirm
          close={() => setOpenRemoveDialog(false)}
          action={handleRemove}
          image={"/icons/bin.svg"}
          title={"Bạn chắc chắn xoá không?"}
          description={"Sau khi xoá, dữ liệu sẽ không được phục hồi."}
        />
      )}

      <LoadingPopup open={loading} />
    </div>
  );
}

function _renderText(text: string) {
  return <p className="font-medium text-grayOz text-sm">{text}</p>;
}
