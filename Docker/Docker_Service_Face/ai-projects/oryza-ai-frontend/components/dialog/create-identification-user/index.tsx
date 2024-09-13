import { LoadingPopup } from "@/components/common/loading/loading-popup";
import TextFieldFormV2 from "@/components/common/text-field/text-field-form-v2";
import { ChooseGender } from "@/components/input-field/choose-gender";
import { ChooseImage } from "@/components/input-field/choose-image";
import { FileInterface } from "@/components/input-field/choose-image/interface";
import { CancelBtn, SubmitBtn, Transition } from "@/components/ui";
import { ResultEnum } from "@/constants/enum";
import { IPerson } from "@/interfaces/identification-profile/person";
import { Validator } from "@/utils/validate";
import CloseRoundedIcon from "@mui/icons-material/CloseRounded";
import { Grid, IconButton } from "@mui/material";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogTitle from "@mui/material/DialogTitle";
import * as React from "react";
import { useState } from "react";
import { ConfirmCloseDialog } from "../confirm-dialog/confirm-close-dialog";
import { CreateMultipleCamera } from "./create-multiple-camera";
import { useRouter } from "next/router";

export interface IIdentificationUserDialogProps {
  open: boolean;
  handleClose: () => void;
  submit: (data: any) => Promise<ResultEnum | string>;
  data?: IPerson;
  defaultImage?: string[];
}

export function IdentificationUserDialog(
  props: IIdentificationUserDialogProps
) {
  // ************** --init state-- *****************
  const { open, handleClose, submit } = props;
  const [formErr, setFormErr] = useState<any>({});
  const [confirmDialog, setConfirmDialog] = useState(false);
  const [loading, setLoading] = useState(false);
  const [files, setFiles] = useState<FileInterface[]>([]);
  const [openCreateALl, setOpenCreateALl] = useState(false);
  const [presonId, setPresonId] = useState("");
  const router = useRouter();

  // * * * * * * * * VALIDATE FUNCTION * * * * * * * * *
  const checkValidate = (formData: any) => {
    let hasError = false;

    const name = Validator.checkNotEmpty(formData["name"] ?? "");

    const hasFile = files.some(
      (item: FileInterface) => item.file instanceof File
    );
    const hasNoNulls = files.every((item: FileInterface) => item.file !== null);

    let fileError: string | null = null;

    if (!hasNoNulls) {
      fileError = "Hình không hợp lệ";
    } else if (!hasFile) {
      fileError = "Chọn ít nhất 1 hình";
    } else {
      fileError = null;
    }

    let error = {
      ...formErr,
      name: name,
      fileError: props.data ? null : fileError,
    };

    if (error.name !== null || error.fileError !== null) {
      hasError = true;
    }

    setFormErr(error);

    return !hasError;
  };

  // * * * * * * * * SUBMIT FUNCTION * * * * * * * * *
  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    let formData = new FormData(event.currentTarget);

    if (!props.data) {
      for (let i = 0; i < files.length; i++) {
        if (files[i].file !== null) {
          formData.append("files", files[i].file as File);
        }
      }
    }

    const formJson = Object.fromEntries(formData.entries());

    let other_info = {
      gender: formJson.gender,
      address: formJson.address,
    };

    formData.append("other_info", JSON.stringify(other_info));
    formData.delete("gender");
    formData.delete("address");

    if (!checkValidate(formJson)) return;

    setLoading(true);
    let result = await submit(formData);

    setLoading(false);
    if (result !== ResultEnum.success && result !== ResultEnum.error) {
      setOpenCreateALl(true);
      setPresonId(result);
    }
    if (result === ResultEnum.success) onClose();
  };

  // * * * * * * * * ON CLOSE * * * * * * * * *
  const onClose = () => {
    setFormErr({});
    setFiles([]);
    handleClose();
  };

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
        onSubmit: handleSubmit,
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

      {presonId !== "" && (
        <CreateMultipleCamera
          open={openCreateALl}
          handleClose={() => {
            setOpenCreateALl(false);
            onClose();
            router.reload();
          }}
          presonId={presonId}
        />
      )}

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
        {props.data ? "Chỉnh sửa đối tượng" : "Tạo mới đối tượng"}
      </DialogTitle>
      <DialogContent>
        <Grid container spacing={2}>
          <Grid item xs={12}>
            <TextFieldFormV2
              label="Tên đối tượng"
              required
              placeholder="Nhập tên..."
              name="name"
              defaultValue={props.data?.name ?? ""}
              textError={formErr?.name ?? ""}
            />
          </Grid>
          <Grid item xs={6}>
            <ChooseGender
              label="Giới tính"
              name="gender"
              defaultValue={props.data?.other_info?.gender ?? ""}
            />
          </Grid>
          <Grid item xs={6}>
            <TextFieldFormV2
              label="Địa chỉ"
              placeholder="--"
              name="address"
              defaultValue={props.data?.other_info?.address ?? ""}
            />
          </Grid>
          <Grid item xs={12}>
            <ChooseImage
              name={""}
              label={""}
              files={files}
              setFiles={setFiles}
              data={props.data}
              textError={formErr.fileError}
              defaultImage={props.defaultImage}
            />
          </Grid>
        </Grid>
      </DialogContent>
      <DialogActions sx={{ justifyContent: "center", gap: "16px" }}>
        <CancelBtn onClick={() => setConfirmDialog(true)} text={"Hủy bỏ"} />
        <SubmitBtn type="submit" text={props.data ? "Xác nhận" : "Tạo mới"} />
      </DialogActions>
    </Dialog>
  );
}
