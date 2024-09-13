import * as React from "react";
import { BASE_STATUS_STYLE } from "./style";
import { StatusState } from "./interface";
import { getStatus } from "./status";

export interface IStatusProps {
  status: StatusState;
}

export function Status(props: IStatusProps) {
  const status = getStatus(props.status);

  return (
    <div
      className={`rounded-[44px] py-1 px-4 ${status.bg} w-fit flex flex-row items-center space-x-[8px]`}
    >
      <div className={`w-2 h-2 rounded-full ${status.dotColor}`} />
      <p className={`${status.textColor} text-sm font-normal`}>{status.text}</p>
    </div>
  );
}
