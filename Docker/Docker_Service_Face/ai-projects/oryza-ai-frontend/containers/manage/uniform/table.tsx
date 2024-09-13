import { watchVideo } from "@/api-client/event";
import { Status } from "@/components";
import ImageFallback from "@/components/common/image-fallback";
import { PreviewImage } from "@/components/common/preview-img";
import { WatchVideoBtn } from "@/components/ui";
import { useManagement } from "@/context/manage-context";
import { EventData } from "@/interfaces/manage/event";
import moment from "moment";
import { memo } from "react";
import { GridItemTable, ListItemTable } from "./table-item";

export interface ITableUniformItemProps {
  data: EventData;
  index: number;
}

function TableUniformItem(props: ITableUniformItemProps) {
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

export default memo(TableUniformItem);
