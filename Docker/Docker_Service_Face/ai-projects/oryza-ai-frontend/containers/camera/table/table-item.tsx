import { cameraApi } from "@/api-client/camera";
import { TableAction } from "@/components";
import { LoadingPopup } from "@/components/common/loading/loading-popup";
import { DialogConfirm } from "@/components/dialog/confirm-dialog";
import { CreateCameraDialog } from "@/components/dialog/create-camera";
import { LoadingDialog } from "@/components/dialog/loading-dialog";
import { ResultEnum } from "@/constants/enum";
import { PaginateKey } from "@/constants/paginate-key";
import { useCameras } from "@/context/camera-context";
import useScrollToElement from "@/hooks/use-scroll-to-element";
import useHandleError from "@/hooks/useHandleError";
import { CameraRes } from "@/interfaces/camera";
import { useRouter } from "next/navigation";
import { enqueueSnackbar } from "notistack";
import { useState } from "react";
import { CopyBtn } from "@/components/common/button/copy-btn";

export interface ITableItemCameraProps {
  camera: CameraRes;
  index: number;
  reload: () => void;
}

export function TableItemCamera(props: ITableItemCameraProps) {
  // ************** --init state-- *****************
  const { camera, index } = props;
  const router = useRouter();
  const { total, setTotal } = useCameras();
  const [openEditDialog, setOpenEditDialog] = useState(false);
  const [openRemoveDialog, setOpenRemoveDialog] = useState(false);
  const [openReloadDialog, setOpenReloadDialog] = useState(false);
  const handleError = useHandleError();
  const [loading, setloading] = useState(false);

  // ************** --HANDLE UPDATE-- *****************
  const handleUpdate = async (formData: any) => {
    try {
      let payload: any = {
        ip_address: formData?.ip_address.trim() ?? "",
        name: formData?.name.trim() ?? "",
        password: formData?.password.trim() ?? "",
        rtsp: formData?.rtsp.trim() ?? "",
        username: formData?.username.trim() ?? "",
        is_ai: formData?.is_ai ?? false,
        brand_camera_id:
          formData?.brand_camera_id?.id ?? formData?.brand_camera_id ?? "",
        type_service_ids: formData?.type_service_ids ?? [],
        ward_id: formData?.ward_id ?? "",
        other_info: formData?.other_info ?? "",
      };
      if (formData?.port) {
        payload.port = formData.port;
      }

      await cameraApi.update(payload, camera.id);
      props.reload();
      enqueueSnackbar("Cập nhật camera thành công", { variant: "success" });
      return ResultEnum.success;
    } catch (error) {
      handleError(error, "Cập nhật camera không thành công");
      return ResultEnum.error;
    }
  };

  // ************** --HANDLE REMOVE-- *****************
  const handleRemove = async () => {
    setloading(true);
    try {
      await cameraApi.delete(camera.id);
      props.reload();
      setTotal(total - 1);
      enqueueSnackbar("Xóa camera thành công", { variant: "success" });
    } catch (error) {
      handleError(error, "Xóa camera không thành công");
    } finally {
      setloading(false);
    }
  };

  // ************** --SCROLL TO ELEMENT-- *****************
  const { handlePushRoute } = useScrollToElement();
  function pushToChild() {
    handlePushRoute("/camera", camera.id); // as id to params
    router.push("/camera/" + camera.id); // router push
  }

  return (
    <div
      id={camera.id} // required to scroll to element
      className="w-full flex flex-row min-w-[1200px] table-row-custom items-center"
    >
      <div
        onClick={pushToChild}
        className="w-[60px] py-6 flex justify-center"
      >
        {_renderText(index.toString())}
      </div>
      <div
        onClick={pushToChild}
        className="w-[35%] py-6 pr-3 flex justify-start"
      >
        {_renderText(camera.name)}
      </div>
      <div
        onClick={pushToChild}
        className="w-[25%] py-6 pr-3 flex justify-start"
      >
        {_renderText(camera.ip_address)}
      </div>
      <div
        onClick={pushToChild}
        className="w-[10%] py-6 pr-3 flex justify-start"
      >
        {_renderText(camera.port.toString())}
      </div>
      <div className="w-[30%] py-6 pr-3 flex justify-start">
          <div style={{ marginRight: '10px' }}>{_renderText(camera.id)}</div>
          <CopyBtn text={camera.id} title="camera id"/>
      </div>
      <div className="w-[10%] py-3 pr-3 flex justify-center">
        <TableAction
          onEdit={() => setOpenEditDialog(true)}
          onRemove={() => setOpenRemoveDialog(true)}
          onUpdate={() => {
            setOpenReloadDialog(true);
            setTimeout(() => {
              setOpenReloadDialog(false);
            }, 3000);
          }}
        />
      </div>

      {/* update dialog */}
      {openEditDialog && (
        <CreateCameraDialog
          open={openEditDialog}
          handleClose={() => setOpenEditDialog(false)}
          submit={handleUpdate}
          camera={camera}
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

      <LoadingDialog
        open={openReloadDialog}
        onClose={function (): void {
          setOpenReloadDialog(false);
        }}
        text="Camera đang được tải lại ..."
      />
    </div>
  );
}

function _renderText(text: string) {
  return <p className="font-medium text-grayOz text-sm break-all">{text}</p>;
}
