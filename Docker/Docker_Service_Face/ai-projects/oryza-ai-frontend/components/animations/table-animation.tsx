import { motion } from "framer-motion";
import * as React from "react";

const base = 4;
const t = (d: any) => d * base;

export interface ITableAnimationProps {
  children: React.ReactNode;
}

export function TableAnimation(props: ITableAnimationProps) {
  const { children } = props;
  return (
    <motion.div
      initial={{ height: 0, opacity: 0 }}
      animate={{
        height: "auto",
        opacity: 1,
        transition: {
          duration: 0.3,
          type: "spring",
          opacity: { delay: t(0.025) },
        },
      }}
      exit={{ height: 0, opacity: 0 }}
      transition={{
        duration: t(0.15),
        type: "spring",
        bounce: 0,
        opacity: { delay: t(0.03) },
      }}
      className="relative"
    >
      {children}
    </motion.div>
  );
}
