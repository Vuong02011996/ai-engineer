import { processApi } from "@/api-client/process";
import { EmptyData, Loading} from "@/components/common";
import { DrawLineComponenent } from "@/components/common/paint/draw-line";
import { LoadingPopup } from "@/components/common/loading/loading-popup";
import { CancelBtn, SubmitBtn, Transition } from "@/components/ui";
import { ResultEnum } from "@/constants/enum";
import { CameraTripwire } from "@/interfaces/identification-profile/tripwire";
import { Validator } from "@/utils/validate";
import CloseRoundedIcon from "@mui/icons-material/CloseRounded";
import { IconButton, Stack } from "@mui/material";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogTitle from "@mui/material/DialogTitle";
import { enqueueSnackbar } from "notistack";
import * as React from "react";
import { useEffect, useState } from "react";
import { ConfirmCloseDialog } from "../confirm-dialog/confirm-close-dialog";
import { TypeServiceKey } from "@/constants/type-service";

export interface IConfigAITripwireDialogProps {
  open: boolean;
  handleClose: () => void;
  submit: (data: any) => Promise<ResultEnum>;
  data: CameraTripwire;
}

const formInit = {
  line: "",
  image_url: "",
};

export function ConfigAITripwireDialog(props: IConfigAITripwireDialogProps) {
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
    console.log('line', form);
    let error = {
      ...formErr,
      line: Validator.checkLine(form["line"] ?? ""),
    };

    if (error.line !== null) {
      hasError = true;
    }
    if (error.line) {
      enqueueSnackbar(error.line, { variant: "error" });
    }

    setFormErr(error);

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

  // * * * * * * * USE EFFECT INIT FORM * * * * * * * * *
  useEffect(() => {
    if (!open) return;
    if (props?.data?.setting) {
      setLoadingImg(false);
      const tripwireData = props?.data?.setting;

      setimage(tripwireData.image_url);
      setForm({
        line: tripwireData.line,
        image_url: tripwireData.image_url,
      });
    } else {
      getImage(props.data?.process_id);
    }
    console.log('Setting loaded', props.data);
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
        Cấu hình AI Hàng rào ảo
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
            minHeight: 400,
          }}
        >
          {loadingImg ? (
            <Loading />
          ) : !image ? (
            <EmptyData />
          ) : (
            <DrawLineComponenent
              image={image}
              lines={data.setting?.line}
              onReloadImage={() => {
                getImage(props.data?.process_id);
              }}
              onSubmit={(line: any) => {
                setForm({ ...form, line: line });
              }}
              type={TypeServiceKey.tripwire}
            />
          )}
        </Stack>
      </DialogContent>
      <DialogActions sx={{ justifyContent: "end", gap: "16px" }}>
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
            setLoading(false);
            if (result === ResultEnum.success) onClose();
          }}
        />
      </DialogActions>
    </Dialog>
  );
}
