import * as React from "react";
import WatchVideoIcon from "@/assets/svgs/video-camera.svg";
import clsx from "clsx";
import { motion } from "framer-motion";

export interface IWatchVideoBtnProps
  extends React.HTMLProps<HTMLButtonElement> {}

export function WatchVideoBtn(props: IWatchVideoBtnProps) {
  return (
    <motion.button
      initial={false}
      whileTap={{ scale: 0.95 }}
      whileHover={{ scale: 1.05 }}
      title="Xem video"
      onClick={props.onClick}
      type="button"
      className={clsx(
        " bg-grayOz hover:bg-gray-800 focus:outline-none  font-medium ",
        "rounded-full text-sm p-2.5 text-center inline-flex items-center me-2 ",
        "items-center justify-end flex "
      )}
    >
      <WatchVideoIcon />
    </motion.button>
  );
}
