import { eventApi } from "@/api-client/event";
import { EmptyData } from "@/components/common";
import { PaginationTable } from "@/components/pagination/pagination-search";
import { LIMIT_ITEM } from "@/constants/config";
import { TypeServiceKey } from "@/constants/type-service";

// table components
import { TableCorwd } from "@/containers/manage/crowd";
import { FaceAiTable } from "@/containers/manage/face-ai";
import { TableLoitering } from "@/containers/manage/loitering";
import { TableTripwire } from "@/containers/manage/tripwire";
import { TableIllegalParking } from "@/containers/manage/illegal-parking";
import { TablePlateNumber } from "@/containers/manage/plate-number";
import { TableLaneViolation } from "@/containers/manage/lane-violation";  
import { TableForgotten } from "@/containers/manage/forgotten";
import { TableUniform } from "@/containers/manage/uniform";
import { TableTampering } from "@/containers/manage/tampering";
import { TableLeaving } from "@/containers/manage/leaving";
import { TableObjAttr } from "@/containers/manage/obj-attr";

import SocketEvent from "@/containers/server/socket/socket-event";
import { useManagement } from "@/context/manage-context";
import { usePaginationCustom } from "@/hooks/usePagination";
import { useAppSelector } from "@/hooks/useReudx";
import { EventData } from "@/interfaces/manage/event";
import HomeLayout from "@/layouts/home";
import { ManageLayout } from "@/layouts/manage";
import { formatEventData } from "@/libs/format-data";
import { useDebouncedValue } from "@mantine/hooks";
import moment from "moment";
import { useRouter } from "next/router";
import { useCallback, useEffect, useState } from "react";

import { LightTraffict } from "@/containers/manage/light-traffict";

