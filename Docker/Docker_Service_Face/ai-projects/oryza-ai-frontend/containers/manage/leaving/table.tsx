import { useManagement } from "@/context/manage-context";
import { EventData } from "@/interfaces/manage/event";
import { memo } from "react";
import { GridItemTable, ListItemTable } from "./table-item";
import { enqueueSnackbar } from "notistack";
import { eventApi } from "@/api-client/event";
export interface ITableLeavingItemProps {
  data: EventData;
  index: number;
}
const handleWatchVideo = async (eventId: string) => {
  if (!eventId) {
    enqueueSnackbar("Không tìm thấy ID của video", {
      variant: "error",
    });
    return;
  }
  try {
    let response = await eventApi.getRecord(eventId);
    const videoUrl = response.data.data;
    window.open(videoUrl, "_blank");
  } catch (error) {
    enqueueSnackbar("Không tải được video", {
      variant: "error",
    });
  }
};

function TableLeavingItem(props: ITableLeavingItemProps) {
  const { data, index } = props;
  const { viewType } = useManagement();

  if (viewType === "LIST") {
    return <ListItemTable data={data} index={index} handleWatchVideo={handleWatchVideo}/>;
  }
  if (viewType === "GRID") {
    return <GridItemTable data={data} index={index} handleWatchVideo={handleWatchVideo}/>;
  }

  return <></>;
}

export default memo(TableLeavingItem);
