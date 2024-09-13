import { Outline2Btn } from "@/components/common/button/outline-2-btn";
import * as React from "react";

export interface IProfileItemProps {
  children: React.ReactNode;
  title: string;
  summary: string;
}

export function ProfileItem({ children, title, summary }: IProfileItemProps) {
  return (
    <div
      className={[
        "flex flex-row justify-between items-center py-3 border-b-2 transition-all duration-300 border-[#F8F8F8]",
      ].join(" ")}
    >
      <div>
        <p className="text-blackOz text-[18px] font-normal ">{title}</p>
        <div className="h-7    items-center flex  ">
          <p className="text-[#8E95A9] text-[14px] font-normal ">{summary}</p>
        </div>
      </div>

      <div className="flex flex-row space-x-24 items-center ">{children}</div>
    </div>
  );
}
