import { serverApi } from "@/api-client/server";
import { EmptyData, Loading } from "@/components/common";
import Scrollbar from "@/components/common/scrollbar";
import { LIMIT_ITEM } from "@/constants/config";
import { useServers } from "@/context/server-context";
import { ServerRes } from "@/interfaces/server";
import { formatServerData } from "@/libs/server";
import { useDebouncedValue } from "@mantine/hooks";
import { Button } from "@mui/material";
import * as React from "react";
import { useEffect, useState } from "react";
import { ServerItem } from "./server-item";
import { useAppSelector } from "@/hooks/useReudx";

export interface IServerGridProps {
  search: string;
  setSearch: (search: string) => void;
}

export function ServerGrid(props: IServerGridProps) {
  // * * * * * * * * STATE * * * * * * * * * *
  const [isLoading, setIsLoading] = useState(true);
  const { data, setData } = useServers();
  const [total, setTotal] = useState(0);
  // * * * * * * * * SEARCH * * * * * * * * * *
  const [searchData, setSearchData] = useState<ServerRes[]>([]);
  // search by name & ip_address
  function handleSearch(searchKey: string) {
    return data.filter((item) => {
      const name = item.name.toLocaleLowerCase();
      const ip_address = item.ip_address.toLocaleLowerCase();
      const search = searchKey.toLocaleLowerCase();

      const searchName = name.includes(search);
      const searchIp = ip_address.includes(search);

      if (searchName || searchIp) return item;
    });
  }

  useEffect(() => {
    if (data.length <= 0) return;
    const searchData = handleSearch(props.search.trim());
    setSearchData(searchData);
  }, [props.search]);

  // * * * * * * * * GET DATA * * * * * * * * * *
  const fetchData = React.useCallback(async () => {
    setIsLoading(true);

    await serverApi
      .getAll({ page: 0, page_break: true })
      .then((res: any) => {
        let response = formatServerData(res.data?.data);
        setData(response);
      })
      .catch((error) => {})
      .finally(() => {
        setIsLoading(false);
      });
  }, []);

  // * * * * * * * * GET COUNT * * * * * * * * * *
  const handleGetTotal = async () => {
    serverApi.getTotal().then((res) => {
      setTotal(Number(res.data?.count ?? 0));
    });
  };

  // * * * * * * * * SOCKET SERVER INFO * * * * * * * * * *=
  const newInfo = useAppSelector((state) => state.server.info_server);
  useEffect(() => {
    if (newInfo) {
      setData((prev) => {
        return prev.map((item) => {
          if (item?.ip_address === newInfo?.ip) {
            console.log("INFO_SERVER: ", newInfo);
            return {
              ...item,
              serverInfo: newInfo,
            };
          }
          return item;
        });
      });
    }

    return () => {};
  }, [newInfo?.id]);

  useEffect(() => {
    handleGetTotal();
    fetchData();
  }, []);

  if (isLoading) return <Loading />;

  if (!data) return <EmptyData />;

  if (data.length === 0)
    return (
      <div className="h-full w-full flex items-center justify-center">
        <Button variant="contained" onClick={fetchData}>
          <p>làm mới</p>
        </Button>
      </div>
    );

  return (
    <div className="h-full  border-[#F2F2F2] border-t-2 ">
      <Scrollbar
        onScroll={(e) => {
          if (
            e.currentTarget.scrollHeight - e.currentTarget.scrollTop ===
            e.currentTarget.clientHeight
          ) {
            if (total <= data.length) return;
            serverApi
              .getAll({
                page: Math.ceil(data.length / LIMIT_ITEM),
                page_break: true,
              })
              .then((res: any) => {
                let response = formatServerData(res.data);
                setData([...data, ...response]);
              });
          }
        }}
      >
        {props.search.length > 0 ? (
          searchData.length <= 0 ? (
            <div className="w-full h-full">
              <EmptyData />
            </div>
          ) : (
            <div className="grid gap-[27px] xs:grid-cols-1 sm:grid-cols-1 md:grid-cols-2 tablet:grid-cols-2 laptop:grid-cols-3 desktop:grid-cols-4 p-8 ">
              {searchData.map((data: ServerRes, index) => (
                <ServerItem
                  key={index}
                  data={data}
                  reload={fetchData}
                  serverInfo={data?.serverInfo}
                />
              ))}
            </div>
          )
        ) : (
          <div className="grid gap-[27px] xs:grid-cols-1 sm:grid-cols-1 md:grid-cols-2 tablet:grid-cols-2 laptop:grid-cols-3 desktop:grid-cols-4 p-8 ">
            {data.map((data: ServerRes, index) => (
              <ServerItem
                key={index}
                data={data}
                reload={fetchData}
                serverInfo={data?.serverInfo}
              />
            ))}
          </div>
        )}
      </Scrollbar>
    </div>
  );
}
