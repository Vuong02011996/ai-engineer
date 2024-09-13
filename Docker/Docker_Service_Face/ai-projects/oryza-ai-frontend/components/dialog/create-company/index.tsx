import TextFieldFormV2 from "@/components/common/text-field/text-field-form-v2";
import { CompanyRes } from "@/interfaces/company";
import { formatCompanyData } from "@/libs/company";
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
import { ResultEnum } from "@/constants/enum";
import { LoadingPopup } from "@/components/common/loading/loading-popup";

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
  domain: "",
};

export interface ICreateCompanyDialogProps {
  open: boolean;
  handleClose: () => void;
  submit: (data: any) => Promise<ResultEnum>;
  data?: CompanyRes;
}

export function CreateCompanyDialog(props: ICreateCompanyDialogProps) {
  const { open, handleClose, submit, data } = props;

  const [formErr, setFormErr] = useState<any>({});
  const [formData, setFormData] = useState<any>(formInit);
  const [loading, setLoading] = useState(false);

  const handleChange = (name: string, value: string) => {
    setFormData({ ...formData, [name]: value });
  };

  useEffect(() => {
    if (data) {
      let response: CompanyRes[] = formatCompanyData([data]);
      setFormData(response[0]);
    }
  }, [data]);

  const handleSubmit = async () => {
    if (!checkValidate()) return;
    setLoading(true);
    let result = await submit(formData);
    if (result === ResultEnum.success) {
      setFormData(formInit);
      props.handleClose();
    }
    setLoading(false);
  };

  const checkValidate = () => {
    let hasError = false;
    const MIN = 2;
    const MAX = 150;

    const name = Validator.checkNotEmpty(formData["name"] ?? "", MIN, MAX);
    const domain = Validator.checkNotEmpty(formData["domain"] ?? "");

    let error = {
      ...formErr,
      name: name,
      domain: domain,
    };

    if (error.name !== null || error.domain !== null) {
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
      onClose={() => setConfirmDialog(true)}
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
        onClose={function (event: any): void {
          setConfirmDialog(false);
        }}
        submit={function (): void {
          setConfirmDialog(false);
          onClose();
        }}
      />
      <LoadingPopup open={loading} />

      {/* close btn */}
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
        {data ? "Chỉnh sửa công ty" : "Tạo mới công ty"}
      </DialogTitle>
      <DialogContent>
        <Grid container spacing={2}>
          <Grid item xs={12}>
            <TextFieldFormV2
              label="Tên công ty"
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
              label="Domain"
              required
              placeholder="https://website"
              name="domain"
              onChange={(event: any) => {
                const { name, value } = event.target;

                handleChange(name, value);
              }}
              value={formData["domain"]}
              textError={formErr.domain}
            />
          </Grid>
        </Grid>
      </DialogContent>
      <DialogActions sx={{ justifyContent: "center", gap: "16px" }}>
        <button
          onClick={() => setConfirmDialog(true)}
          className="min-w-[100px] shadow-shadown1 bg-white rounded-lg px-[14px] py-2 capitalize text-grayOz font-semibold text-sm hover:bg-white hover:shadow-shadown1"
        >
          Hủy bỏ
        </button>
        <button
          onClick={handleSubmit}
          className="min-w-[100px] shadow-shadown1 bg-primary rounded-lg px-[14px] py-2 capitalize text-white font-semibold text-sm hover:bg-primaryDark"
        >
          {data ? "Xác nhận" : "Tạo mới"}
        </button>
      </DialogActions>
    </Dialog>
  );
}
