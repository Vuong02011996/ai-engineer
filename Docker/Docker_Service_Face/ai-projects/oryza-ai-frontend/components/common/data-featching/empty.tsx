import * as React from "react";

export interface IEmptyDataProps {}

export function EmptyData(props: IEmptyDataProps) {
  return (
    <div className="h-full w-full flex items-center justify-center ">
      <p>Không có dữ liệu </p>
    </div>
  );
}
