import { LoadingPopup } from "@/components/common/loading/loading-popup";
import TextFieldFormV2 from "@/components/common/text-field/text-field-form-v2";
import { WebhookRes } from "@/interfaces/webhook";
import { Validator } from "@/utils/validate";
import CloseRoundedIcon from "@mui/icons-material/CloseRounded";
import { Grid, IconButton } from "@mui/material";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogTitle from "@mui/material/DialogTitle";
import Slide from "@mui/material/Slide";
import { TransitionProps } from "@mui/material/transitions";
import * as React from "react";
import { useState } from "react";
import { ChooseServer } from "../../input-field/choose-server";
import { ConfirmCloseDialog } from "../confirm-dialog/confirm-close-dialog";
import { ResultEnum } from "@/constants/enum";
import useFormSubmit from "@/hooks/useFromSubmit";
import { SelectCustom } from "@/components/common/select/select";
import { ChooseTokenType } from "@/components/input-field/choose-token-type";

const Transition = React.forwardRef(function Transition(
  props: TransitionProps & {
    children: React.ReactElement<any, any>;
  },
  ref: React.Ref<unknown>
) {
  return <Slide direction="up" ref={ref} {...props} />;
});

export interface ISettingWebhookDialogProps {
  open: boolean;
  handleClose: () => void;
  submit: (data: any) => Promise<ResultEnum>;
  data?: WebhookRes;
}

export function SettingWebhookDialog(props: ISettingWebhookDialogProps) {
  const { open, handleClose, submit, data } = props;
  const [formErr, setFormErr] = useState<any>({});

  const checkValidate = (formData: any) => {
    let hasError = false;

    const name = Validator.checkNotEmpty(formData["name"] ?? "");
    const endpoint = Validator.checkNotEmpty(formData["endpoint"] ?? "");
    const type_service_id = Validator.checkNotEmpty(
      formData["type_service_id"] ?? ""
    );

    let error = {
      ...formErr,
      name: name,
      endpoint: endpoint,
      type_service_id: type_service_id,
    };

    if (
      error.name !== null ||
      error.endpoint !== null ||
      error.type_service_id !== null
    ) {
      hasError = true;
    }

    setFormErr(error);

    return !hasError;
  };

  const onClose = () => {
    setFormErr({});
    handleClose();
  };

  const [confirmDialog, setConfirmDialog] = useState(false);

  const { loading, handleSubmit } = useFormSubmit(submit, checkValidate);

  return (
    <Dialog
      open={open}
      TransitionComponent={Transition}
      onClose={() => setConfirmDialog(true)}
      aria-describedby="alert-dialog-slide-description"
      PaperProps={{
        sx: {
          borderRadius: "11px",
          boxShadow: "0px 1px 10px 0px rgba(34, 34, 34, 0.10)",
          padding: "16px",
          position: "relative",
          width: "500px",
          overflow: "unset",
        },
        component: "form",
        onSubmit: async (event: React.FormEvent<HTMLFormElement>) => {
          const result = await handleSubmit(event);
          if (result === ResultEnum.success) handleClose();
        },
      }}
    >
      <ConfirmCloseDialog
        open={confirmDialog}
        onClose={function (event: any): void {
          setConfirmDialog(false);
        }}
        submit={function (): void {
          setConfirmDialog(false);
          onClose();
        }}
      />
      <LoadingPopup open={loading} />
      {/* close btn */}
      <IconButton
        onClick={() => setConfirmDialog(true)}
        aria-label="delete"
        size="small"
        title="Đóng"
        className="w-[24px] h-[24px] flex top-[16px] right-[16px]"
        sx={{
          position: "absolute",
        }}
      >
        <CloseRoundedIcon fontSize="inherit" />
      </IconButton>

      <DialogTitle className="text-center text-[#1C2A53] text-xl font-medium">
        {data ? "Chỉnh sửa webhook" : "Tạo mới webhook"}
      </DialogTitle>
      <DialogContent sx={{ overflow: "unset" }}>
        <Grid container spacing={2}>
          <Grid item xs={12}>
            <TextFieldFormV2
              label="Tên"
              required
              placeholder="Nhập tên..."
              name="name"
              defaultValue={data?.name ?? ""}
              textError={formErr?.name ?? ""}
            />
          </Grid>
          <Grid item xs={12}>
            <TextFieldFormV2
              label="URL"
              required
              placeholder="--"
              name="endpoint"
              defaultValue={data?.endpoint ?? ""}
              textError={formErr?.endpoint ?? ""}
            />
          </Grid>
          <Grid item xs={12}>
            <ChooseServer
              name={"type_service_id"}
              defaultValue={data?.type_service?.id ?? ""}
              textError={formErr?.type_service_id ?? ""}
            />
          </Grid>
          <Grid item xs={12}>
            <ChooseTokenType defaultValue={data?.auth_type} />
          </Grid>
          <Grid item xs={12}>
            <TextFieldFormV2
              label="Token"
              placeholder="--"
              name="token"
              defaultValue={data?.token ?? ""}
            />
          </Grid>
        </Grid>
      </DialogContent>
      <DialogActions sx={{ justifyContent: "center", gap: "16px" }}>
        <button
          type="button"
          onClick={() => setConfirmDialog(true)}
          className="min-w-[100px] shadow-shadown1 bg-white rounded-lg px-[14px] py-2 capitalize text-grayOz font-semibold text-sm hover:bg-white hover:shadow-shadown1"
        >
          Hủy bỏ
        </button>
        <button
          type="submit"
          className="min-w-[100px] shadow-shadown1 bg-primary rounded-lg px-[14px] py-2 capitalize text-white font-semibold text-sm hover:bg-primaryDark"
        >
          {data ? "Xác nhận" : "Tạo mới"}
        </button>
      </DialogActions>
    </Dialog>
  );
}
