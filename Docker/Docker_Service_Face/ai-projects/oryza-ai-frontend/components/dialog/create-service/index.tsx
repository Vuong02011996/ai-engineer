import TextFieldFormV2 from "@/components/common/text-field/text-field-form-v2";
import { CompanyRes } from "@/interfaces/company";
import CloseRoundedIcon from "@mui/icons-material/CloseRounded";
import {
  FormControl,
  FormControlLabel,
  FormLabel,
  Grid,
  IconButton,
  InputAdornment,
  Radio,
  RadioGroup,
} from "@mui/material";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogTitle from "@mui/material/DialogTitle";
import Slide from "@mui/material/Slide";
import { TransitionProps } from "@mui/material/transitions";
import * as React from "react";
import { ChooseServiceType } from "../../input-field/choose-service-type";
import { ServiceRes } from "@/interfaces/service";
import { ChooseTypeCamera } from "./choose-type";
import { useState } from "react";
import { Validator } from "@/utils/validate";
import { ConfirmCloseDialog } from "../confirm-dialog/confirm-close-dialog";

const Transition = React.forwardRef(function Transition(
  props: TransitionProps & {
    children: React.ReactElement<any, any>;
  },
  ref: React.Ref<unknown>
) {
  return <Slide direction="up" ref={ref} {...props} />;
});

export interface ICreateServiceDialogProps {
  open: boolean;
  handleClose: () => void;
  submit: (data: any) => void;
  data?: ServiceRes;
}

export function CreateServiceDialog(props: ICreateServiceDialogProps) {
  const { open, handleClose, submit, data } = props;
  const [formErr, setFormErr] = useState<any>({});

  const checkValidate = (formData: any) => {
    let hasError = false;

    const type = Validator.checkNotEmpty(formData["type"] ?? "");
    const name = Validator.checkNotEmpty(formData["name"] ?? "");
    const max_process = Validator.checkNumberString(
      formData["max_process"] ?? ""
    );
    const port = Validator.checkNumberString(formData["port"] ?? "");
    const type_service_id = Validator.checkNotEmpty(
      formData["type_service_id"] ?? ""
    );

    let error = {
      ...formErr,
      type: type,
      name: name,
      max_process: max_process,
      port: port,
      type_service_id: type_service_id,
    };

    if (
      error.type !== null ||
      error.name !== null ||
      error.max_process !== null ||
      error.port != null ||
      error.type_service_id != null
    ) {
      hasError = true;
    }

    setFormErr(error);

    return !hasError;
  };

  const onClose = () => {
    handleClose();
    setFormErr({});
  };

  const [confirmDialog, setConfirmDialog] = useState(false);

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
        },
        component: "form",
        onSubmit: (event: React.FormEvent<HTMLFormElement>) => {
          event.preventDefault();
          const formData = new FormData(event.currentTarget);
          const formJson = Object.fromEntries((formData as any).entries());
          if (!checkValidate(formJson)) return;
          submit(formJson);
          handleClose();
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
        {data ? "Chỉnh sửa service AI" : "Tạo mới service AI"}
      </DialogTitle>
      <DialogContent>
        <Grid container spacing={2}>
          <Grid item xs={12}>
            <ChooseTypeCamera
              defaultValue={data?.type ?? "AI_SERVICE"}
              textError={formErr?.type ?? ""}
            />
          </Grid>
          <Grid item xs={12}>
            <TextFieldFormV2
              label="Tên service"
              required
              placeholder="Nhập tên ..."
              name="name"
              defaultValue={data?.name ?? ""}
              textError={formErr?.name ?? ""}
            />
          </Grid>
          <Grid item xs={7}>
            <TextFieldFormV2
              label="Giới hạn tối đa"
              required
              placeholder="--"
              defaultValue={data?.max_process ?? ""}
              name="max_process"
              textError={formErr?.max_process ?? ""}
              endAdornment={
                <InputAdornment
                  position="end"
                  className="border-l border-[#AFAFAF] h-full pl-3 "
                >
                  <p className="text-[#AFAFAF]">camera</p>
                </InputAdornment>
              }
            />
          </Grid>
          <Grid item xs={5}>
            <TextFieldFormV2
              label="Port"
              required
              placeholder="--"
              name="port"
              textError={formErr?.port ?? ""}
              defaultValue={data?.port ?? ""}
            />
          </Grid>
          <Grid item xs={12}>
            <ChooseServiceType
              defaultValue={data?.type_service}
              textError={formErr?.type_service_id ?? ""}
              name="type_service_id"
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
