import * as React from "react";
import Icon from "../common/icon";
import { useState } from "react";
import { ActionItem } from "./item";
import exportIcon from "@/assets/svgs/import.svg";
import improtIcon from "@/assets/svgs/exprot.svg";
import downloadIcon from "@/assets/svgs/download.svg";

export interface IFileActionProps {}

export function FileAction(props: IFileActionProps) {
  const [action, setAction] = useState<"EXPORT" | "IMPORT" | "DOWNLOAD">(
    "EXPORT"
  );
  const toggleAction = (value: "EXPORT" | "IMPORT" | "DOWNLOAD") => {
    setAction(value);
  };
  return (
    <div className="flex flex-row p-[4px] rounded-[8px] bg-[#F2F2F2]">
      <ActionItem
        active={action === "EXPORT"}
        onClick={() => toggleAction("EXPORT")}
        tooltip={"Xuất"}
        icon={exportIcon}
      />
      <ActionItem
        active={action === "IMPORT"}
        onClick={() => toggleAction("IMPORT")}
        tooltip={"Nhập"}
        icon={improtIcon}
      />
      <ActionItem
        active={action === "DOWNLOAD"}
        onClick={() => toggleAction("DOWNLOAD")}
        tooltip={"Tải"}
        icon={downloadIcon}
      />
    </div>
  );
}
