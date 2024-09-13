import { motion } from "framer-motion";
import * as React from "react";

export interface IOpactityAnimationProps {
  children: React.ReactNode;
  className?: string | undefined;
  duration?: number;
}

export function OpactityAnimation(props: IOpactityAnimationProps) {
  const { children, className, duration } = props;
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ ease: "easeInOut", duration: duration || 0.5 }}
      className={className}
    >
      {children}
    </motion.div>
  );
}
