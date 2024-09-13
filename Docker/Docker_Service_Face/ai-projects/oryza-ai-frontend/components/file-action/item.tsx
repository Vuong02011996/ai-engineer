import * as React from "react";

export interface IActionItemProps {
  active: boolean;
  onClick: () => void;
  tooltip?: string;
  icon: string;
}

export function ActionItem(props: IActionItemProps) {
  const { onClick, icon, tooltip, active } = props;
  const Icon = props.icon;
  return (
    <div
      onClick={onClick}
      className={` ${
        active ? "bg-white shadow-shadown1" : "bg-transparent shadow-none"
      } p-[8px] rounded-[8px] cursor-pointer ${tooltip && "tooltip"}`}
    >
      <Icon />
      {tooltip && <span className="tooltiptext">{tooltip}</span>}
    </div>
  );
}
