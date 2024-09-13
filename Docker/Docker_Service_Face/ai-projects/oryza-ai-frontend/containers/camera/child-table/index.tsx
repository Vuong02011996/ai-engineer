import Scrollbar from "@/components/common/scrollbar";
import { TableHead } from "@/components/table";
import headData from "@/data/camera-child";
import { TableItemCamera } from "./table-item";
import { useProcess } from "@/context/process-context";
import { PorcessRes } from "@/interfaces/process";

export interface ICameraChildTableProps {
  reload?: () => void;
}

export function CameraChildTable(props: ICameraChildTableProps) {
  const { data, searchData, searchKey } = useProcess();

  return (
    <div className="h-full ">
      <div className="h-full overflow-auto">
        <Scrollbar>
          <TableHead dataHead={headData} />
          {(searchKey.length > 0 ? searchData : data).map(
            (process: PorcessRes, index) => {
              return (
                <TableItemCamera
                  key={process.id}
                  index={index + 1}
                  data={process}
                  reload={props.reload}
                />
              );
            }
          )}
        </Scrollbar>
      </div>
    </div>
  );
}
