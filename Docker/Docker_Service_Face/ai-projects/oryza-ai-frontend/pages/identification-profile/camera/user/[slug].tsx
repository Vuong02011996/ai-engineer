"use client";
import { cameraApi } from "@/api-client/camera";
import { personApi } from "@/api-client/identification-profile/person";
import { personCameraApi } from "@/api-client/identification-profile/person-camera";
import { serviceApi } from "@/api-client/service";
import { MainHead } from "@/components";
import {
  EmptyData,
  Loading,
  OpactityAnimation,
  SeoPage,
} from "@/components/common";
import { LoadingPopup } from "@/components/common/loading/loading-popup";
import Scrollbar from "@/components/common/scrollbar";
import { HeadContent } from "@/components/head/content-head";
import { PaginationTable } from "@/components/pagination/pagination-search";
import { FilterSmallIcon } from "@/components/popup/filter/filter-small-icon";
import { TableHead } from "@/components/table";
import { LIMIT_ITEM } from "@/constants/config";
import { CameraSlugTableItem } from "@/containers/identification-profile/camera/table-slug-item";
import {
  cameraSlugHeadData,
  cameraSlugTabData,
} from "@/data/identification-profile/camera";
import { filterPersonByCamera } from "@/data/identification-profile/filter-option";
import { useAuth } from "@/hooks/auth-hook";
import { usePaginationCustom } from "@/hooks/usePagination";
import { CameraRes } from "@/interfaces/camera";
import { PersonCompanyCamera } from "@/interfaces/identification-profile/person";
import HomeLayout from "@/layouts/home";
import { formatCameraData, formatServiceToCamera } from "@/libs/camera";
import { useDebouncedValue } from "@mantine/hooks";
import { useRouter } from "next/router";
import { enqueueSnackbar } from "notistack";
import clsx from "clsx";
import * as React from "react";
import { useEffect, useState } from "react";

export interface ICameraSlugIdentificationProfileProps {}

