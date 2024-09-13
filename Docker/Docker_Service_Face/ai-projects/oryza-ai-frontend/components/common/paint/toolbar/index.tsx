import { Tooltip } from "@mui/material";
import clsx from "clsx";
import Image from "next/image";
import { useState } from "react";
type ToolbarType = "MOVE" | "PEN" | "REMOVE" | "RESET" | "NONE" | "REFRESH";

export interface IPainToolbarProps {
  onMove?: () => void;
  onPaint?: () => void;
  onReset?: () => void;
  onRemove?: () => void;
  onSubmit?: () => void;
  onRefresh?: () => void;
  isShowSubmit?: boolean;
}

export function PainToolbar(props: IPainToolbarProps) {
  const [toolbar, setToolbar] = useState<ToolbarType>("PEN");

  // on MOVE click
  function onMove() {
    if (props.onMove) props.onMove();
    setToolbar((prev) => (prev === "MOVE" ? "NONE" : "MOVE"));
  }

  // on PEN click
  function onPaint() {
    if (props.onPaint) props.onPaint();
    setToolbar("PEN");
  }

  // on RESET click
  function onReset() {
    if (props.onReset) props.onReset();
  }

  // on REMOVE click
  function onRemove() {
    if (props.onRemove) props.onRemove();
  }

  // on REMOVE click
  function onRefresh() {
    if (props.onRefresh) props.onRefresh();
  }

  // on REMOVE click
  function onSubmit() {
    if (props.onSubmit) props.onSubmit();
    setToolbar("NONE");
  }

  return (
    <div className="w-full h-10 bg-grayOz flex flex-row justify-center">
      <div className="flex flex-1 flex-row items-center">
        {_renderButton({
          icon: "/icons/move-btn.svg",
          label: "Di chuyển",
          active: toolbar === "MOVE",
          onClick: onMove,
          size: 16,
        })}
        {_renderButton({
          icon: "/icons/draw-button.svg",
          label: "Vẽ điểm",
          active: toolbar === "PEN",
          onClick: onPaint,
          size: 18,
        })}
        {_renderButton({
          icon: "/icons/remove-white.svg",
          label: "Xóa tất cả",
          active: toolbar === "RESET",
          onClick: onReset,
          size: 14,
        })}
        {_renderButton({
          icon: "/icons/close.svg",
          label: "Xóa",
          active: toolbar === "REMOVE",
          onClick: onRemove,
          size: 12,
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
}

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
