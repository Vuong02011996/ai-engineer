import * as React from "react";
import Icon from "../../icon";
import styles from "./style.module.css";

export interface IButton100Props {
  onClick?: React.MouseEventHandler<HTMLButtonElement> | undefined;
  onSubmit?: React.FormEventHandler<HTMLButtonElement> | undefined;
  text: string;
  icon?: string;
  className: string;
  disabled?: boolean | undefined;
}

export function Button100(props: IButton100Props) {
  const { text, icon, className } = props;
  return (
    <button
      onSubmit={props.onSubmit}
      onClick={props.onClick}
      disabled={props.disabled}
      className={`${styles.btn}  ${className} `}
    >
      {text}
    </button>
  );
}
