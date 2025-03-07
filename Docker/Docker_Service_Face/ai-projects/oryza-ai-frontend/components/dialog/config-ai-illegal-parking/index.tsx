import { processApi } from "@/api-client/process";
import { EmptyData, Loading, PainComponents } from "@/components/common";
import { LoadingPopup } from "@/components/common/loading/loading-popup";
import { CancelBtn, FieldNumber, SubmitBtn, Transition } from "@/components/ui";
import { ResultEnum } from "@/constants/enum";
import { CameraIllegalParking } from "@/interfaces/identification-profile/illegal-parking";
import { Validator } from "@/utils/validate";
import CloseRoundedIcon from "@mui/icons-material/CloseRounded";
import { Grid, IconButton, Stack } from "@mui/material";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogTitle from "@mui/material/DialogTitle";
import { enqueueSnackbar } from "notistack";
import * as React from "react";
import { useEffect, useState } from "react";
import { ConfirmCloseDialog } from "../confirm-dialog/confirm-close-dialog";

export interface IConfigAIIllegalParkingDialogProps {
  open: boolean;
  handleClose: () => void;
  submit: (data: any) => Promise<ResultEnum>;
  data: CameraIllegalParking;
}

const formInit = {
  boundary: "",
  waiting_time: undefined,
  alert_interval: undefined,
  image_url: "",
};

