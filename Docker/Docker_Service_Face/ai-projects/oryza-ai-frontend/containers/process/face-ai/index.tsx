import { TableAnimation } from "@/components";
import { EmptyData, Loading } from "@/components/common";
import Scrollbar from "@/components/common/scrollbar";
import { TableHead } from "@/components/table";
import { LIMIT_ITEM } from "@/constants/config";
import headData from "@/data/process/face-ai";
import { ProcessEvent } from "@/interfaces/process-page";
import { AnimatePresence } from "framer-motion";
import TableFaceAi from "./table-item";

export interface IFaceAiTableProps {
  loading: boolean;
  data: ProcessEvent[];
  page: any;
  reload: any;
}

export function FaceAiTable(props: IFaceAiTableProps) {
  const { loading, data, page } = props;
  return (
    <>
      {loading ? (
        <Loading />
      ) : !data || data.length === 0 ? (
        <EmptyData />
      ) : (
        <Scrollbar>
          <TableHead dataHead={headData} />
          <AnimatePresence initial={false}>
            {data.map((value: ProcessEvent, index: number) => {
              return (
                <TableAnimation key={`${value.id}`}>
                  <TableFaceAi
                    data={value}
                    index={page * LIMIT_ITEM + index + 1}
                    reload={props.reload}
                  />
                </TableAnimation>
              );
            })}
          </AnimatePresence>
        </Scrollbar>
      )}
    </>
  );
}
