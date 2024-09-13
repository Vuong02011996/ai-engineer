import * as React from "react";
import clsx from "clsx";
export interface IFieldNumberProps {
  text: string;
  value: string;
  onChange: (e: any) => void;
  textError: string;
}

export function FieldNumber(props: IFieldNumberProps) {
  const { text, value, onChange, textError } = props;
  return (
    <div className="flex flex-row items-center">
      <p className="flex-1 w-full text-[#808080] font-normal text-[14px]">
        {text}
      </p>
      <input
        value={value}
        onChange={onChange}
        type="number"
        placeholder="--"
        className={clsx(
          "w-14 border rounded-md text-center py-[6px] px-1 outline-none text-[#808080] font-normal text-[14px]",
          textError ? "border-[#E53935] placeholder-[#E53935]" : "border-[#E3E5E5]"
        )}
      />
    </div>
  );
}
