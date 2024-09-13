import { laneViolationApi } from "@/api-client/setting_ai_process";
import { MainHead } from "@/components";
import {
  EmptyData,
  Loading,
  OpactityAnimation,
  SeoPage,
} from "@/components/common";
import Scrollbar from "@/components/common/scrollbar";
import { HeadContent } from "@/components/head/content-head";
import { PaginationTable } from "@/components/pagination/pagination-search";
import { FilterComponents } from "@/components/popup/filter";
import { TableHead } from "@/components/table/table-head";
import { LIMIT_ITEM } from "@/constants/config";
import { LaneViolationTable } from "@/containers/identification-profile/lane-violation/table-item";
import tabData from "@/data/identification-profile";
import {
  laneViolationHead,
  optionFilterLaneViolation,
} from "@/data/identification-profile/lane-violation";
import { usePaginationCustom } from "@/hooks/usePagination";
import { CameraLaneViolation } from "@/interfaces/identification-profile/lane-violation";
import HomeLayout from "@/layouts/home";
import { formatLaneViolationData } from "@/libs/format-data";
import { useDebouncedValue } from "@mantine/hooks";
import router from "next/router";
import { useEffect, useState } from "react";
import { useAuth } from "@/hooks/auth-hook";
export interface IWrongWayPageProps {}

export default function WrongWayPage(props: IWrongWayPageProps) {
  const { profile } = useAuth();
  const [loading, setloading] = useState(false);
  const [data, setData] = useState<CameraLaneViolation[]>([]);
  const [total, setTotal] = useState(0);

  const { maxPage, currentPage, setPage } = usePaginationCustom(
    total,
    LIMIT_ITEM
  );

  const [filter, setFilter] = useState("ALL");
  const [textSearch, setTextSearch] = useState("");
  const [debounce] = useDebouncedValue(textSearch, 500);

  const hanldeGetAll = async () => {
    setloading(true);
    try {
      const params = {
        page: currentPage,
        page_break: true,
        filter: filter,
        data_search: textSearch,
      };
      const { data } = await laneViolationApi.getAllInfo(params);

      const response = formatLaneViolationData(data);
      setData(response);
    } catch (error) {
    } finally {
      setloading(false);
    }
  };

  const getCount = async () => {
    try {
      const params = {
        filter: filter,
        data_search: textSearch,
      };
      let { data } = await laneViolationApi.getCount(params);
      setTotal(Number(data));
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    hanldeGetAll();

    if (debounce) {
      setPage("/identification-profile/wrong-way", 1);
    }

    return () => {
      setData([]);
    };
  }, [filter, debounce, currentPage]);

  useEffect(() => {
    getCount();
  }, [filter, debounce]);

  return profile?.is_admin ? (
    <section className="p-[24px] h-full">
      <SeoPage title="Nhận diện hành vi đi ngược chiều" />

      <MainHead searchValue={textSearch} onChange={setTextSearch} />

      <div className="h-calc50 shadow-shadown1 rounded-[16px] relative">
        {/* table title */}
        <HeadContent
          key="setting-company"
          title={"Danh sách hồ sơ nhận diện"}
          tabData={tabData}
          tabIndex={"14"}
          handleChangeTab={(tab) => {
            if (router.pathname != tab.path) router.push(tab.path);
          }}
          hiddenCreateBtn
          hiddenUpdateBtn
          tabChildren={
            <FilterComponents
              options={optionFilterLaneViolation}
              value={filter}
              onChange={(e) => {
                setFilter(e);
                setPage("/identification-profile/wrong-way", 1);
              }}
            />
          }
        />

        <OpactityAnimation className={"h-calc112"}>
          <div className="flex-1 h-full pt-2">
            <div className="h-calc60 overflow-auto">
              <Scrollbar>
                <TableHead dataHead={laneViolationHead} />

                {loading ? (
                  <>
                    <Loading></Loading>
                  </>
                ) : !data || data.length === 0 ? (
                  <EmptyData />
                ) : (
                  data.map((value, index) => {
                    return (
                      <LaneViolationTable
                        data={value}
                        key={index}
                        index={currentPage * LIMIT_ITEM + index + 1}
                        reload={hanldeGetAll}
                      />
                    );
                  })
                )}
              </Scrollbar>
            </div>
            <PaginationTable
              total={total}
              currentPage={currentPage}
              currentCount={data.length}
              maxPage={maxPage}
              basePath={"/identification-profile/wrong-way"}
            />
          </div>
        </OpactityAnimation>
      </div>
    </section>
  ) : null;
}

WrongWayPage.Layout = HomeLayout;
