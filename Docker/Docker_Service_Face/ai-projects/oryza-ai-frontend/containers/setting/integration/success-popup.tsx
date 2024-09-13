import Button from "@mui/material/Button";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogContentText from "@mui/material/DialogContentText";
import DialogTitle from "@mui/material/DialogTitle";
import Slide from "@mui/material/Slide";
import { TransitionProps } from "@mui/material/transitions";
import * as React from "react";
import Image from "next/image";
import CloseRoundedIcon from "@mui/icons-material/CloseRounded";
import { IconButton, Stack, Typography } from "@mui/material";

const Transition = React.forwardRef(function Transition(
  props: TransitionProps & {
    children: React.ReactElement<any, any>;
  },
  ref: React.Ref<unknown>
) {
  return <Slide direction="up" ref={ref} {...props} />;
});
export interface ISucsessPopupProps {
  open: boolean;
  handleClose: () => void;
}

export function SucsessPopup(props: ISucsessPopupProps) {
  const { open, handleClose } = props;
  return (
    <Dialog
      open={open}
      TransitionComponent={Transition}
      onClose={handleClose}
      PaperProps={{
        sx: {
          borderRadius: "11px",
          boxShadow: "0px 1px 10px 0px rgba(34, 34, 34, 0.10)",
          padding: "24px",
          position: "relative",
        },
      }}
    >
      <Stack sx={{ position: "relative", alignItems: "center" }}>
        <IconButton
          onClick={handleClose}
          aria-label="delete"
          size="small"
          title="Đóng"
          className="w-[32px] h-[32px] flex top-[-10px] right-[-10px]"
          sx={{
            position: "absolute",
          }}
        >
          <CloseRoundedIcon fontSize="inherit" sx={{ fontSize: 24 }} />
        </IconButton>
        <Image
          src="/icons/success.svg"
          alt="success icon"
          width={60}
          height={60}
        />
        <Typography
          sx={{
            color: "#323232",
            fontSize: 16,
            fontWeight: 600,
            pt: "24px",
            pb: "6px",
          }}
        >
          Kết nối thành công
        </Typography>
        <Typography
          sx={{
            color: "#55595D",
            fontSize: 14,
            fontWeight: 400,
          }}
        >
          Đã kết nối thành công cho Oryza AI Nx Plugin
        </Typography>
      </Stack>
    </Dialog>
  );
}
