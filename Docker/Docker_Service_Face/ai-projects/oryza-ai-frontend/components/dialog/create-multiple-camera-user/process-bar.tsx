import * as React from "react";
import clsx from "clsx";

export interface IProcessbarProps {
  percent: number;
}

export function Processbar(props: IProcessbarProps) {
  const percent = Math.min(Math.max(props.percent, 0), 100).toFixed(0);

  return (
    <div className="h-1 w-full bg-[#171C1F] rounded-2xl relative overflow-hidden ">
      <div
        className={clsx("h-full bg-aquaTranquil transition-all duration-300")}
        style={{
          width: `${percent}%`,
        }}
      />
    </div>
  );
}
