import { LoadingPopup } from "@/components/common/loading/loading-popup";
import { CancelBtn, SubmitBtn, Transition } from "@/components/ui";
import { ResultEnum } from "@/constants/enum";
import CloseRoundedIcon from "@mui/icons-material/CloseRounded";
import { IconButton } from "@mui/material";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogTitle from "@mui/material/DialogTitle";
import { useEffect, useState } from "react";
import { ConfirmCloseDialog } from "../confirm-dialog/confirm-close-dialog";

import { ColorPicker } from "./color";
import { ChooseImageUniform } from "./choose-image";

export interface ISettingCompanyUniformDialogProps {
  open: boolean;
  handleClose: () => void;
  submit: (data: any) => Promise<ResultEnum>;
  data: any;
}

const formInit = {
  rgb: "[255,255,255]",
  files: [],
};

export function SettingCompanyUniformDialog(
  props: ISettingCompanyUniformDialogProps
) {
  // ************** --init state-- *****************
  const { open, handleClose, submit, data } = props;
  const [loading, setLoading] = useState(false);
  const [files, setFiles] = useState<any[]>([]);
  const [formErr, setFormErr] = useState<any>({});
  const [form, setForm] = useState<any>(formInit);

  //* on close
  const onClose = () => {
    handleClose();
    setFormErr({});
    setForm(formInit);
  };

  const [confirmDialog, setConfirmDialog] = useState(false);

  useEffect(() => {
    if (!open) return;
    if (props.data) {
      console.log(props.data);
      setForm({
        rgb: props.data.rgb,
      });

      setFiles(props.data.images);
    }

    return () => {};
  }, [props.data, open]);

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

      <DialogTitle className="text-start text-[#1C2A53] text-xl font-medium p-0 pl-[15px]">
        {props.data ? "Chỉnh sửa nhận diện" : "Tạo mới nhận diện"}
      </DialogTitle>
      <DialogContent
        sx={{
          padding: "0 15px",
          mt: "15px",
          overflow: "hidden",
          display: "flex",
          flexDirection: "column",
          gap: "10px",
        }}
      >
        <ColorPicker
          color={form["rgb"]}
          onChange={(newColor) => {
            setForm({ ...form, rgb: newColor });
          }}
        />
        <ChooseImageUniform
          setFiles={setFiles}
          files={files}
          data={props.data}
        />
      </DialogContent>
      <DialogActions sx={{ justifyContent: "center" }}>
        <CancelBtn text={"Hủy bỏ"} onClick={() => setConfirmDialog(true)} />
        <SubmitBtn
          text={props.data ? "Cập nhật" : "Tạo mới"}
          onClick={async (e) => {
            const formData: any = new FormData();
            for (const key in files) {
              if (files[key] !== null) formData.append("files", files[key]);
            }
            formData.append("rgb", form["rgb"]);

            setLoading(true);
            const result = await submit(formData);
            setLoading(false);
            if (result === ResultEnum.success) onClose();
          }}
        />
      </DialogActions>
    </Dialog>
  );
}
