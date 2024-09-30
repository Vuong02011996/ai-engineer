import { useManagement } from "@/context/manage-context";
import { EventData } from "@/interfaces/manage/event";
import { memo } from "react";
import { GridItemTable, ListItemTable } from "./table-item";

export interface ITableLaneViolationProps {
  data: EventData;
  index: number;
}

export function TableLaneViolationItem(props: ITableLaneViolationProps) {
  const { data, index } = props;
  const { viewType } = useManagement();

  if (viewType === "GRID") {
    return <GridItemTable data={data} index={index} />;
  }
  if (viewType === "LIST") {
    return <ListItemTable data={data} index={index} />;
  }
  return <></>;
}

export default memo(TableLaneViolationItem);