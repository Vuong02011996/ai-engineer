import { motion } from "framer-motion";
import * as React from "react";
import clsx from "clsx";
import { ImageError } from "./image-error";

const base = 4;

const t = (d: any) => d * base;

export interface IImageItemProps {
  children: React.ReactNode;
  isError?: boolean;
  urlError?: string;
}

export function ImageItem(props: IImageItemProps) {
  const { children, isError, urlError } = props;
  return (
    <motion.div
      className={clsx(
        "bg-gray-300 h-[150px] relative",
        isError ? "border-2 border-error rounded-[6px]" : ""
      )}
      style={
        isError
          ? {
              background: `linear-gradient(0deg, rgba(255, 255, 255, 0.80) 0%, rgba(255, 255, 255, 0.80) 100%), url(${urlError}) lightgray 50%`,
              backgroundSize: "cover",
              backgroundPosition: "center",
              backgroundRepeat: "no-repeat",
            }
          : {}
      }
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
