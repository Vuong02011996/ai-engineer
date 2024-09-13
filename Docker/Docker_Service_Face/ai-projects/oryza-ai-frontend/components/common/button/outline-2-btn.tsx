import * as React from "react";
import Image from "next/image";

export interface IOutline2BtnProps {
  onClick?: React.MouseEventHandler<HTMLDivElement> | undefined;
  icon?: string;
  text: string;
}

export function Outline2Btn(props: IOutline2BtnProps) {
  return (
    <div
      onClick={props.onClick}
      className="h-10 flex flex-row items-center space-x-2 rounded-lg border border-[#F2F2F2] px-3 py-2 select-none hover:border-transparent hover:shadow-shadown1 transition-all duration-300 cursor-pointer"
    >
      {props.icon && (
        <Image src={props.icon} alt="edit-btn" width={20} height={20} />
      )}

      <p className="text-grayOz font-medium text-[14px]">{props.text}</p>
    </div>
  );
}