export default function CameraSlugIdentificationProfile(
  props: ICameraSlugIdentificationProfileProps
) {
  const router = useRouter();
  const { profile } = useAuth();
  const [data, setData] = useState<PersonCompanyCamera[]>([]);
  const [loading, setLoading] = useState(true);
  const [total, setTotal] = useState(0);
  const { maxPage, currentPage } = usePaginationCustom(total, LIMIT_ITEM);
  const [camera, setCamera] = useState<CameraRes | null>(null);
  const [textSearch, setTextSearch] = useState("");
  const [debounce] = useDebouncedValue(textSearch, 500);
  const [filter, setFilter] = useState<"NO_SETTING" | "SETTING" | "ALL">("ALL");

  // * * * * * * * * * * * * * * * *

  const [isSync, setIsSync] = useState(false);
  const [action, setAction] = useState<null | "create" | "delete">(null);

  const checkMultiplePersonCamera = async (notifiMsg?: string) => {
    if (!router.query?.slug) return;

    try {
      const { data } = await personCameraApi.checkMultiplePersonCamera(
        router.query?.slug as string
      );

      setIsSync(data.status);
      setAction(data.action);

      if (data.status) {
        setTimeout(() => checkMultiplePersonCamera(notifiMsg), 3000);
      } else {
        handleGetData(notifiMsg);
      }
    } catch (error) {
      console.error("Error calling API:", error);
      setTimeout(() => checkMultiplePersonCamera(notifiMsg), 3000);
    }
  };
  useEffect(() => {
    checkMultiplePersonCamera();
  }, [router.query?.slug]);

  // * * * * * * * * FETCH DATA * * * * * * * * *
  const handleGetData = React.useCallback(
    async (notifiMsg?: string) => {
      const companyId = profile?.company?.id || "";
      if (!companyId || !router.query?.slug) return;
      setLoading(true);

      try {
        const params = {
          id_camera: router.query?.slug as string,
          page: currentPage,
          page_break: true,
          data_search: textSearch,
          filter: filter,
        };

        const { data } = await personApi.getPersionByCompanyCamera(params);
        setData(data);
        if (notifiMsg) {
          enqueueSnackbar(notifiMsg, {
            variant: "success",
          });
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setLoading(false);
      }
    },
    [profile?.company?.id, currentPage, router.query?.slug, debounce, filter]
  );

  // * * * * * * * * GET COUNT * * * * * * * * *
  const handleGetCount = React.useCallback(async () => {
    let companyId = profile?.company.id ?? "";
    if (!companyId) return;
    try {
      let { data } = await personApi.getCount({ data_search: "" }, companyId);
      setTotal(Number(data));
    } catch (error) {}
  }, [profile?.company?.id]);

  // * * * * * * * * GET CAMERA BY ID * * * * * * * * *
  const getCameraById = React.useCallback(async () => {
    const { slug, type_camera } = router?.query || {};
    if (!slug || !type_camera) return;

    const fetchCameraData = async (fetchFunc: any, formatFunc: any) => {
      try {
        let { data } = await fetchFunc(slug as string);
        const camera: CameraRes = formatFunc([data])[0];
        setCamera(camera);
      } catch (error) {
        console.error("Fetch error", error);
      }
    };

    if (type_camera === "CameraAI") {
      await fetchCameraData(cameraApi.getById, formatCameraData);
    } else if (type_camera === "ServiceAI") {
      await fetchCameraData(serviceApi.getInfoById, formatServiceToCamera);
    }
  }, [router?.query]);

  // * * * * * * * * USE EFFECT * * * * * * * * *
  useEffect(() => {
    handleGetCount();
  }, []);

  useEffect(() => {
    handleGetData();
  }, [handleGetData]);

  useEffect(() => {
    getCameraById();
  }, [getCameraById]);

  // * * * * * * * * CHECK ALL * * * * * * * * *
  const [checkedIds, setCheckedIds] = useState<string[]>([]);

  const handleCheckALl = (checked: boolean) => {
    if (checked) {
      setCheckedIds(data.map((i) => i.id));
    } else {
      setCheckedIds([]);
    }
  };

  const handleCheck = (value: string, checked: boolean) => {
    if (checked) {
      setCheckedIds((prev) => [...prev, value]);
    } else {
      setCheckedIds((prev) => prev.filter((i) => i !== value));
    }
  };

  // * * * * * * * * CREATE ALL USER CAMERA * * * * * * * * *
  const [loadingCreate, setloadingCreate] = useState(false);
  const hanleCreateMultipleUserCamera = async () => {
    setloadingCreate(true);
    try {
      const { slug } = router?.query || {};

      await personCameraApi.createMultiplePersonCamera(slug as string);
      checkMultiplePersonCamera("Giám sát tất cả đối tượng thành công");
    } catch (error) {
      enqueueSnackbar("Giám sát tất cả đối tượng không thành công", {
        variant: "error",
      });
    } finally {
      setloadingCreate(false);
    }
  };

  const handleRemoveMultipleUserCamera = async () => {
    setloadingCreate(true);
    try {
      const { slug } = router?.query || {};

      await personCameraApi.removeMultiplePersonCamera(slug as string);
      checkMultiplePersonCamera("Hủy giám sát tất cả đối tượng thành công");
    } catch (error) {
      console.log("Create multiple person camera error:", error);
      enqueueSnackbar("Hủy giám sát tất cả đối tượng không thành công", {
        variant: "error",
      });
    } finally {
      setloadingCreate(false);
    }
  };

  return (
    <section className="p-[24px] h-full">
      <SeoPage title="Nhận diện đối tượng" />

      <MainHead searchValue={textSearch} onChange={setTextSearch} />

      <LoadingPopup open={loadingCreate} />

      <div className="h-calc50 shadow-shadown1 rounded-[16px] relative">
        {/* table title */}
        <HeadContent
          key="setting-company"
          title={"Nhận diện bởi"}
          tabIndex={"1"}
          tabData={cameraSlugTabData}
          handleChangeTab={(tab) => {
            if (router.pathname != tab.path)
              router.replace(
                tab.path +
                  router?.query?.slug +
                  `?type_camera=${router.query?.type_camera}`
              );
          }}
          hiddenCreateBtn
          hiddenUpdateBtn
          subTitleApostrophe={camera?.name ?? ""}
          rootPage="/identification-profile/camera"
          tabChildren={
            <div className="-translate-y-3 items-center flex space-x-3 ">
              <button
                disabled={isSync}
                onClick={hanleCreateMultipleUserCamera}
                className={clsx(
                  "shadow-shadown1 p-2 rounded-lg min-w-24 bg-white  transition-all duration-200",
                  "disabled:opacity-60 disabled:cursor-not-allowed"
                )}
              >
                <p className="text-grayOz text-center font-semibold text-[14px]">
                  Giám sát tất cả
                </p>
              </button>
              <button
                disabled={isSync}
                onClick={handleRemoveMultipleUserCamera}
                className={clsx(
                  "shadow-shadown1 p-2 rounded-lg min-w-24 bg-redDark  transition-all duration-200",
                  "disabled:opacity-60 disabled:cursor-not-allowed"
                )}
              >
                <p className="text-white text-center font-semibold text-[14px]">
                  Hủy tất cả
                </p>
              </button>
              <FilterSmallIcon
                options={filterPersonByCamera}
                onChange={(e) => {
                  setFilter(e);
                }}
              />
            </div>
          }
        ></HeadContent>

        <OpactityAnimation className={"h-calc72"}>
          <div className="flex-1 h-full">
            <div className="overflow-auto h-calc92">
              {camera && (
                <Scrollbar>
                  <TableHead
                    dataHead={cameraSlugHeadData}
                    hanleCheckAll={handleCheckALl}
                  />

                  {loading ? (
                    <>
                      <Loading />
                    </>
                  ) : !data || data.length === 0 ? (
                    <EmptyData />
                  ) : (
                    data.map((value: PersonCompanyCamera, index) => {
                      return (
                        <CameraSlugTableItem
                          data={value}
                          key={value.id}
                          index={currentPage * LIMIT_ITEM + index + 1}
                          updateState={(is_supervision: boolean) => {
                            setData((prevData) =>
                              prevData.map((item) =>
                                item.id === value.id
                                  ? { ...item, is_supervision: is_supervision }
                                  : item
                              )
                            );
                          }}
                          setTotal={() => setTotal(total - 1)}
                          isOn={value.is_supervision}
                          camera={camera}
                          handleCheck={handleCheck}
                          checkedIds={checkedIds}
                          loading={isSync}
                          action={action}
                        />
                      );
                    })
                  )}
                </Scrollbar>
              )}
            </div>
            <PaginationTable
              total={total}
              currentPage={currentPage}
              currentCount={data.length}
              maxPage={maxPage}
              basePath={`/identification-profile/camera/user/${router?.query?.slug}`}
              searchParams={{
                type_camera: router.query?.type_camera,
              }}
            />
          </div>
        </OpactityAnimation>
      </div>
    </section>
  );
}

CameraSlugIdentificationProfile.Layout = HomeLayout;
