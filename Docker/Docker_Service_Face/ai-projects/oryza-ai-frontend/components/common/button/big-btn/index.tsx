import * as React from "react";
import styles from "./style.module.css";
import { useMediaQuery, useTheme } from "@mui/material";

export interface IBigBtnProps {
  onClick?: React.MouseEventHandler<HTMLButtonElement> | undefined;
  text: string;
  icon: string;
  className: string;
  classIcon: string;
}

export function BigBtn(props: IBigBtnProps) {
  const { text, icon, className, classIcon } = props;
  const Icon = props.icon;
  const theme = useTheme();
  const smScreen = useMediaQuery(theme.breakpoints.down("md"));
  return (
    <button
      onClick={props.onClick}
      className={`${styles.bigBtn}  ${className} `}
    >
      {icon && (
        <div className={`${classIcon ?? ""} ${styles.btnIcon} `}>
          <Icon />
        </div>
      )}
      {text}
    </button>
  );
}
