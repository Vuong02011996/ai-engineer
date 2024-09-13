import * as React from "react";
import Image from "next/image";
import { enqueueSnackbar } from "notistack";
import { Tooltip } from "@mui/material";

export interface ICopyBtnProps {
  text?: string;
  title?: string;
}

export function CopyBtn(props: ICopyBtnProps) {
  const handleCopy = () => {
    try {
      if (!props.text) return;
      navigator.clipboard.writeText(props?.text || "");
      enqueueSnackbar(`Sao chép ${props.title ?? ""} thành công`, {
        variant: "success",
      });
    } catch (error) {
      enqueueSnackbar(`Sao chép ${props.title ?? ""} không thành công`, {
        variant: "error",
      });
      console.log("Copy error", error);
    }
  };
  return (
    <Tooltip title={`Sao chép ${props.title}`}>
      <div onClick={handleCopy}>
        <Image src="/icons/copy.svg" width={16} height={16} alt="copy" />
      </div>
    </Tooltip>
  );
}
