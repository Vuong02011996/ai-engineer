import { serverApi } from "@/api-client/server";
import { serviceApi } from "@/api-client/service";
import Scrollbar from "@/components/common/scrollbar";
import PaginateCustom from "@/components/pagination";
import { TableHead } from "@/components/table";
import { useService } from "@/context/service-context";
import headData from "@/data/server-child";
import { usePaginationCustom } from "@/hooks/usePagination";
import { ServiceRes } from "@/interfaces/service";
import { formatServerData } from "@/libs/server";
import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import { TableItemCamera } from "./table-item";
import { EmptyData, Loading } from "@/components/common";
import { useAppSelector } from "@/hooks/useReudx";
import { LIMIT_ITEM } from "@/constants/config";
import { PaginationTable } from "@/components/pagination/pagination-search";

export interface IServerChildTableProps {}

export function ServerChildTable(props: IServerChildTableProps) {
  const { serverData, setServerData, data, setData, total } = useService();
  const { query } = useRouter();
  const [isLoading, setLoading] = useState(true);
  const { maxPage, currentPage } = usePaginationCustom(total, LIMIT_ITEM);

  const newData = useAppSelector((state) => state.server.service);

  useEffect(() => {
    if (newData) {
      setData((prev) => {
        return prev.map((item) => {
          if (item.id === newData.id) {
            return {
              ...item,
              is_alive: Boolean(newData.is_alive),
            };
          }
          return item;
        });
      });
    }
  }, [newData]);

  const getServer = () => {
    if (typeof query.id === "string") {
      serverApi
        .getById(query.id)
        .then((res) => {
          let server = formatServerData([res.data])[0];
          setServerData(server);
          getServiceByServer(server?.id ?? "");
        })
        .catch((error) => {
          console.log("Error ", error);
          setLoading(false);
        });
    } else {
    }
  };

  const getServiceByServer = (serverId: string) => {
    serviceApi
      .getByServer({ server_id: serverId, page: currentPage, page_break: true })
      .then((res) => {
        setData(res.data.data);
      })
      .catch((error) => {
        console.log("Error ", error);
      })
      .finally(() => {
        setLoading(false);
      });
  };

  useEffect(() => {
    getServer();
  }, [query, currentPage]);

  return (
    <div className="h-full ">
      <div className="h-calc60 overflow-auto  ">
        {isLoading ? (
          <Loading />
        ) : data.length === 0 ? (
          <EmptyData />
        ) : (
          <Scrollbar>
            <TableHead dataHead={headData} />
            {data.map((service: ServiceRes, index) => {
              return (
                <TableItemCamera
                  key={index}
                  data={service}
                  reload={() => getServiceByServer(serverData?.id ?? "")}
                  index={currentPage * LIMIT_ITEM + index + 1}
                />
              );
            })}
          </Scrollbar>
        )}
      </div>
      <PaginationTable
        total={total}
        currentPage={currentPage}
        currentCount={data.length}
        maxPage={maxPage}
        basePath={`/server/${query.id}`}
      />
    </div>
  );
}
