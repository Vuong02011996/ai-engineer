import { cameraApi } from "@/api-client/camera";
import { EmptyData, Loading } from "@/components/common";
import Scrollbar from "@/components/common/scrollbar";
import { PaginationTable } from "@/components/pagination/pagination-search";
import { TableHead } from "@/components/table";
import { LIMIT_ITEM } from "@/constants/config";
import { useCameras } from "@/context/camera-context";
import tableHead from "@/data/camera";
import { usePaginationCustom } from "@/hooks/usePagination";
import { CameraRes } from "@/interfaces/camera";
import { formatCameraData } from "@/libs/camera";
import { useDebouncedValue } from "@mantine/hooks";
import { useSearchParams } from "next/navigation";
import { useCallback, useEffect, useState } from "react";
import { TableItemCamera } from "./table-item";

export interface ICameraTableProps {}

export function CameraTable(props: ICameraTableProps) {
  // ************** --init state-- *****************
  const { data, setData, total } = useCameras();
  const [isLoading, setLoading] = useState(true);
  const { maxPage, currentPage, setPage } = usePaginationCustom(
    total,
    LIMIT_ITEM
  );
  const searchParams = useSearchParams();
  const search = useCallback(() => {
    if (searchParams.has("search")) {
      return searchParams.get("search") || "";
    }
    return "";
  }, [searchParams]);
  const [debounce] = useDebouncedValue(search(), 500);

  // ************** --GET CAMERA-- *****************
  const getCamera = useCallback(async () => {
    try {
      let { data } = await cameraApi.getAll({
        page: currentPage,
        page_break: true,
        data_search: search().trim(),
      });
      let response: CameraRes[] = formatCameraData(data?.data);
      setData(response);
    } catch (error) {
      console.log(error);
    } finally {
      setLoading(false);
    }
  }, [currentPage, debounce]);

  // ************** --USE EFFECT GET CAMERA-- *****************
  useEffect(() => {
    getCamera();
  }, [getCamera]);

  useEffect(() => {
    if (debounce) {
      setPage("/camera", 1);
    }
  }, [debounce]);

  if (isLoading) return <Loading />;

  if (!data) return <EmptyData />;
  return (
    <div className="h-full ">
      <div className="h-calc60 overflow-auto">
        <Scrollbar>
          <TableHead dataHead={tableHead} />
          <div>
            {data.map((camera: CameraRes, index) => {
              return (
                <TableItemCamera
                  key={index}
                  camera={camera}
                  index={currentPage * LIMIT_ITEM + index + 1}
                  reload={getCamera}
                />
              );
            })}
          </div>
        </Scrollbar>
      </div>

      {/*  */}
      <PaginationTable
        total={total}
        currentPage={currentPage}
        currentCount={data.length}
        maxPage={maxPage}
        basePath={"/camera"}
      />
    </div>
  );
}
