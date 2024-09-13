import * as React from "react";
import clsx from "clsx";

export interface ISubmitBtnProps extends React.HTMLProps<HTMLButtonElement> {
  text: string;
}

export function SubmitBtn(props: ISubmitBtnProps) {
  return (
    <button
      disabled={props.disabled}
      onClick={props.onClick}
      className={clsx(
        "min-w-[100px] shadow-shadown1 bg-primary rounded-lg px-[14px] py-2 capitalize text-white font-semibold text-sm hover:bg-primaryDark",
        "disabled:opacity-40 disabled:cursor-not-allowed"
      )}
    >
      {props.text}
    </button>
  );
}
