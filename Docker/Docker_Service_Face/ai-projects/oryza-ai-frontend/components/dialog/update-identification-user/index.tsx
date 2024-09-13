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
import { ConfirmCloseDialog } from "../confirm-dialog/confirm-close-dialog";
// import { CreateMultipleCamera } from "./create-multiple-camera";
import { useRouter } from "next/router";
import { ChooseIdentificationUser } from "@/components/input-field/choose-identification-user";
import { useEffect, useState } from "react";
import { enqueueSnackbar } from "notistack";
import { personApi } from "@/api-client/identification-profile/person";
import useHandleError from "@/hooks/useHandleError";


export interface IIdentificationUserDialogProps {
  open: boolean;
  handleClose: () => void;
  data?: IPerson;
  defaultImage?: string[];
}

const formInit = {
    id_company: "",
    data_search: ""
};


export function IdentificationUserUpdateDialog(
  props: IIdentificationUserDialogProps
) {
  // ************** --init state-- *****************
  const handleError = useHandleError();
  const { open, handleClose} = props;
  const [formErr, setFormErr] = useState<any>({});
  const [confirmDialog, setConfirmDialog] = useState(false);
  const [loading, setLoading] = useState(false);
  const [files, setFiles] = useState<FileInterface[]>([]);
//   const [openCreateALl, setOpenCreateALl] = useState(false);
  const [presonId, setPresonId] = useState("");
  const router = useRouter();
  const [formData, setFormData] = useState<any>(formInit);
  const [personId, setPersonId] = useState<string | undefined>(undefined);
  
  const handlePersonChange = (id: string | undefined) => {
    setPersonId(id);
    console.log('Selected person ID:', id);
  };

  // const getForm = React.useCallback(async () => {
  //   if (data) {
  //       let response: IPerson[] = [data];
  //       let form = {
  //           ...response[0]
  //       };
  //       setFormData(form);
  //   }
  // }, [data]);

  // useEffect(() => {
  //   getForm();
  // }, [getForm]);

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

  const handleUpdate = async (formData: any, personId: string) => {
    const files = formData.getAll("files[]");
    console.log("files", files);
    try {
      for (const file of files) {
          const apiFormData = new FormData();
          apiFormData.append("files", file); // Use "file" for individual file uploads
  
          await personApi.addImage(apiFormData, personId).then(async (res) => {
              console.log("API response for file:", res.data.id);
          });
      }
  
      enqueueSnackbar("Cập nhật hồ sơ nhận diện đối tượng thành công ", {
          variant: "success",
      });
  } catch (error) {
      handleError(error, "Cập nhật hồ sơ nhận diện đối tượng không thành công");
      return ResultEnum.error;
  }
  return ResultEnum.success;
  };



  // * * * * * * * * SUBMIT FUNCTION * * * * * * * * *
  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    let formData = new FormData(event.currentTarget);

    if (!props.data) {
      for (let i = 0; i < files.length; i++) {
        if (files[i].file !== null) {
          console.log(`Appending file ${i}:`, files[i].file);
          formData.append("files[]", files[i].file as File); 
        }
      }
    }
    const formJson = Object.fromEntries(formData.entries());

    if (!checkValidate(formJson)) return;

    setLoading(true);
    console.log("formData entries:", Array.from(formData.entries()));
    console.log("formJson", formJson);
    let result = await handleUpdate(formData, personId ?? "");
    console.log("result", result);
    setLoading(false);
    if (result !== ResultEnum.success && result !== ResultEnum.error) {
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
        onClose={function (): void {
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
        {"Cập nhật đối tượng"}
      </DialogTitle>
      <DialogContent>
        <Grid container spacing={2}>
          <Grid item xs={12}>
            <ChooseIdentificationUser
              label={"Tên đối tượng"}
              name="name"
              onChange={handlePersonChange}
              value = {formData["name"]}
              textError={formErr?.name ?? ""}
              onClose={handleClose}
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
        <SubmitBtn type="submit" text="Xác nhận" />
      </DialogActions>
    </Dialog>
  );
}
