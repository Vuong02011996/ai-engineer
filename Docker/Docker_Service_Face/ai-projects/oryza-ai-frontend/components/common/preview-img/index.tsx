import CloseRoundedIcon from "@mui/icons-material/CloseRounded";
import Dialog from "@mui/material/Dialog";
import IconButton from "@mui/material/IconButton";
import Slide from "@mui/material/Slide";
import { TransitionProps } from "@mui/material/transitions";
import Image from "next/image";
import * as React from "react";
import ImageFallback from "../image-fallback";
import { Stack } from "@mui/material";
import clsx from "clsx";

const Transition = React.forwardRef(function Transition(
  props: TransitionProps & {
    children: React.ReactElement;
  },
  ref: React.Ref<unknown>
) {
  return <Slide direction="up" ref={ref} {...props} />;
});

export interface IPreviewImageProps {
  children: React.ReactNode;
  className: any;
  src: string;
  openWithDoubleClick?: boolean;
}

export function PreviewImage({
  children,
  className,
  src,
  openWithDoubleClick,
}: IPreviewImageProps) {
  const [open, setOpen] = React.useState(false);

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  return (
    <React.Fragment>
      <div
        className={className}
        onClick={!openWithDoubleClick ? handleClickOpen : () => {}}
        onDoubleClick={openWithDoubleClick ? handleClickOpen : () => {}}
      >
        {children}
      </div>

      <Dialog
        fullScreen
        open={open}
        onClose={handleClose}
        TransitionComponent={Transition}
      >
        <div className="relative w-screen h-screen  ">
          <ImageFallback
            src={src}
            fallbackSrc={"/images/logo-oryza.png"}
            fill
            className="object-contain bg-black"
            alt={"Hình ảnh ghi nhận"}
          />

          <div
            onClick={handleClose}
            aria-label="delete"
            title="Đóng"
            className={clsx(
              "w-[32px] h-[32px] flex top-[16px] right-[16px] absolute  bg-white shadow-shadown1 hover:opacity-75 z-9999 rounded-full",
              "flex items-center justify-center cursor-pointer"
            )}
          >
            <CloseRoundedIcon fontSize="inherit" />
          </div>
        </div>
      </Dialog>
    </React.Fragment>
  );
}
