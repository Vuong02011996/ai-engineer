import {
  CircularProgressProps,
  Box,
  CircularProgress,
  circularProgressClasses,
  Dialog,
} from "@mui/material";
import * as React from "react";

export interface ILoadingDialogProps {
  open: boolean;
  onClose: () => void;
  text?: string;
}

export function LoadingDialog(props: ILoadingDialogProps) {
  const { onClose, open, text } = props;
  const handleClose = () => {
    onClose();
  };

  return (
    <Dialog onClose={handleClose} open={open}>
      <div className="p-8 items-center justify-center flex flex-col h-fit space-y-8 ">
        <LoadingProgress />
        {text && <p className="text-grayOz text-[16px] font-normal ">{text}</p>}
      </div>
    </Dialog>
  );
}
//
function LoadingProgress(props: CircularProgressProps) {
  return (
    <Box sx={{ position: "relative", height: "fit-content" }}>
      <CircularProgress
        variant="indeterminate"
        disableShrink
        sx={{
          "svg circle": { stroke: "url(#my_gradient)" },
          animationDuration: "1s",
          [`& .${circularProgressClasses.circle}`]: {
            strokeLinecap: "round",
          },
        }}
        size={60}
        thickness={4}
        {...props}
      />
      <svg width={0} height={0}>
        <defs>
          <linearGradient id="my_gradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#2F80ED" />
            <stop offset="100%" stopColor="#fff" />
          </linearGradient>
        </defs>
      </svg>
    </Box>
  );
}
