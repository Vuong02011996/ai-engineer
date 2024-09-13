import * as React from "react";
import { useCallback, useState } from "react";

export type SystemType = "OVERLOAD" | "NORMAL";

export interface ISystemItemProps {
  percent: number;
  name: string;
  unit: string;
  value?: number;
  subName?: string;
}

export function SystemItem(props: ISystemItemProps) {
  const { percent, name, unit, value, subName } = props;
  const clampedPercent = Math.min(Math.max(percent, 0), 100).toFixed(0);
  const systemType: SystemType = React.useMemo(() => {
    return percent > 90 ? "OVERLOAD" : "NORMAL";
  }, [percent]);

  const bgColor = systemType === "OVERLOAD" ? "bg-[#FF7A00]" : "bg-[#4FC3F7]";
  const textColog =
    systemType === "OVERLOAD" ? "text-[#FF7A00]" : "text-[#64686D]";

  return (
    <div>
      <div className="flex flex-row justify-between">
        <p className="text-[#64686D] text-sm font-medium">
          {name} {typeof subName !== "undefined" && <span>: {subName}</span>}
        </p>
        {typeof value !== "undefined" && (
          <p className={`${textColog} text-xs font-medium`}>
            {value} {unit}
          </p>
        )}
      </div>
      <div className="h-5 w-full bg-[#E6EEF5]  rounded-r-lg relative flex">
        <div
          className={`p-1 ${bgColor} h-full rounded-r-lg transition-all duration-1000 flex justify-end items-center `}
          style={{
            width: `${clampedPercent}%`,
          }}
        >
          {Number(clampedPercent) >= 10 && (
            <p className="text-end text-[14px] font-normal pr-1 text-white">
              {clampedPercent}%
            </p>
          )}
        </div>
        {Number(clampedPercent) < 10 && (
          <p className="text-end text-[14px] font-normal pl-1 text-black">
            {clampedPercent}%
          </p>
        )}
      </div>
    </div>
  );
}
