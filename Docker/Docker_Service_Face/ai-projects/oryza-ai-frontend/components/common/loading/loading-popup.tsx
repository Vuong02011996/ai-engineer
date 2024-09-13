import * as React from "react";
import { Loading } from ".";
import { Backdrop } from "@mui/material";

export interface ILoadingPopupProps {
  open: boolean;
  handleClose?: any;
}

export function LoadingPopup(props: ILoadingPopupProps) {
  const { handleClose, open } = props;
  return (
    <Backdrop
      sx={{ color: "#fff", zIndex: (theme) => theme.zIndex.drawer + 1, display: "none" }}
      open={open}
      onClick={handleClose}
    >
      <Loading color="white" />
    </Backdrop>
  );
}
