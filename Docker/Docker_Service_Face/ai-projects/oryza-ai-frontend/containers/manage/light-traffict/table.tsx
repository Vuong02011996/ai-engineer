import { useManagement } from "@/context/manage-context";
import { EventData } from "@/interfaces/manage/event";
import { memo } from "react";
import { GridItemTable, ListItemTable } from "./table-item";

export interface ITableLightTraffictItemProps {
  data: EventData;
  index: number;
}

function TableLightTraffictItem(props: ITableLightTraffictItemProps) {
  const { data, index } = props;
  const { viewType } = useManagement();

  if (viewType === "LIST") {
    return <ListItemTable data={data} index={index} />;
  }
  if (viewType === "GRID") {
    return <GridItemTable data={data} index={index} />;
  }
  return <></>;
}

export default memo(TableLightTraffictItem);