import { motion } from "framer-motion";
import * as React from "react";

const base = 4;

const t = (d: any) => d * base;

export interface IImageItemProps {
  children: React.ReactNode;
}

export function ImageItem(props: IImageItemProps) {
  const { children } = props;
  return (
    <motion.div
      className=" bg-gray-300 h-[150px] relative"
      initial={{ height: 0, opacity: 0 }}
      animate={{
        height: "150px",
        opacity: 1,
        transition: {
          duration: 0.3,
          type: "spring",
          opacity: { delay: t(0.125) },
        },
      }}
      exit={{ height: 0, opacity: 0 }}
      transition={{
        duration: t(0.15),
        type: "spring",
        bounce: 0,
        opacity: { delay: t(0.03) },
      }}
    >
      {children}
    </motion.div>
  );
}
