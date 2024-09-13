import TextFieldFormV2 from "@/components/common/text-field/text-field-form-v2";
import { ServerRes } from "@/interfaces/server";
import { formatServerData } from "@/libs/server";
import { Validator } from "@/utils";
import CloseRoundedIcon from "@mui/icons-material/CloseRounded";
import { Grid, IconButton } from "@mui/material";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogTitle from "@mui/material/DialogTitle";
import Slide from "@mui/material/Slide";
import { TransitionProps } from "@mui/material/transitions";
import * as React from "react";
import { useEffect, useState } from "react";
import { ConfirmCloseDialog } from "../confirm-dialog/confirm-close-dialog";

const Transition = React.forwardRef(function Transition(
  props: TransitionProps & {
    children: React.ReactElement<any, any>;
  },
  ref: React.Ref<unknown>
) {
  return <Slide direction="up" ref={ref} {...props} />;
});

const formInit = {
  name: "",
  ip_address: "",
  is_alive: false,
};

export interface ICreateServerDialogProps {
  open: boolean;
  handleClose: () => void;
  submit: (data: any) => void;
  server?: ServerRes;
}

export function CreateServerDialog(props: ICreateServerDialogProps) {
  const { open, handleClose, submit, server } = props;

  const [formErr, setFormErr] = useState<any>({});
  const [formData, setFormData] = useState<any>(formInit);

  const handleChange = (name: string, value: string) => {
    setFormData({ ...formData, [name]: value });
  };

  useEffect(() => {
    if (server) {
      let response: ServerRes[] = formatServerData([server]);
      setFormData(response[0]);
    }
  }, [server]);

  const handleSubmit = () => {
    if (!checkValidate()) return;

    submit(formData);
    setFormData(formInit);
    props.handleClose();
  };

  const checkValidate = () => {
    let hasError = false;
    const MIN = 2;
    const MAX = 150;

    const name = Validator.checkNotEmpty(formData["name"] ?? "", MIN, MAX);
    const ip = Validator.validateIPAddress(formData["ip_address"] ?? "");

    let error = {
      ...formErr,
      name: name,
      ip_address: ip,
    };

    if (error.name !== null || error.ip_address !== null) {
      hasError = true;
    }

    setFormErr(error);

    return !hasError;
  };

  const onClose = () => {
    handleClose();
    setFormErr({});
    setFormData(formInit);
  };

  const [confirmDialog, setConfirmDialog] = useState(false);

  return (
    <Dialog
      open={open}
      TransitionComponent={Transition}
      onClose={(event: any) => {
        event.stopPropagation();
        setConfirmDialog(true);
      }}
      aria-describedby="alert-dialog-slide-description"
      fullWidth
      maxWidth="xs"
      PaperProps={{
        sx: {
          borderRadius: "11px",
          boxShadow: "0px 1px 10px 0px rgba(34, 34, 34, 0.10)",
          padding: "16px",
          position: "relative",
        },
      }}
    >
      <ConfirmCloseDialog
        open={confirmDialog}
        onClose={function (): void {
          setConfirmDialog(false);
        }}
        submit={function (): void {
          setConfirmDialog(false);
          onClose();
        }}
      />

      {/* close btn */}
      <IconButton
        onClick={(event) => {
          event.stopPropagation();
          setConfirmDialog(true);
        }}
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
        {server ? "Chỉnh sửa Server" : "Tạo mới Server"}
      </DialogTitle>
      <DialogContent>
        <Grid container spacing={2}>
          <Grid item xs={12}>
            <TextFieldFormV2
              label="Tên server"
              required
              placeholder="Nhập tên ..."
              name="name"
              onChange={(event: any) => {
                const { name, value } = event.target;

                handleChange(name, value);
              }}
              value={formData["name"]}
              textError={formErr.name}
            />
          </Grid>
          <Grid item xs={12}>
            <TextFieldFormV2
              label="Địa chỉ IP"
              required
              placeholder="--"
              onChange={(event: any) => {
                const { name, value } = event.target;

                handleChange(name, value);
              }}
              name="ip_address"
              value={formData["ip_address"]}
              textError={formErr.ip_address}
            />
          </Grid>
        </Grid>
      </DialogContent>
      <DialogActions sx={{ justifyContent: "center", gap: "16px" }}>
        <button
          onClick={(event) => {
            event.stopPropagation();
            setConfirmDialog(true);
          }}
          className="min-w-[100px] shadow-shadown1 bg-white rounded-lg px-[14px] py-2 capitalize text-grayOz font-semibold text-sm hover:bg-white hover:shadow-shadown1"
        >
          Hủy bỏ
        </button>
        <button
          onClick={(event) => {
            event.stopPropagation();
            handleSubmit();
          }}
          className="min-w-[100px] shadow-shadown1 bg-primary rounded-lg px-[14px] py-2 capitalize text-white font-semibold text-sm hover:bg-primaryDark"
        >
          {server ? "Xác nhận" : "Tạo mới"}
        </button>
      </DialogActions>
    </Dialog>
  );
}
