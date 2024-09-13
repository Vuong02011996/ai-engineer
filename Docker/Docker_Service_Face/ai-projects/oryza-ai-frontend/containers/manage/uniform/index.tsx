import { EmptyData, Loading } from "@/components/common";
import Scrollbar from "@/components/common/scrollbar";
import { TableHead } from "@/components/table";
import { LIMIT_ITEM } from "@/constants/config";
import headData from "@/data/manage/uniform";
import { EventData } from "@/interfaces/manage/event";
import TableUniformItem from "./table";
import { AnimatePresence } from "framer-motion";
import { TableAnimation } from "@/components";
import clsx from "clsx";
import { useManagement } from "@/context/manage-context";

export interface ITableUniformProps {
  loading: boolean;
  data: any;
  page: any;
}

export function TableUniform(props: ITableUniformProps) {
  const { loading, data, page } = props;
  const { viewType } = useManagement();

  return (
    <>
      {loading ? (
        <Loading />
      ) : !data || data.length === 0 ? (
        <EmptyData />
      ) : (
        <Scrollbar>
          {viewType === "LIST" && <TableHead dataHead={headData} />}
          <AnimatePresence initial={false}>
            <div
              className={clsx(
                viewType === "GRID" && "grid px-7 py-5 gap-10",
                viewType === "GRID" && "xs:grid-cols-1",
                viewType === "GRID" && "sm:grid-cols-2",
                viewType === "GRID" && "md:grid-cols-3",
                viewType === "GRID" && "tablet:grid-cols-4",
                viewType === "GRID" && "laptop:grid-cols-5",
                viewType === "GRID" && "desktop:grid-cols-7"
              )}
            >
              {data.map((value: EventData, index: number) => {
                return (
                  <TableAnimation
                    key={`${value.camera_ip}--${value.timestamp}--${value.uuid}`}
                  >
                    <TableUniformItem
                      data={value}
                      index={page * LIMIT_ITEM + index + 1}
                    />
                  </TableAnimation>
                );
              })}
            </div>
          </AnimatePresence>
        </Scrollbar>
      )}
    </>
  );
}
