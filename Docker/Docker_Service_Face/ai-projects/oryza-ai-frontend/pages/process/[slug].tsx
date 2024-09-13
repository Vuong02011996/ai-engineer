import { processApi } from "@/api-client/process";
import { PaginationTable } from "@/components/pagination/pagination-search";
import { LIMIT_ITEM } from "@/constants/config";
import SocketProcess from "@/containers/camera/socket/socket-process";
import { FaceAiTable } from "@/containers/process";
import { useProcessPage } from "@/context/process-page-context";
import { usePaginationCustom } from "@/hooks/usePagination";
import { useAppSelector } from "@/hooks/useReudx";
import { ProcessEvent } from "@/interfaces/process-page";
import HomeLayout from "@/layouts/home";
import { ProcessLayout } from "@/layouts/process";
import { formatProcessEvent } from "@/libs/format-data";
import { useDebouncedValue } from "@mantine/hooks";
import { useRouter } from "next/router";
import { useCallback, useEffect, useState } from "react";
import { useAuth } from "@/hooks/auth-hook";

function ProcessEventComponents() {
  const { profile } = useAuth();
  // ************** --init state-- *****************
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [total, setTotal] = useState(0);
  const [data, setData] = useState<ProcessEvent[]>([]);
  const { startTime, endTime, textSearch, filter } = useProcessPage();
  const [debounced] = useDebouncedValue(textSearch, 500);
  const { maxPage, currentPage } = usePaginationCustom(total, LIMIT_ITEM);

  const typeServiceId = useCallback(
    () => router?.query?.id as string,
    [router?.query?.id]
  );

  // * * * * * * * * SOCKET * * * * * * * *
  const newData = useAppSelector((state) => state.process.data);

  useEffect(() => {
    if (newData) {
      setData((prev) => {
        return prev.map((item) => {
          if (item.id === newData.id) {
            return {
              ...item,
              status: newData.status,
            };
          }
          return item;
        });
      });
    }
  }, [newData?.socketId]);

  // * * * * * * * * GET DATA * * * * * * * *
  const handleGetEventData = useCallback(async () => {
    let type_service_id = typeServiceId();
    if (typeof type_service_id !== "string") return;

    try {
      let { data } = await processApi.getProcessEvent(typeServiceId(), {
        type_service_id: typeServiceId(),
        page: currentPage,
        page_break: true,
        data_search: textSearch.trim(),
      });
      let response: ProcessEvent[] = formatProcessEvent(data);

      setData(response);
    } catch (error) {
      console.log("get data event Error :", error);
    } finally {
      setLoading(false);
    }
  }, [typeServiceId(), currentPage, debounced, startTime, endTime]);

  // * * * * * * * * GET COUNT * * * * * * * *
  async function getCount() {
    let type_service_id = typeServiceId();
    if (typeof type_service_id !== "string") return;

    try {
      let params = {
        type_service_id: typeServiceId(),
        data_search: textSearch.trim(),
      };
      let { data } = await processApi.getProcessEventCount(
        type_service_id,
        params
      );
      setTotal(Number(data));
    } catch (error) {
      console.log("get data event Error :", error);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    handleGetEventData();
    return setData([]);
  }, [handleGetEventData]);

  useEffect(() => {
    getCount();

    return setTotal(0);
  }, [typeServiceId, debounced, startTime, endTime, filter]);

  return profile?.is_admin ? (
    <>
      <SocketProcess />

      <div className="flex-1 h-full pt-2 ">
        <div className="h-calc60 overflow-auto">
          <FaceAiTable
            loading={loading}
            data={data}
            page={currentPage}
            reload={handleGetEventData}
          />
        </div>

        {/*  */}
        <PaginationTable
          total={total}
          currentPage={currentPage}
          currentCount={data.length}
          maxPage={maxPage}
          searchParams={{
            id: router?.query?.id,
          }}
          basePath={`/process/${router?.query?.slug}`}
        />
      </div>
    </>
  ) : null;
}

export default function ProcessEventPage() {
  const router = useRouter();
  const typeServiceId = useCallback(
    () => router?.query?.id as string,
    [router?.query?.id]
  );
  const { profile } = useAuth();

  return profile?.is_admin ? (
    <ProcessLayout
      tabIndex={typeServiceId()}
      handleChangeTab={(tab) => {
        if (router?.query?.slug != tab.path) {
          router.push({
            pathname: "/process/" + tab.path,
            query: { id: tab.id },
          });
        }
      }}
    >
      <ProcessEventComponents />
    </ProcessLayout>
  ) : null;
}

ProcessEventPage.Layout = HomeLayout;
