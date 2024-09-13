import { LoadingPopup } from "@/components/common/loading/loading-popup";
import TextFieldFormV2 from "@/components/common/text-field/text-field-form-v2";
import { CancelBtn, SubmitBtn } from "@/components/ui";
import { ResultEnum } from "@/constants/enum";
import useFormSubmit from "@/hooks/useFromSubmit";
import { CameraLoiteringDetection } from "@/interfaces/identification-profile/loitering-detection";
import { Validator } from "@/utils";
import {
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
} from "@mui/material";
import * as React from "react";
import { useEffect, useState } from "react";
import { ConfirmCloseDialog } from "../confirm-dialog/confirm-close-dialog";

export interface IConfigAITamperingDialogProps {
  open: boolean;
  handleClose: () => void;
  submit: (data: any) => Promise<ResultEnum>;
  data: CameraLoiteringDetection;
}
export function ConfigAITamperingDialog(props: IConfigAITamperingDialogProps) {
  const { open, handleClose, submit, data } = props;

  const [formErr, setFormErr] = useState<any>({});
  const [alarmInterval, setAlarmInterval] = useState(
    data?.setting?.alarm_interval
  );

  useEffect(() => {
    if (data?.setting?.alarm_interval) {
      setAlarmInterval(data?.setting?.alarm_interval);
    }
  }, [data?.setting?.alarm_interval]);

  const onClose = () => {
    handleClose();
    setFormErr({});
  };

  const checkValidate = (formData: any) => {
    let hasError = false;

    const alarm_interval = Validator.checkNumberString(
      formData["alarm_interval"] ?? ""
    );

    let error = {
      ...formErr,
      alarm_interval: alarm_interval,
    };

    if (error.alarm_interval !== null) {
      hasError = true;
    }

    setFormErr(error);

    return !hasError;
  };

  const [confirmDialog, setConfirmDialog] = useState(false);
  const { loading, handleSubmit } = useFormSubmit(submit, checkValidate);

  return (
    <Dialog
      open={open}
      onClose={handleClose}
      fullWidth
      maxWidth="xs"
      PaperProps={{
        component: "form",
        onSubmit: async (event: React.FormEvent<HTMLFormElement>) => {
          const result = await handleSubmit(event);
          if (result === ResultEnum.success) handleClose();
        },
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

      <DialogTitle>Cấu hình AI phát hiện phá hoại</DialogTitle>
      <DialogContent>
        <TextFieldFormV2
          label="Khoảng thời gian báo động"
          required
          name="alarm_interval"
          type="number"
          fullWidth
          autofocus
          value={alarmInterval}
          textError={formErr?.alarm_interval}
          placeholder="Nhập khoảng thời gian báo động"
          onChange={(e) => {
            setAlarmInterval(e.target.value);
            setFormErr({});
          }}
        />
      </DialogContent>
      <DialogActions>
        <CancelBtn text={"Hủy bỏ"} onClick={onClose} />
        <SubmitBtn
          text={data?.setting ? "Cập nhật" : "Tạo mới"}
          type="submit"
        />
      </DialogActions>
    </Dialog>
  );
}
