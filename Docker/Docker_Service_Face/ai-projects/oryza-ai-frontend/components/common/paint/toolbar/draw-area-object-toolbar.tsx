// for leaving recognition, draw 1 lane and objects
import { Tooltip } from "@mui/material";
import clsx from "clsx";
import Image from 'next/image';
import { forwardRef, useState, useImperativeHandle } from "react"

type ToolbarType = "MOVE" | "ADD_AREA" | "ADD_OBJECTS" | "REMOVE" | "RESET" | "REFRESH" | "NONE";

export interface IDrawAreaObjectToolbarProps {
  onMove?: () => void;
  onAddArea?: () => void;
  onAddObjects?: () => void;
  onRemove?: () => void;
  onReset?: () => void;
  onRefresh?: () => void;
  onSubmit?: () => void;
  isShowSubmit?: boolean;
}

export interface IDrawAreaObjectToolbarRef {
  setToolbar: (toolbar: ToolbarType) => void; 
}

export const DrawAreaObjectToolbar = forwardRef<IDrawAreaObjectToolbarRef, IDrawAreaObjectToolbarProps>((props, ref) => {
  const [toolbar, setToolbar] = useState<ToolbarType>("NONE");

  useImperativeHandle(ref, () => ({
    setToolbar,
  }));

  // on MOVE click
  function onMove() {
    if (props.onMove) props.onMove();
    setToolbar("MOVE");
  }

  // on ADD LANE click
  function onAddArea() {
    if (props.onAddArea) props.onAddArea();
    setToolbar("ADD_AREA");
  }

  // on ADD OBJECT click
  function onAddObjects() {
    if (props.onAddObjects) props.onAddObjects();
    setToolbar("ADD_OBJECTS");
  }

  // on RESET click
  function onReset() {
    if (props.onReset) props.onReset();
    setToolbar("ADD_AREA");
  }

  // on REMOVE click
  function onRemove() {
    if (props.onRemove) props.onRemove();
  }

  // on REFRESH click
  function onRefresh() {
    if (props.onRefresh) props.onRefresh();
  }

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
          icon: "/icons/area.svg",
          label: "Vẽ khu vực theo dõi",
          active: toolbar === "ADD_AREA",
          onClick: onAddArea,
          size: 16,
        })}
        {_renderButton({
          icon: "/icons/add-new.svg",
          label: "Vẽ đối tượng",
          active: toolbar === "ADD_OBJECTS",
          onClick: onAddObjects,
          size: 16,
        })}
        {_renderButton({
          icon: "/icons/close.svg",
          label: "Xóa điểm vừa vẽ",
          active: toolbar === "REMOVE",
          onClick: onRemove,
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

DrawAreaObjectToolbar.displayName = "DrawLaneAndObjectToolbar";

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