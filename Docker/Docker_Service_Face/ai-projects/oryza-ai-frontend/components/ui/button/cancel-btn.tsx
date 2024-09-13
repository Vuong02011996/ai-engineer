import * as React from "react";

export interface ICancelBtnProps extends React.HTMLProps<HTMLButtonElement> {
  text: string;
}

export function CancelBtn(props: ICancelBtnProps) {
  return (
    <button
      type="button"
      onClick={props.onClick}
      className="min-w-[100px] shadow-shadown1 bg-white rounded-lg px-[14px] py-2 capitalize text-grayOz font-semibold text-sm hover:bg-white hover:shadow-shadown1"
    >
      {props.text}
    </button>
  );
}
