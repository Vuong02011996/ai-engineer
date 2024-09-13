import { webhookApi } from "@/api-client/setting/webhook";
import { TableAction } from "@/components";
import { LoadingPopup } from "@/components/common/loading/loading-popup";
import { SwitchBtn } from "@/components/common/switch/switch-btn";
import { DialogConfirm } from "@/components/dialog/confirm-dialog";
import { SettingWebhookDialog } from "@/components/dialog/create-setting-webhook";
import { LoadingDialog } from "@/components/dialog/loading-dialog";
import { ResultEnum } from "@/constants/enum";
import { useWebhook } from "@/context/webhook-context";
import useHandleError from "@/hooks/useHandleError";
import { WebhookRes } from "@/interfaces/webhook";
import { enqueueSnackbar } from "notistack";
import { useState } from "react";

export interface ITableItemSettingWebhookProps {
  data: WebhookRes;
  index: number;
  reload: () => void;
}

export function TableItemSettingWebhook(props: ITableItemSettingWebhookProps) {
  const { index } = props;
  const { total, setTotal } = useWebhook();
  const [openEditDialog, setOpenEditDialog] = useState(false);
  const [openRemoveDialog, setOpenRemoveDialog] = useState(false);
  const [loading, setLoading] = useState(false);
  const [openReloadDialog, setOpenReloadDialog] = useState(false);
  const handleError = useHandleError();

  const handleUpdate = async (formData: any) => {
    try {
      let newPayload = {
        ...formData,
      };
      if (formData?.name) {
        newPayload.name = formData?.name.trim();
      }
      if (formData?.endpoint) {
        newPayload.endpoint = formData?.endpoint.trim();
      }

      if (newPayload.type_service_id === props.data.type_service) {
        delete newPayload.type_service_id;
      }
      if (newPayload.name === props.data.name) {
        delete newPayload.name;
      }
      if (newPayload.endpoint === props.data.endpoint) {
        delete newPayload.endpoint;
      }
      if (newPayload.token === props.data.token) {
        delete newPayload.token;
      }
      if (newPayload.auth_type === props.data.auth_type) {
        delete newPayload.auth_type;
      }
      if (Object.keys(newPayload).length === 0) return ResultEnum.success;
      setLoading(true);

      await webhookApi.update(newPayload, props.data.id);
      props.reload();
      enqueueSnackbar("Cập nhật webhook thành công", {
        variant: "success",
      });
      return ResultEnum.success;
    } catch (error) {
      handleError(error, "Đã xảy ra lỗi khi cập nhật webhook");
      return ResultEnum.error;
    } finally {
      setLoading(false);
    }
  };

  const handleRemove = async () => {
    setLoading(true);
    try {
      await webhookApi.delete(props.data.id);
      props.reload();
      setTotal(total - 1);
      enqueueSnackbar("Xóa webhook thành công", { variant: "success" });
    } catch (error) {
      const handleError = useHandleError();
      handleError(error, "Đã xảy ra lỗi khi xóa webhook");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full flex flex-row min-w-[1200px] table-row-custom items-center">
      <div className="w-[60px] py-6 flex justify-center">
        {_renderText(index.toString())}
      </div>
      <div className="w-[25%] py-6 flex justify-start">
        {_renderText(props.data?.name ?? "")}
      </div>
      <div className="w-[25%] py-6 flex justify-start">
        {_renderText(props.data?.endpoint ?? "")}
      </div>
      <div className="w-[25%] py-6 flex justify-start">
        {_renderText(props.data?.type_service?.name ?? "")}
      </div>
      <div className="w-[15%] py-6 flex justify-start">
        <SwitchBtn
          checked={props.data.status}
          onChange={(e) => {
            if (loading) return;
            handleUpdate({ status: e.target.checked });
          }}
        />
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
          onCopy={() => {
            try {
              navigator.clipboard.writeText(props.data?.endpoint ?? "");
              enqueueSnackbar("Dữ liệu đã được lưu vào khay nhớ tạm", {
                variant: "default",
              });
            } catch (error) {
              enqueueSnackbar("Dữ liệu chưa được lưu vào khay nhớ tạm", {
                variant: "error",
              });
            }
          }}
        />
      </div>

      {/* update dialog */}
      <SettingWebhookDialog
        open={openEditDialog}
        handleClose={() => setOpenEditDialog(false)}
        submit={handleUpdate}
        data={props.data}
      />

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
        text="Webhook đang được tải lại ..."
      />
    </div>
  );
}

function _renderText(text: string) {
  return <p className="font-medium text-grayOz text-sm">{text}</p>;
}