export function ConfigAIIllegalParkingDialog(props: IConfigAIIllegalParkingDialogProps) {
  // ************** --init state-- *****************
  const { open, handleClose, submit, data } = props;
  const [formErr, setFormErr] = useState<any>({});
  const [form, setForm] = useState<any>(formInit);
  const [confirmDialog, setConfirmDialog] = useState(false);
  const [image, setimage] = useState<any>("");
  const [loadingImg, setLoadingImg] = useState(true);
  const [loading, setLoading] = useState(false);

  // * * * * * * * * HANDLE INPUT CHANGE * * * * * * * * *
  const handleInputChange = (key: string, value: any) => {
    setForm({ ...form, [key]: value });
    setFormErr({ ...formErr, [key]: null });
  };

  // * * * * * * * ON CLOSE * * * * * * * * *
  const onClose = () => {
    handleClose();
    setFormErr({});
    setimage("");
    setForm(formInit);
  };

  // * * * * * * * VALIDATE FUNCTION * * * * * * * * *
  const checkValidate = (form: any) => {
    let hasError = false;

    let error = {
      ...formErr,
      waiting_time: Validator.checkContainsOnlyNumbers(
        form["waiting_time"] ?? ""
      ),
      alert_interval: Validator.checkContainsOnlyNumbers(
        form["alert_interval"] ?? ""
      ),
      boundary: Validator.checkBoundary(form["boundary"] ?? ""),
    };

    if (error.boundary !== null || error.waiting_time !== null || error.alert_interval !== null) {
      hasError = true;
    }
    if (error.boundary) {
      enqueueSnackbar(error.boundary, { variant: "error" });
    }

    setFormErr(error);

    return !hasError;
  };

  // * * * * * * * GET IMAGE * * * * * * * * *
  // const getImage = async (id: string) => {
  //   if (!id) return;
  //   setimage("");
  //   setLoadingImg(true);
  //   try {
  //     let { data } = await IllegalParkingApi.getImageByIdCamera(id);
  //     setimage(data);
  //     setForm({ ...form, image_url: data });
  //   } catch (error) {
  //     enqueueSnackbar("Không tải được hình ảnh", {
  //       variant: "error",
  //     });
  //   } finally {
  //     setLoadingImg(false);
  //   }
  // };
  const getImage = async (process_id: any) => {
    if (!process_id) return;
    setimage("");
    setLoadingImg(true);
    try {
      let { data } = await processApi.getPreviewImage(process_id);
      setimage(data);
      setForm({ ...form, image_url: data });
    } catch (error) {
      enqueueSnackbar("Không tải được hình ảnh", {
        variant: "error",
      });
    } finally {
      setLoadingImg(false);
    }
  }

  // * * * * * * * USE EFFECT INIT FORM * * * * * * * * *
  useEffect(() => {
    if (!open) return;
    if (props?.data?.setting) {
      setLoadingImg(false);
      const crowdData = props?.data?.setting;

      setimage(crowdData.image_url);
      setForm({
        boundary: crowdData.boundary,
        waiting_time: crowdData.waiting_time,
        alert_interval: crowdData.alert_interval,
        image_url: crowdData.image_url,
      });
    } else {
      getImage(props.data?.process_id);
    }

    return () => {};
  }, [props.data, open]);

  return (
    <Dialog
      open={open}
      TransitionComponent={Transition}
      onClose={() => setConfirmDialog(true)}
      aria-describedby="alert-dialog-slide-description"
      fullWidth
      maxWidth="lg"
      PaperProps={{
        sx: {
          borderRadius: "11px",
          boxShadow: "0px 1px 10px 0px rgba(34, 34, 34, 0.10)",
          padding: "16px",
          position: "relative",
        },
        component: "form",
      }}
    >
      <LoadingPopup open={loading} />

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
        className="w-[32px] h-[32px] flex top-[16px] right-[16px]"
        sx={{
          position: "absolute",
        }}
      >
        <CloseRoundedIcon fontSize="inherit" sx={{ fontSize: 24 }} />
      </IconButton>

      <DialogTitle className="text-start text-[#1C2A53] text-xl font-medium p-0 ">
        Cấu hình AI phát hiện đậu đỗ trái phép
      </DialogTitle>
      <DialogContent
        sx={{
          marginTop: "20px",
          padding: "0px 40px",
          height: "100%",
          overflow: "hidden",
        }}
      >
        <Stack
          sx={{
            minHeight: 400,
          }}
        >
          <Grid container columnSpacing={10}>
            <Grid item xs={7}>
              {loadingImg ? (
                <Loading />
              ) : !image ? (
                <EmptyData />
              ) : (
                <PainComponents
                  image={image}
                  points={data.setting?.boundary}
                  onReloadImage={() => {
                    getImage(props.data?.id);
                  }}
                  onSubmit={(boundary: any) => {
                    setForm({ ...form, boundary: boundary });
                  }}
                />
              )}
            </Grid>
            <Grid item xs={5}>
              <div style={{ marginBottom: '10px' }}>
                <Stack spacing={2}>
                  {/* waiting_time */}
                  <FieldNumber
                    text={"Thời gian chờ"}
                    value={form["waiting_time"]}
                    onChange={(e: any): void => {
                      const key = "waiting_time";
                      handleInputChange(key, e.target.value);
                    }}
                    textError={formErr["waiting_time"]}
                  />
                </Stack>
              </div>
              <Stack spacing={2}>
                {/* alert interval */}
                <FieldNumber
                  text={"Thời gian cảnh báo"}
                  value={form["alert_interval"]}
                  onChange={function (e: any): void {
                    const key = "alert_interval";
                    handleInputChange(key, e.target.value);
                  }}
                  textError={formErr["alert_interval"]}
                />
              </Stack>
            </Grid>
          </Grid>
        </Stack>
      </DialogContent>
      <DialogActions sx={{ justifyContent: "end", gap: "16px" }}>
        <CancelBtn text={"Hủy bỏ"} onClick={() => setConfirmDialog(true)} />
        <SubmitBtn
          disabled={image === ""}
          text={"Cập nhật"}
          onClick={async (e) => {
            e.preventDefault();
            if (!checkValidate(form)) return;
            setLoading(true);
            const result = await submit(form);
            setLoading(false);
            if (result === ResultEnum.success) onClose();
          }}
        />
      </DialogActions>
    </Dialog>
  );
}
