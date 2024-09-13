import { Tooltip } from "@mui/material";
import clsx from "clsx";
import Image from 'next/image';
import { useState, forwardRef, useImperativeHandle } from "react";

type ToolbarType = "ADD" | "REMOVE" | "RESET" | "NONE" | "REFRESH";

export interface IDrawLaneToolbarProps {
  onMove?: () => void;
  onAddLane?: () => void;
  onRemoveLane?: () => void;
  onReset?: () => void;
  onRemove?: () => void;
  onSubmit?: () => void;
  onRefresh?: () => void;
  isShowSubmit?: boolean;
}

export interface IDrawLaneToolbarRef {
  setToolbar: (toolbar: ToolbarType) => void;
}

export const DrawLaneToolbar = forwardRef<IDrawLaneToolbarRef, IDrawLaneToolbarProps>((props, ref) => {
  const [toolbar, setToolbar] = useState<ToolbarType>("NONE");

  useImperativeHandle(ref, () => ({
    setToolbar,
  }));

  // on ADD LANE click
  function onAddLane() {
    if (props.onAddLane) props.onAddLane();
    setToolbar("ADD");
  }

  // on RESET click
  function onReset() {
    if (props.onReset) props.onReset();
  }

  // on REMOVE click
  function onRemoveLane() {
    if (props.onRemoveLane) props.onRemoveLane();
  }

  // on REMOVE click
  function onRefresh() {
    if (props.onRefresh) props.onRefresh();
  }

  // on REMOVE click
  function onSubmit() {
    if (props.onSubmit) props.onSubmit();
    // setToolbar("NONE");
  }

  return (
    <div className="w-full h-10 bg-grayOz flex flex-row justify-center">
      <div className="flex flex-1 flex-row items-center">
        {_renderButton({
          icon: "/icons/add-new.svg",
          label: "Thêm làn đường",
          active: toolbar === "ADD",
          onClick: onAddLane,
          size: 16,
        })}
        {_renderButton({
          icon: "/icons/close.svg",
          label: "Xóa làn đường",
          active: toolbar === "REMOVE",
          onClick: onRemoveLane,
          size: 12,
        })}
        {_renderButton({
          icon: "/icons/remove-white.svg",
          label: "Xóa tất cả",
          active: toolbar === "RESET",
          onClick: onReset,
          size: 14,
        })}
        
        {_renderButton({
          icon: "/icons/reset.svg",
          label: "Tải lại hình ảnh",
          active: toolbar === "REFRESH",
          onClick: onRefresh,
          size: 14,
        })}
      </div>

      {props.isShowSubmit && (
        <button
          type="button"
          onClick={onSubmit}
          className="bg-primary h-full px-3 text-[14px] font-medium text-white hover:bg-primaryDark active:bg-primaryDark"
        >
          Xong
        </button>
      )}
    </div>
  );
});

DrawLaneToolbar.displayName = "DrawLaneToolbar";

function _renderButton({
  icon,
  label,
  onClick,
  active,
  size,
}: {
  icon: string;
  label: string;
  onClick?: (e: any) => void;
  active?: boolean;
  size: number;
}) {
  return (
    <Tooltip title={label} placement="bottom" arrow>
      <div
        onClick={onClick}
        className={clsx(
          "w-10 h-full flex items-center justify-center  transition-all duration-200  cursor-pointer select-none",
          active
            ? "bg-primary hover:bg-primaryDark"
            : "bg-grayOz hover:bg-blackOz active:bg-black"
        )}
      >
        <Image src={icon} width={size} height={size} alt="draw-button" />
      </div>
    </Tooltip>
  );
}