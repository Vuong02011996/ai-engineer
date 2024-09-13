import * as React from "react";
import { Status, TableAction } from "@/components";
import { SwitchBtn } from "@/components/common/switch/switch-btn";
import { ServiceRes } from "@/interfaces/service";
import { CreateServiceDialog } from "@/components/dialog/create-service";
import { useState } from "react";
import { serviceApi } from "@/api-client/service";
import { enqueueSnackbar } from "notistack";
import { DialogConfirm } from "@/components/dialog/confirm-dialog";
import { useService } from "@/context/service-context";
import { LoadingDialog } from "@/components/dialog/loading-dialog";

export interface ITableItemCameraProps {
  data: ServiceRes;
  index: number;
  reload?: () => void;
}

export function TableItemCamera(props: ITableItemCameraProps) {
  const { data, index } = props;
  const { total, setTotal } = useService();

  const [openEditDialog, setOpenEditDialog] = useState(false);
  const [openRemoveDialog, setOpenRemoveDialog] = useState(false);
  const [openReloadDialog, setOpenReloadDialog] = useState(false);

  const handleUpdateService = (formData: any) => {
    serviceApi
      .update({ ...formData, name: formData?.name.trim() }, data.id)
      .then((res) => {
        enqueueSnackbar("Cập nhật service thành công", { variant: "success" });
        if (props.reload) props.reload();
      })
      .catch((error: any) => {
        const errorMsg =
          error?.response?.data?.detail || "Cập nhật service không thành công";
        enqueueSnackbar(errorMsg, { variant: "error" });
      });
  };
  const handleRemove = () => {
    serviceApi
      .delete(data.id)
      .then((res) => {
        if (props.reload) props.reload();
        setTotal(total - 1);
        enqueueSnackbar("Xóa service thành công", { variant: "success" });
      })
      .catch(() => {
        enqueueSnackbar("Xóa service không thành công", { variant: "error" });
      });
  };
  return (
    <div className="w-full flex flex-row min-w-[1200px] table-row-custom items-center">
      <div className="w-[60px] py-6 flex justify-center">
        {_renderText(index.toString())}
      </div>
      <div className="w-[20%] py-6 flex justify-start">
        {_renderText(data?.name ?? "")}
      </div>
      <div className="w-[20%] py-6 flex justify-start">
        {_renderText(
          data?.type === "AI_CAMERA" ? "Camera AI" : "Camera thường"
        )}
      </div>
      <div className="w-[15%] py-6 flex justify-start">
        {_renderText(data?.count_process?.toString() ?? "--")}
      </div>
      <div className="w-[15%] py-6 flex justify-start">
        {_renderText(data?.max_process?.toString() ?? "")}
      </div>
      <div className="w-[5%] py-6 flex justify-start">
        {_renderText(data?.port ?? 0)}
      </div>
      <div className="w-[15%] py-6 flex justify-start">
        <Status status={data?.is_alive ? "ONLINE" : "OFFLINE"} />
      </div>
      <div className="w-[10%] py-6 flex justify-center">
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

      <CreateServiceDialog
        open={openEditDialog}
        handleClose={function (): void {
          setOpenEditDialog(false);
        }}
        submit={handleUpdateService}
        data={data}
      />
      {openRemoveDialog && (
        <DialogConfirm
          close={() => setOpenRemoveDialog(false)}
          action={handleRemove}
          image={"/icons/bin.svg"}
          title={"Bạn chắc chắn xoá không?"}
          description={"Sau khi xoá, dữ liệu sẽ không được phục hồi."}
        />
      )}

      <LoadingDialog
        open={openReloadDialog}
        onClose={function (): void {
          setOpenReloadDialog(false);
        }}
        text="Service đang được tải lại ..."
      />
    </div>
  );
}

function _renderText(text: string) {
  return <p className="font-medium text-grayOz text-sm">{text}</p>;
}
