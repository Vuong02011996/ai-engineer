import { loiteringApi } from "@/api-client/setting_ai_process";
import { MainHead } from "@/components";
import {
  EmptyData,
  Loading,
  OpactityAnimation,
  SeoPage,
} from "@/components/common";

import { tripwireHead } from "@/data/identification-profile/tripwire";

import Scrollbar from "@/components/common/scrollbar";
import { HeadContent } from "@/components/head/content-head";
import { PaginationTable } from "@/components/pagination/pagination-search";
import { FilterComponents } from "@/components/popup/filter";
import { TableHead } from "@/components/table/table-head";
import { LIMIT_ITEM } from "@/constants/config";
import { TripwireTable } from "@/containers/identification-profile/tripwire/table-item";
import tabData from "@/data/identification-profile";
import { optionFilterCrow } from "@/data/identification-profile/crowd";
import { usePaginationCustom } from "@/hooks/usePagination";
import { CameraLoiteringDetection } from "@/interfaces/identification-profile/loitering-detection";
import HomeLayout from "@/layouts/home";
import { formatLoiteringData } from "@/libs/format-data";
import { useDebouncedValue } from "@mantine/hooks";
import router from "next/router";
import { useEffect, useState } from "react";
import { useAuth } from "@/hooks/auth-hook";
import { TypeServiceKey } from "@/constants/type-service";

export interface IIntrusionProps {}

export default function Intrusion(props: IIntrusionProps) {
  const { profile } = useAuth();
  const [loading, setloading] = useState(false);
  const [data, setData] = useState<CameraLoiteringDetection[]>([]);
  const [total, setTotal] = useState(0);

  const { maxPage, currentPage, setPage } = usePaginationCustom(
    total,
    LIMIT_ITEM
  );

  const [filter, setFilter] = useState("ALL");
  const [textSearch, setTextSearch] = useState("");
  const [debounce] = useDebouncedValue(textSearch, 500);

  const handleGetAll = async () => {
    setloading(true);
    try {
      const params = {
        page: currentPage,
        page_break: true,
        filter: filter,
        data_search: textSearch,
        key_ai: TypeServiceKey.intrusion,
      };
      const { data } = await loiteringApi.getAllInfo(params);

      const response = formatLoiteringData(data);

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
        key_ai: TypeServiceKey.loitering,
      };
      let { data } = await loiteringApi.getCount(params);
      setTotal(Number(data));
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    handleGetAll();

    if (debounce) {
      setPage("/identification-profile/intrusion", 1);
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
      <SeoPage title="Nhận diện xâm nhập" />

      <MainHead searchValue={textSearch} onChange={setTextSearch} />

      <div className="h-calc50 shadow-shadown1 rounded-[16px] relative">
        {/* table title */}
        <HeadContent
          key="setting-company"
          title={"Danh sách hồ sơ nhận diện"}
          tabData={tabData}
          tabIndex={"15"}
          handleChangeTab={(tab) => {
            if (router.pathname != tab.path) router.push(tab.path);
          }}
          hiddenCreateBtn
          hiddenUpdateBtn
          tabChildren={
            <FilterComponents
              options={optionFilterCrow}
              value={filter}
              onChange={(e) => {
                setFilter(e);
                setPage("/identification-profile/intrusion", 1);
              }}
            />
          }
        />

        <OpactityAnimation className={"h-calc112"}>
          <div className="flex-1 h-full pt-2">
            <div className="h-calc60 overflow-auto">
              <Scrollbar>
                <TableHead dataHead={tripwireHead} />

                {loading ? (
                  <>
                    <Loading></Loading>
                  </>
                ) : !data || data.length === 0 ? (
                  <EmptyData />
                ) : (
                  data.map((value, index) => {
                    return (
                      <TripwireTable
                        data={value}
                        key={index}
                        index={currentPage * LIMIT_ITEM + index + 1}
                        reload={handleGetAll}
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
              basePath={"/identification-profile/intrusion"}
            />
          </div>
        </OpactityAnimation>
      </div>
    </section>
  ) : null;
}

Intrusion.Layout = HomeLayout;
