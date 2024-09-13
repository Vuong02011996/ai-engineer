import { cameraApi } from "@/api-client/camera";
import { MainHead } from "@/components";
import {
  EmptyData,
  Loading,
  OpactityAnimation,
  SeoPage,
} from "@/components/common";
import Scrollbar from "@/components/common/scrollbar";
import { HeadContent } from "@/components/head/content-head";
import { TableHead } from "@/components/table";
import { LIMIT_ITEM } from "@/constants/config";
import { CameraTableItem } from "@/containers/identification-profile/camera/table-item";
import tabData from "@/data/identification-profile";
import { cameraHeadData } from "@/data/identification-profile/camera";
import { useAuth } from "@/hooks/auth-hook";
import useHandleError from "@/hooks/useHandleError";
import { ICameraAI } from "@/interfaces/identification-profile/camera-ai";
import HomeLayout from "@/layouts/home";
import { formatCameraAi } from "@/libs/format-data";
import { useSearchParams } from "next/navigation";
import router from "next/router";
import * as React from "react";
import { useCallback, useEffect, useState } from "react";

export interface ICameraIdentificationProfileProps {}

export default function CameraIdentificationProfile(
  props: ICameraIdentificationProfileProps
) {
  const { profile } = useAuth();
  const [data, setData] = useState<ICameraAI[]>([]);
  const [loading, setLoading] = useState(true);

  const [total, setTotal] = useState(0);

  const searchParams = useSearchParams();

  const search = useCallback(() => {
    if (searchParams.has("search")) {
      return searchParams.get("search") || "";
    }
    return "";
  }, [searchParams]);

  const [searchData, setSearchData] = useState<ICameraAI[]>([]);
  const [searchKey, setSearchKey] = useState(search());

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
    const searchData = handleSearch(searchKey.trim());

    setSearchData(searchData);
  }, [data]);

  const handleGetData = React.useCallback(async () => {
    try {
      let { data } = await cameraApi.getCameraAi();

      const response = formatCameraAi(data, []);

      setData(response);
    } catch (error) {
    } finally {
      setLoading(false);
    }
  }, [profile?.company?.id]);

  useEffect(() => {
    handleGetData();
  }, [handleGetData]);

  return profile?.is_admin ? (
    <section className="p-[24px] h-full">
      <SeoPage title="Camera AI" />

      <MainHead
        searchValue={searchKey}
        onChange={(e) => {
          setSearchKey(e);

          //
          let query: any = { ...router.query, search: e };
          delete query["index"];

          router.replace({
            pathname: "/identification-profile/camera",
            query: query,
          });

          if (data.length <= 0) return;
          const searchData = handleSearch(e.trim());

          setSearchData(searchData);
        }}
      />

      <div className="h-calc50 shadow-shadown1 rounded-[16px] relative">
        {/* table title */}
        <HeadContent
          key="setting-company"
          title={"Danh sách hồ sơ nhận diện"}
          tabData={tabData}
          tabIndex={"2"}
          handleChangeTab={(tab) => {
            if (router.pathname != tab.path) router.push(tab.path);
          }}
          hiddenCreateBtn
          hiddenUpdateBtn
        />

        <OpactityAnimation className={"h-calc112"}>
          <div className="flex-1 h-full pt-2">
            <div className="h-full overflow-auto">
              <Scrollbar>
                <TableHead dataHead={cameraHeadData} />

                {loading ? (
                  <>
                    <Loading></Loading>
                  </>
                ) : !data || data.length === 0 ? (
                  <EmptyData />
                ) : (
                  (searchKey.length > 0 ? searchData : data).map(
                    (value: ICameraAI, index) => {
                      return (
                        <CameraTableItem
                          data={value}
                          key={value.id}
                          index={index + 1}
                          reload={handleGetData}
                          setTotal={() => setTotal(total - 1)}
                          currentPage={"1"}
                        />
                      );
                    }
                  )
                )}
              </Scrollbar>
            </div>
          </div>
        </OpactityAnimation>
      </div>
    </section>
  ) : null;
}

CameraIdentificationProfile.Layout = HomeLayout;