function EventComponents() {
  // ************** --init state-- *****************
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [pageSlug, setPageSlug] = useState<string | undefined>();
  const [total, setTotal] = useState(0);
  const [data, setData] = useState<EventData[]>([]);
  const { startTime, endTime, textSearch, filter } = useManagement();
  const [debounced] = useDebouncedValue(textSearch, 500);
  const newData = useAppSelector((state) => state.event.data);
  const { maxPage, currentPage } = usePaginationCustom(total, LIMIT_ITEM);

  // * * * * * * * * LISTEN EVENT SOCKET * * * * * * * *
  useEffect(() => {
    if (!newData || currentPage !== 0 || textSearch !== "") return;
    if (newData?.type_service?.toUpperCase() === pageSlug?.toUpperCase()) {
      if (
        newData?.type_service?.toUpperCase() === TypeServiceKey.loitering ||
        newData?.type_service?.toUpperCase() === TypeServiceKey.illegal_parking
      )
      {
        if (newData?.type === "update") {
          setData((prev) => {
            return prev.map((item) => {
              if (item?.track_id === newData?.data?.track_id) {
                return {
                  ...item,
                  end_time: newData?.data?.end_time,
                  image_end: newData?.data?.image_end,
                  duration_time: newData?.data?.duration_time,
                  status: newData?.data?.status,
                };
              }
              return item;
            });
          });
          setTotal(total + 1);
        } else {
          setData((prev) => [newData.data, ...prev].splice(0, 20));
          setTotal(total + 1);
        }
      } else {
        setData((prev) => [newData.data, ...prev].splice(0, 20));
        setTotal(total + 1);
      }
    }
  }, [newData?.data]);

  // * * * * * * * * GET SLUG * * * * * * * *
  useEffect(() => {
    if (router?.query?.slug) {
      setPageSlug(router?.query?.slug as string);
    }
  }, [router?.query?.slug]);

  const typeServiceId = useCallback(
    () => router?.query?.id as string,
    [router?.query?.id]
  );

  // * * * * * * * * GET DATA * * * * * * * *
  const handleGetEventData = useCallback(async () => {
    let type_service_id = typeServiceId();
    if (typeof type_service_id !== "string") return;

    try {
      let { data } = await eventApi.getAll({
        page: currentPage,
        page_break: true,
        type_service_id: typeServiceId(),
        start_time: moment(startTime).format("yyyy-MM-DD HH:mm"),
        end_time: moment(endTime).format("yyyy-MM-DD HH:mm"),
        data_search: textSearch.trim(),
        filter: filter,
      });
      let response: EventData[] = formatEventData(data?.data, true);
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
        start_time: moment(startTime).format("yyyy-MM-DD HH:mm"),
        end_time: moment(endTime).format("yyyy-MM-DD HH:mm"),
        data_search: textSearch.trim(),
        filter: filter,
      };
      let { data } = await eventApi.getCount(params);
      setTotal(Number(data?.count));
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

  // * * * * * * * * RENDER TABEL * * * * * * * *
  const renderTable = () => {
    if (router.query.slug) {
      const type: string = router.query.slug as string;

      switch (type.toUpperCase()) {
        // TODO: Khuôn mặt
        case TypeServiceKey.FACE_RECOGNITION_EXCHANGES:
          return (
            <FaceAiTable loading={loading} data={data} page={currentPage} />
          );

        // TODO: Biển số
        case TypeServiceKey.plate_number:
          return (
            <TablePlateNumber
              loading={loading}
              data={data}
              page={currentPage}
            />
          );

        // TODO: Đám đông
        case TypeServiceKey.CROWD_DETECTION_EXCHANGES:
          return (
            <TableCorwd loading={loading} data={data} page={currentPage} />
          );
        // TODO: Lãng vãng
        case TypeServiceKey.loitering:
          return (
            <TableLoitering loading={loading} data={data} page={currentPage} />
          );
        case TypeServiceKey.tripwire:
          return (
            <TableTripwire loading={loading} data={data} page={currentPage} />
          );
        // TODO: Đồng phục
        case TypeServiceKey.IDENTIFY_UNIFORMS_EXCHANGES:
          return (
            <TableUniform loading={loading} data={data} page={currentPage} />
          );
        // TODO: Đồ vật bỏ quyên
        case TypeServiceKey.DETECT_ITEMS_FORGOTTEN_EXCHANGES:
          return (
            <TableForgotten loading={loading} data={data} page={currentPage} />
          );
        // TODO: Phá hoại
        case TypeServiceKey.CAMERA_TAMPERING_EXCHANGES:
          return (
            <TableTampering loading={loading} data={data} page={currentPage} />
          );
        // TODO: Đèn giao thông
        case TypeServiceKey.CAMERA_TRAFFIC_SIGNAL_EXCHANGES:
          return (
            <LightTraffict loading={loading} data={data} page={currentPage} />
          );
        // TODO: Đỗ xe vi phạm
        case TypeServiceKey.illegal_parking:
          return (
            <TableIllegalParking
              loading={loading}
              data={data}
              page={currentPage}
            />
          );
        case TypeServiceKey.lane_violation:
        case TypeServiceKey.line_violation:
        case TypeServiceKey.wrong_way:
          return (
            <TableLaneViolation
              loading={loading}
              data={data}
              page={currentPage}
            />
          );
        case TypeServiceKey.leaving:
        case TypeServiceKey.intrusion:
          return (
            <TableLeaving
              loading={loading}
              data={data}
              page={currentPage}
            />
          )
        case TypeServiceKey.obj_attr:
          return (
            <TableObjAttr
              loading={loading}
              data={data}
              page={currentPage}
            />
          )
          
        default:
          return <EmptyData />;
      }
    }
    return <EmptyData />;
  };

  return (
    <>
      <SocketEvent />

      <div className="flex-1 h-full pt-2 ">
        <div className="h-calc60 overflow-auto">{renderTable()}</div>

        {/*  */}
        <PaginationTable
          total={total}
          currentPage={currentPage}
          currentCount={data.length}
          maxPage={maxPage}
          searchParams={{
            id: router?.query?.id,
          }}
          basePath={`/manage/${router?.query?.slug}`}
        />
      </div>
    </>
  );
}

export default function EventPage() {
  const router = useRouter();
  const typeServiceId = useCallback(
    () => router?.query?.id as string,
    [router?.query?.id]
  );

  return (
    <ManageLayout
      tabIndex={typeServiceId()}
      handleChangeTab={(tab) => {
        if (router?.query?.slug != tab.path) {
          router.push({
            pathname: "/manage/" + tab.path,
            query: { id: tab.id },
          });
        }
      }}
    >
      <EventComponents />
    </ManageLayout>
  );
}

EventPage.Layout = HomeLayout;
