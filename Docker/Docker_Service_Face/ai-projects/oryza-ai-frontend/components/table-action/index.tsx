import MoreIcon from "@/assets/svgs/more-vertical-2.svg";
import { ActionPopup } from "@/components";
import * as React from "react";

export interface ITableActionProps {
  onUpdate?: () => void;
  onRemove?: () => void;
  onEdit?: () => void;
  onCopy?: () => void;
  onAIHandle?: () => void;
  onCreate?: () => void;
  onDebug?: () => void;
}

export function TableAction(props: ITableActionProps) {
  const [anchorEl, setAnchorEl] = React.useState<HTMLButtonElement | null>(
    null
  );

  const handleClick = (event: any) => {
    event.stopPropagation();
    event.nativeEvent.stopImmediatePropagation();

    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const open = Boolean(anchorEl);
  const id = open ? "simple-popover" : undefined;

  return (
    <div className="relative">
      <div
        onClick={handleClick}
        title="Hành động"
        className={`w-8 h-8 flex items-center justify-center rounded-[6px] hover:bg-[#E3E5E5] transition-all duration-200 ${
          open && "border-2 border-[#78C6E7]"
        }`}
      >
        <MoreIcon className="" />
      </div>
      {open && (
        <ActionPopup
          onClose={handleClose}
          anchorEl={anchorEl}
          open={open}
          id={id}
          onEdit={props.onEdit}
          onRemove={props.onRemove}
          onUpdate={props.onUpdate}
          onCopy={props.onCopy}
          onAIHandle={props.onAIHandle}
          onCreate={props.onCreate}
          onDebug={props.onDebug}
        />
      )}
    </div>
  );
}
