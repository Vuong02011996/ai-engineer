import { processApi } from "@/api-client/process";
import { EmptyData, Loading } from "@/components/common";
import { DrawLineComponenent } from "@/components/common/paint/draw-line";
import { DrawLaneComponent } from "@/components/common/paint/draw-lane";
import { DrawLaneWithConfig } from "@/components/common/paint/draw-lane-w-config";
import { LoadingPopup } from "@/components/common/loading/loading-popup";
import { CancelBtn, SubmitBtn, Transition } from "@/components/ui";
import { ResultEnum } from "@/constants/enum";
import { CameraLaneViolation } from "@/interfaces/identification-profile/lane-violation";
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
import { TypeServiceKey } from "@/constants/type-service";

export interface IConfigAILaneViolationDialogProps {
  open: boolean;
  handleClose: () => void;
  submit: (data: any) => Promise<ResultEnum>;
  data: CameraLaneViolation;
  keyAI?: string;
}

const formInit = {
  lanes: "",
  codes: "",
  image_url: "",
};

export function ConfigAILaneViolationDialog(props: IConfigAILaneViolationDialogProps) {
  // ************** --init state-- *****************
  const { open, handleClose, submit, data } = props;
  const [formErr, setFormErr] = useState<any>({});
  const [form, setForm] = useState<any>(formInit);
  const [confirmDialog, setConfirmDialog] = useState(false);
  const [image, setimage] = useState<any>("");
  const [loadingImg, setLoadingImg] = useState(true);
  const [loading, setLoading] = useState(false);

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
    console.log('Validate form', form);
    let error = {
      ...formErr,
      lanes: (
        (props.keyAI === TypeServiceKey.lane_violation
        || props.keyAI === TypeServiceKey.wrong_way
        ) 
        ? Validator.checkLanes(form["lanes"] ?? "")
        : (props.keyAI === TypeServiceKey.line_violation)
        ? Validator.checkLines(form["lanes"] ?? "")
        : null
      ),
      codes: (
        props.keyAI === TypeServiceKey.lane_violation
      )
      ? Validator.checkCodes(form["codes"], form["lanes"])
      : null
    };

    if (error.lanes !== null) {
      hasError = true;
      console.log('Validate lanes has error:', hasError);
    }
    if (error.lanes) {
      enqueueSnackbar(error.lanes, { variant: "error" });
    }
    if (error.codes !== null) {
      hasError = true;
      console.log('Validate codes has error:', hasError);
    }
    if (error.codes) {
      enqueueSnackbar(error.codes, { variant: "error" });
    }

    setFormErr(error);
    console.log('Validate has error:', error);
    return !hasError;
  };

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

  const getDrawWindow = () => {
    switch (props.keyAI) {
      case TypeServiceKey.lane_violation:
        return <DrawLaneWithConfig
          image={image}
          lanes_str={data.setting?.lanes}
          codes_str={data.setting?.codes}
          onReloadImage={() => {
            getImage(props.data?.process_id);
          }}
          onSubmit={(lanes: string, codes: string) => {
            console.log('Got from lane violation box')
            console.log('Lanes', lanes);
            console.log('Codes', codes);
            setForm({ ...form, lanes: lanes, codes: codes });
          }}
        />
      case TypeServiceKey.wrong_way:
        return <DrawLaneComponent
          image={image}
          lanes={data.setting?.lanes}
          onReloadImage={() => {
            getImage(props.data?.process_id);
          }}
          onSubmit={(lanes: any) => {
            setForm({ ...form, lanes: lanes });
          }}
        />
      case TypeServiceKey.line_violation:
        return <DrawLineComponenent
          image={image}
          lines={data.setting?.lanes}
          onReloadImage={() => {
            getImage(props.data?.process_id);
          }}
          onSubmit={(lines: any) => {
            setForm({ ...form, lanes: lines });
          }}
          // lane here is actually line, we use the same api for both
        />
      default:
        return <EmptyData />
    }
  }

  const getTitle = () => {
    switch (props.keyAI) {
      case TypeServiceKey.lane_violation:
        return "Cấu hình AI phát hiện vi phạm lấn làn";
      case TypeServiceKey.line_violation:
        return "Cấu hình AI phát hiện vi phạm lấn vạch";
      case TypeServiceKey.wrong_way:
        return "Cấu hình AI phát hiện vi phạm đi ngược chiều";
      default:
        return "Cấu hình AI";
    }
  }

  // * * * * * * * USE EFFECT INIT FORM * * * * * * * * *
  useEffect(() => {
    if (!open) return;
    console.log('data', props.data);
    if (props?.data?.setting) {
      setLoadingImg(false);
      const laneViolationData = props?.data?.setting;

      setimage(laneViolationData.image_url);
      setForm({
        lanes: laneViolationData.lanes,
        image_url: laneViolationData.image_url,
        codes: laneViolationData.codes,
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
          width: "1000px", // Fixed width
          height: "700px", // Fixed height
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

      <DialogTitle className="text-start text-[#1C2A53] text-xl font-medium p-3 ">
        {getTitle()}
      </DialogTitle>
      <DialogContent
        sx={{
          padding: "0px 40px",
          height: "100%",
          overflow: "hidden",
        }}
      >
      <Stack
        sx={{
          minHeight: 400, // Adjusted to be smaller
          maxHeight: 800, // Added maxHeight for better control
          overflow: 'auto', // Added overflow to handle content overflow
        }}
      >
        {props.keyAI === TypeServiceKey.lane_violation ? (
          <Grid item xs={12}>
            {loadingImg ? (
              <Loading />
            ) : !image ? (
              <EmptyData />
            ) : (
              <DrawLaneWithConfig
                image={image}
                lanes_str={data.setting?.lanes}
                codes_str={data.setting?.codes}
                onReloadImage={() => {
                  getImage(props.data?.process_id);
                }}
                onSubmit={(lanes: string, codes: string) => {
                  console.log('Got from lane violation box')
                  console.log('Lanes', lanes);
                  console.log('Codes', codes);
                  setForm({ ...form, lanes: lanes, codes: codes });
                }}
              />
            )}
          </Grid>
        ) : (
          <Grid container columnSpacing={10}>
            <Grid item xs={12}>
              {loadingImg ? (
                <Loading />
              ) : !image ? (
                <EmptyData />
              ) : (
                getDrawWindow()
              )}
            </Grid>
          </Grid>
        )}
      </Stack>
      </DialogContent>
      <DialogActions sx={{ justifyContent: "end", gap: "16px"}}>
        <CancelBtn text={"Hủy bỏ"} onClick={() => setConfirmDialog(true)} />
        <SubmitBtn
          disabled={image === ""}
          text={"Cập nhật"}
          onClick={async (e) => {
            e.preventDefault(); // Prevent the default behavior

            if (!checkValidate(form)) {
              console.log("Form validation failed:", form); // Log the form value
              return;
            }
            setLoading(true);
            const result = await submit(form);
            console.log("result", form);
            setLoading(false);
            if (result === ResultEnum.success) onClose();
          }}
        />
      </DialogActions>
    </Dialog>
  );
}