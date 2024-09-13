import { Skeleton } from "@mui/material";
import * as React from "react";
import Scrollbar from "../common/scrollbar";

export interface ICameraTableSkeletonProps {}

export function CameraTableSkeleton(props: ICameraTableSkeletonProps) {
  return (
    <div className="h-full w-full">
      <Skeleton variant="rectangular" width={"100%"} height={"32px"} />
      <div className="h-calc92 overflow-auto space-y-2 mt-2">
        {[...Array(6)].map((_, index) => {
          return <Skeleton key={index} variant="rounded" height={80} />;
        })}
      </div>
    </div>
  );
}
