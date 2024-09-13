import * as React from "react";
import Icon from "../../icon";
import styles from "./style.module.css";

export interface OutlineBtnProps {
  onClick?: React.MouseEventHandler<HTMLButtonElement> | undefined;
  text: string;
  icon?: string;
  className: string;
  classIcon?: string;
}

export function OutlineBtn(props: OutlineBtnProps) {
  const { text, icon, className, classIcon } = props;
  return (
    <button
      onClick={props.onClick}
      className={`${styles.bigBtn}  ${className} `}
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="16"
        height="16"
        viewBox="0 0 16 16"
        fill="none"
      >
        <rect y="0.00012207" width="16" height="16" rx="4" fill="#007DC0" />
        <path
          fillRule="evenodd"
          clipRule="evenodd"
          d="M8 4.00012C8.44183 4.00012 8.8 4.35829 8.8 4.80012V7.20012H11.2C11.6418 7.20012 12 7.55829 12 8.00012C12 8.44195 11.6418 8.80012 11.2 8.80012H8.8V11.2001C8.8 11.642 8.44183 12.0001 8 12.0001C7.55817 12.0001 7.2 11.642 7.2 11.2001V8.80012H4.8C4.35817 8.80012 4 8.44195 4 8.00012C4 7.55829 4.35817 7.20012 4.8 7.20012H7.2V4.80012C7.2 4.35829 7.55817 4.00012 8 4.00012Z"
          fill="white"
        />
      </svg>
      {text}
    </button>
  );
}
