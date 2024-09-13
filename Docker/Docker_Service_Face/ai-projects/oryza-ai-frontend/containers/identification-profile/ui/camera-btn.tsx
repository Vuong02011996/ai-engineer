import * as React from "react";
import clsx from "clsx";

export interface ICameraBtnProps {
  status: "ON" | "OFF";
  onClick?: React.MouseEventHandler<HTMLDivElement> | undefined;
}

export function CameraBtn(props: ICameraBtnProps) {
  return (
    <div
      onClick={props.onClick}
      className={clsx(
        "flex flex-row space-x-2 items-center justify-center p-3 rounded-lg  transition-all duration-300 select-none cursor-pointer ",
        props.status === "ON"
          ? "bg-primary hover:bg-primaryDark"
          : "bg-red hover:bg-redDark"
      )}
    >
      <div className="p-1 bg-white rounded w-5 h-5 flex item-center justify-center ">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="10"
          height="12"
          viewBox="0 0 10 12"
          fill="none"
        >
          <path
            fillRule="evenodd"
            clipRule="evenodd"
            d="M7.06565 3.44107C8.20343 4.05273 8.79057 5.07737 8.79057 6.45854C8.79057 8.45875 7.16668 10.0827 5.16646 10.0827C3.16621 10.0827 1.54231 8.45874 1.54231 6.45854C1.54231 5.06906 2.12185 4.0481 3.27078 3.43983C3.49451 3.32139 3.57998 3.0436 3.46154 2.81988C3.34311 2.59615 3.06532 2.51068 2.84159 2.62912C1.40218 3.39114 0.625 4.71775 0.625 6.45853C0.625 8.96501 2.65993 11 5.16647 11C7.67295 11 9.70788 8.96501 9.70788 6.45853C9.70788 4.72815 8.92545 3.39941 7.5 2.63308C7.27704 2.51321 6.9987 2.59691 6.87884 2.81988C6.75898 3.04284 6.84269 3.3212 7.06565 3.44107ZM4.69224 1.45866V4.43922C4.69224 4.69236 4.89776 4.89788 5.1509 4.89788C5.40404 4.89788 5.60956 4.69236 5.60956 4.43922V1.45866C5.60956 1.20552 5.40404 1 5.1509 1C4.89776 1 4.69224 1.20552 4.69224 1.45866Z"
            fill={props.status === "ON" ? "#007DC0" : "#E42727"}
            stroke={props.status === "ON" ? "#007DC0" : "#E42727"}
            strokeWidth="0.5"
          />
        </svg>
      </div>
      <p className="text-white text-[14px] font-medium">
        {props.status == "ON" ? "Bật" : "Tắt"} camera
      </p>
    </div>
  );
}
