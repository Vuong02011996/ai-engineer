import * as React from "react";
import EditIcon from "@/assets/svgs/edit-icon.svg";
import RemoveIcon from "@/assets/svgs/remove-icon.svg";
import UpdateIcon from "@/assets/svgs/update-icon.svg";
import CopyIcon from "@/assets/svgs/copy.svg";
import AIIcon from "@/assets/svgs/services-active.svg";
import CreateIcon from "@/assets/svgs/create-green.svg";
import DebugIcon from "@/assets/svgs/wrench-clock.svg";
import { Popover, Typography } from "@mui/material";

export interface IActionPopupProps {
  onClose: () => void;
  anchorEl: any;
  open: boolean;
  id: any;
  onUpdate?: () => void;
  onRemove?: () => void;
  onEdit?: () => void;
  onCopy?: () => void;
  onAIHandle?: () => void;
  onCreate?: () => void;
  onDebug?: () => void;
}

export function ActionPopup(props: IActionPopupProps) {
  const { anchorEl, id, open } = props;
  return (
    <Popover
      id={id}
      open={open}
      anchorEl={anchorEl}
      onClose={(e: any) => {
        e.stopPropagation();
        props.onClose();
      }}
      anchorOrigin={{
        vertical: "bottom",
        horizontal: "right",
      }}
      transformOrigin={{
        vertical: "top",
        horizontal: "right",
      }}
      slotProps={{
        paper: {
          sx: {
            borderRadius: "8px",
            boxShadow: "0px 1px 10px 0px rgba(34, 34, 34, 0.1)",
          },
        },
      }}
    >
      {props.onCreate && (
        <div
          onClick={(event) => {
            event.stopPropagation();
            if (props.onCreate) props.onCreate();
            if (props.onClose) props.onClose();
          }}
        >
          {_renderItem(CreateIcon, "Tạo mới")}
        </div>
      )}
      {props.onAIHandle && (
        <div
          onClick={(event) => {
            event.stopPropagation();
            if (props.onAIHandle) props.onAIHandle();
            if (props.onClose) props.onClose();
          }}
        >
          {_renderItem(AIIcon, "Cấu hình AI")}
        </div>
      )}
      {props.onCopy && (
        <div
          onClick={(event) => {
            event.stopPropagation();
            if (props.onCopy) props.onCopy();
            if (props.onClose) props.onClose();
          }}
        >
          {_renderItem(CopyIcon, "Sao chép")}
        </div>
      )}

      {props.onEdit && (
        <div
          onClick={(event) => {
            event.stopPropagation();
            if (props.onEdit) props.onEdit();
            if (props.onClose) props.onClose();
          }}
        >
          {_renderItem(EditIcon, "Chỉnh sửa")}
        </div>
      )}

      {props.onRemove && (
        <div
          onClick={(event) => {
            event.stopPropagation();
            if (props.onRemove) props.onRemove();
            if (props.onClose) props.onClose();
          }}
        >
          {_renderItem(RemoveIcon, "Xóa")}
        </div>
      )}

      {props.onUpdate && (
        <div
          onClick={(event) => {
            event.stopPropagation();
            if (props.onUpdate) props.onUpdate();
            if (props.onClose) props.onClose();
          }}
        >
          {_renderItem(UpdateIcon, "Cập nhật")}
        </div>
      )}
      {/* {props.onDebug && (
        <div
          onClick={(event) => {
            event.stopPropagation();
            if (props.onDebug) props.onDebug();
            if (props.onClose) props.onClose();
          }}
        >
          {_renderItem(DebugIcon, "Debug")}
        </div>
      )} */}
    </Popover>
  );
}
function _renderItem(icon: any, text: string) {
  const Icon = icon;
  return (
    <div className="flex flex-row space-x-[4px] items-center justify-start px-3 py-1 hover:bg-[#F8F8F8] transition-all duration-300  border-b border-[#F2F2F2] select-none cursor-pointer">
      <div className="w-6 h-6 flex items-center justify-center mr-1">
        <Icon />
      </div>
      <p className="min-w-[80px] text-[#808080] text-sm font-medium ">{text}</p>
    </div>
  );
}
