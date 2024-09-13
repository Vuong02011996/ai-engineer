import { processApi } from "@/api-client/process";
import { EmptyData, Loading, PainComponents } from "@/components/common";
import { LoadingPopup } from "@/components/common/loading/loading-popup";
import {
  CancelBtn,
  FieldNumber,
  PrettoSlider,
  SubmitBtn,
  Transition,
} from "@/components/ui";
import { ResultEnum } from "@/constants/enum";
import { CameraCrowd } from "@/interfaces/identification-profile/crowd";
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

export interface IConfigAICrowdDialogProps {
  open: boolean;
  handleClose: () => void;
  submit: (data: any) => Promise<ResultEnum>;
  data: CameraCrowd;
}

const formInit = {
  boundary: "",
  min_human_count: "", // Số người được phép tụ tập
  min_neighbours: "", // Độ nhạy
  distance_threshold: 85, //Số người được phép trong nhóm
  waiting_time_to_start_alarm: "", //Thời gian bật cảnh báo (giây)
  waiting_time_for_next_alarm: "", //Khoảng cách cảnh báo (giây)
  image_url: "",
};

export function ConfigAICrowdDialog(props: IConfigAICrowdDialogProps) {
  // ************** --init state-- *****************
  const { open, handleClose, submit, data } = props;
  const [formErr, setFormErr] = useState<any>({});
  const [form, setForm] = useState<any>(formInit);
  const [confirmDialog, setConfirmDialog] = useState(false);
  const [loading, setLoading] = useState(false);
  const [image, setimage] = useState<any>("");
  const [loadingImg, setLoadingImg] = useState(true);

  // * * * * * * * * HANDLE INPUT CHANGE * * * * * * * * *
  const handleInputChange = (key: string, value: any) => {
    setForm({ ...form, [key]: value });
    setFormErr({ ...formErr, [key]: null });
  };

  // * * * * * * * * ON CLOSE * * * * * * * * *
  const onClose = () => {
    handleClose();
    setFormErr({});
    setimage("");
    setForm(formInit);
  };

  // * * * * * * * * VALIDATE FUNCTION * * * * * * * * *
  const checkValidate = (form: any) => {
    let hasError = false;

    let error = {
      ...formErr,
      min_human_count: Validator.checkContainsOnlyNumbers(
        form["min_human_count"] ?? ""
      ),
      min_neighbours: Validator.checkContainsOnlyNumbers(
        form["min_neighbours"] ?? ""
      ),
      distance_threshold: Validator.checkContainsOnlyNumbers(
        form["distance_threshold"] ?? ""
      ),
      waiting_time_to_start_alarm: Validator.checkContainsOnlyNumbers(
        form["waiting_time_to_start_alarm"] ?? ""
      ),
      waiting_time_for_next_alarm: Validator.checkContainsOnlyNumbers(
        form["waiting_time_for_next_alarm"] ?? ""
      ),
      boundary: Validator.checkBoundary(form["boundary"] ?? ""),
    };

    if (
      error.min_human_count !== null ||
      error.min_neighbours !== null ||
      error.distance_threshold !== null ||
      error.waiting_time_to_start_alarm !== null ||
      error.boundary !== null ||
      error.waiting_time_for_next_alarm !== null
    ) {
      hasError = true;
    }
    if (error.boundary) {
      enqueueSnackbar(error.boundary, { variant: "error" });
    }

    setFormErr(error);

    return !hasError;
  };

  // * * * * * * * * GET IMAGE * * * * * * * * *
  // const getImage = async (id: string) => {
  //   if (!id) return;
  //   setimage("");
  //   setLoadingImg(true);
  //   try {
  //     let { data } = await crowdApi.getImageByIdCamera(id);
  //     setimage(data);
  //     setForm({ ...form, image_url: data });
  //   } catch (error) {
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

  // * * * * * * * * USE EFFECT INT FORM * * * * * * * * *
  useEffect(() => {
    if (!open) return;
    if (props?.data?.crowdData) {
      setLoadingImg(false);
      const crowdData = props?.data?.crowdData;

      setimage(crowdData.image_url);
      setForm({
        boundary: crowdData.boundary,
        min_human_count: crowdData.min_human_count,
        min_neighbours: crowdData.min_neighbours,
        distance_threshold: crowdData.distance_threshold,
        waiting_time_to_start_alarm: crowdData.waiting_time_to_start_alarm,
        waiting_time_for_next_alarm: crowdData.waiting_time_for_next_alarm,
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
        Cấu hình AI phát hiện đám đông
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
                  points={data.crowdData?.boundary}
                  onReloadImage={() => {
                    getImage(props.data?.process_id);
                  }}
                  onSubmit={(boundary: any) => {
                    setForm({ ...form, boundary: boundary });
                  }}
                />
              )}
            </Grid>
            <Grid item xs={5}>
              <Stack spacing={2}>
                {/* Số người được phép tụ tập */}
                <FieldNumber
                  text={"Số người được phép tụ tập"}
                  value={form["min_human_count"]}
                  onChange={function (e: any): void {
                    const key = "min_human_count";
                    handleInputChange(key, e.target.value);
                  }}
                  textError={formErr["min_human_count"]}
                />

                {/* Số người được phép trong nhóm*/}
                <FieldNumber
                  text={"Số người được phép trong nhóm"}
                  value={form["min_neighbours"]}
                  onChange={function (e: any): void {
                    const key = "min_neighbours";
                    handleInputChange(key, e.target.value);
                  }}
                  textError={formErr["min_neighbours"]}
                />

                {/* Thời gian bật cảnh báo (giây) */}
                <FieldNumber
                  text={"Thời gian bật cảnh báo (giây)"}
                  value={form["waiting_time_to_start_alarm"]}
                  onChange={function (e: any): void {
                    const key = "waiting_time_to_start_alarm";
                    handleInputChange(key, e.target.value);
                  }}
                  textError={formErr["waiting_time_to_start_alarm"]}
                />

                {/* Khoảng cách cảnh báo (giây) */}
                <FieldNumber
                  text={"Khoảng cách cảnh báo (giây)"}
                  value={form["waiting_time_for_next_alarm"]}
                  onChange={function (e: any): void {
                    const key = "waiting_time_for_next_alarm";
                    handleInputChange(key, e.target.value);
                  }}
                  textError={formErr["waiting_time_for_next_alarm"]}
                />

                {/* Độ nhạy */}
                {_renderSlider({
                  text: "Độ nhạy",
                  value: form["distance_threshold"],
                  onChange: (e: any) => {
                    const key = "distance_threshold";
                    handleInputChange(key, e.target.value);
                  },
                })}
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

function _renderSlider({
  text,
  value,
  onChange,
}: {
  text: string;
  value: number;
  onChange?: (e: any) => void;
}) {
  return (
    <div className="flex flex-row items-center   ">
      <p className="flex-1 w-[70px] text-[#808080] font-normal text-[14px] ">
        {text}
      </p>
      <PrettoSlider
        value={value}
        onChange={onChange}
        aria-label="Default"
        valueLabelDisplay="auto"
        sx={{ width: "200px", height: "24px" }}
      />
    </div>
  );
}
