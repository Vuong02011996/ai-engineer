import { LoadingPopup } from "@/components/common/loading/loading-popup";
import { ChooseServiceType } from "@/components/input-field/choose-service-type";
import { FormControl, FormLabel, RadioGroup, FormControlLabel, Radio, Typography } from '@mui/material';
import { ResultEnum } from "@/constants/enum";
import useFormSubmit from "@/hooks/useFromSubmit";
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
import { useEffect, useState } from "react";
import { ChooseService } from "../../input-field/choose-service";
import { ConfirmCloseDialog } from "../confirm-dialog/confirm-close-dialog";
import { cameraApi } from "@/api-client/camera";
import { enqueueSnackbar } from "notistack";
import { ChooseRtsp } from "../../input-field/choose-rtsp";

const Transition = React.forwardRef(function Transition(
  props: TransitionProps & {
    children: React.ReactElement<any, any>;
  },
  ref: React.Ref<unknown>
) {
  return <Slide direction="up" ref={ref} {...props} />;
});

export interface ICreateProcessDialogProps {
  camera: any;
  open: boolean;
  handleClose: () => void;
  submit: (data: any) => Promise<ResultEnum>;
  data?: any;
}

export function CreateProcessDialog(props: ICreateProcessDialogProps) {
  const { camera, open, handleClose, submit, data } = props;
  const [loading, setLoading] = useState(false);
  const [formErr, setFormErr] = useState<any>({});
  const [formData, setFormData] = useState<any>({
    service_id: "",
    id_type_service: "",
    rtsp_type: "",
    rtsp: "",
  });

  const checkValidate = (formData: any) => {
    let hasError = false;

    const service_id = Validator.checkNotChosen(
      formData["service_id"]?.id ?? ""
    );
    let error = {
      ...formErr,
      service_id: service_id,
    };

    if (formData["service_id"]?.type === "AI_CAMERA") {
      error = {
        ...formErr,
        id_type_service: Validator.checkNotChosen(
          formData["id_type_service"] ?? ""
        ),
        rtsp: null,
      };
    } else if (formData["service_id"]?.type === "AI_SERVICE") {
      error = {
        ...formErr,
        id_type_service: null,
        rtsp: Validator.checkNotChosen(formData["rtsp"] ?? ""),
      };
    }

    if (
      error.service_id !== null 
      || error.id_type_service !== null
      || error.rtsp !== null
    ) {
      hasError = true;
    }

    setFormErr(error);

    return !hasError;
  };

  const onClickSubmit = async () => {
    if (!checkValidate(formData)) return;
    setLoading(true);
    const payload = {
      ...formData,
      service_id: formData["service_id"]?.id,
    };
    let result = await submit(payload);
    setLoading(false);
    if (result === ResultEnum.success) handleClose();
  };

  const onClose = () => {
    handleClose();
    setFormErr({});
    setFormData({
      service_id: "",
      id_type_service: "",
      rtsp_type: "",
      rtsp: "",
    });
  };
  const [confirmDialog, setConfirmDialog] = useState(false);

  useEffect(() => {
    if (!open) {
      setFormData({
        service_id: "",
        id_type_service: "",
        rtsp_type: "",
        rtsp: "",
      });
    }
  }, [open]);
  
  return (
    <Dialog

      open={open}
      TransitionComponent={Transition}
      onClose={() => setConfirmDialog(true)}
      aria-describedby="alert-dialog-slide-description"
      // fullWidth={true}
      // maxWidth="md"
      PaperProps={{
        sx: {
          borderRadius: "11px",
          boxShadow: "0px 1px 10px 0px rgba(34, 34, 34, 0.10)",
          padding: "16px",
          position: "relative",
          width: "1500px",
        },
        component: "form",
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
        {data ? "Chỉnh sửa AI cho camera" : "Thêm AI cho camera"}
      </DialogTitle>
      <DialogContent>
        <Grid container spacing={2}>
          <Grid item xs={12}>
            <ChooseService
              name={"service_id"}
              label={"Chọn service"}
              value={formData["service_id"]?.id}
              onChange={(value) => {
                if (value.type === "AI_CAMERA") {
                  setFormData({ ...formData, ["service_id"]: value });
                  setFormErr({ ...formErr, ["service_id"]: null });
                } else {
                  setFormData({
                    ...formData,
                    ["service_id"]: value,
                    ["id_type_service"]: null,
                  });
                  setFormErr({ ...formErr, ["service_id"]: null });
                }
              }}
              textError={formErr?.service_id ?? ""}
            />
          </Grid>
          {formData["service_id"]?.type === "AI_SERVICE" && (
            <Grid item xs={12}>
              <ChooseRtsp
                label="Chọn RTSP"
                camera={camera}
                name="rtsp"
                value={formData['rtsp']}
                onChange={(value) => {
                  setFormData({ ...formData, ["rtsp"]: value });
                  setFormErr({ ...formErr, ["service_id"]: null });
                }}
                textError={formErr?.rtsp ?? ""}
              />
            </Grid>
          )}
          {formData["service_id"]?.type === "AI_CAMERA" && (
            <Grid item xs={12}>
              <ChooseServiceType
                defaultValue={data?.type_service}
                name="id_type_service"
                value={formData["id_type_service"]}
                onChange={(value) => {
                  setFormData({ ...formData, ["id_type_service"]: value });
                  setFormErr({ ...formErr, ["id_type_service"]: null });
                }}
              />
            </Grid>
          )}
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
          type="button"
          onClick={onClickSubmit}
          className="min-w-[100px] shadow-shadown1 bg-primary rounded-lg px-[14px] py-2 capitalize text-white font-semibold text-sm hover:bg-primaryDark"
        >
          {data ? "Xác nhận" : "Tạo mới"}
        </button>
      </DialogActions>
    </Dialog>
  );
}