import { CancelBtn, SubmitBtn } from "@/components/ui";
import Dialog from "@mui/material/Dialog";

export interface IConfirmDialogV2Props {
  open: boolean;
  handleClose: () => void;
  title: string;
  summany: string;
  submit: () => void;
  cancelText?: string;
  submitText?: string;
}

export function ConfirmDialogV2(props: IConfirmDialogV2Props) {
  const { open, handleClose, title, summany } = props;
  const handleSubmit = () => {
    props.submit();
    handleClose();
  };
  return (
    <Dialog
      open={open}
      keepMounted
      onClose={handleClose}
      aria-describedby="alert-dialog-slide-description"
    >
      <div className="pt-5 px-5">
        <p className="font-medium text-[20px]">{title}</p>
      </div>
      <div className="p-5">
        <p>{summany}</p>
      </div>
      <div className="flex justify-end px-5 pb-5 space-x-3">
        <CancelBtn onClick={handleClose} text={props.cancelText || "Không"} />
        <SubmitBtn
          onClick={handleSubmit}
          text={props.submitText || "Xác nhận"}
        />
      </div>
    </Dialog>
  );
}
