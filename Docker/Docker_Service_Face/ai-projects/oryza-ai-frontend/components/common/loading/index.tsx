import * as React from "react";

export interface ILoadingProps {
  color?: "black" | "white";
}

export function Loading(props: ILoadingProps) {
  const color = props.color || "black";
  return (
    <div className="h-full w-full flex items-center justify-center red">
      <div className={`loader ${color === "white" && "loader-white"}`}></div>
    </div>
  );
}
