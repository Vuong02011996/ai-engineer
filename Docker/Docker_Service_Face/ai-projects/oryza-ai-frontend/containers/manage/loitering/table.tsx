import { eventApi } from "@/api-client/event";
import { useManagement } from "@/context/manage-context";
import { EventData } from "@/interfaces/manage/event";
import { enqueueSnackbar } from "notistack";
import { memo } from "react";
import { GridItemTable, ListItemTable } from "./table-item";
export interface ITableLoiteringItemProps {
  data: EventData;
  index: number;
}

function TableLoiteringItem(props: ITableLoiteringItemProps) {
  const { data, index } = props;
  const { viewType } = useManagement();

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

  if (viewType === "GRID") {
    return (
      <GridItemTable
        data={data}
        index={index}
        handleWatchVideo={handleWatchVideo}
      />
    );
  }
  if (viewType === "LIST") {
    return (
      <ListItemTable
        data={data}
        index={index}
        handleWatchVideo={handleWatchVideo}
      />
    );
  }
  return <></>;
}
export default memo(TableLoiteringItem);
