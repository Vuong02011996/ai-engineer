import { personApi } from "@/api-client/identification-profile/person";
import addBlueIcon from "@/assets/svgs/add-blue.svg";
import gridIcon from "@/assets/svgs/grid.svg";
import listIcon from "@/assets/svgs/list.svg";
import { MainHead } from "@/components";
import {
  BigBtn,
  EmptyData,
  OpactityAnimation,
  SeoPage,
} from "@/components/common";
import { LoadingPopup } from "@/components/common/loading/loading-popup";
import Scrollbar from "@/components/common/scrollbar";
import { IdentificationUserDialog } from "@/components/dialog/create-identification-user";
import { ActionItem } from "@/components/file-action/item";
import { HeadContent } from "@/components/head/content-head";
import { PaginationTable } from "@/components/pagination/pagination-search";
import { TableHead } from "@/components/table";
import { LIMIT_ITEM } from "@/constants/config";
import { ResultEnum } from "@/constants/enum";
import { UserTableItem } from "@/containers/identification-profile/user/table-item";
import tabData, { headData } from "@/data/identification-profile";
import { useAuth } from "@/hooks/auth-hook";
import useHandleError from "@/hooks/useHandleError";
import { usePaginationCustom } from "@/hooks/usePagination";
import { IPerson } from "@/interfaces/identification-profile/person";
import HomeLayout from "@/layouts/home";
import { formatPerson } from "@/libs/format-data";
import { useDebouncedValue } from "@mantine/hooks";
import clsx from "clsx";
import { AnimatePresence } from "framer-motion";
import { useSearchParams } from "next/navigation";
import router from "next/router";
import { enqueueSnackbar } from "notistack";
import * as React from "react";
import { useCallback, useEffect, useState } from "react";

export default function UserIdentificationProfile() {
  // ************** --init state-- *****************
  const [openCreate, setOpenCreate] = useState(false);
  const handleError = useHandleError();
  const { profile } = useAuth();
  const [data, setData] = useState<IPerson[]>([]);
  const [loading, setLoading] = useState(true);
  const [total, setTotal] = useState(0);
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
  const [viewType, setViewType] = useState<"LIST" | "GRID">("LIST");

  // ************** --on change view type-- *****************
  const onChangeViewType = (type: "LIST" | "GRID") => {
    // TODO: change view type
    setViewType(type);

    localStorage.setItem("identification-profile_view_type", type);
  };

  useEffect(() => {
    if (typeof window === "undefined") return;

    const type = localStorage.getItem("identification-profile_view_type");
    if (type === "LIST" || type === "GRID") {
      onChangeViewType(type);
    }
  }, []);

  // ************** --Handle Create-- *****************
  const handleCreate = async (formData: any) => {
    try {
      await personApi.create(formData);

      handleGetData();
      setTotal(total + 1);
      enqueueSnackbar("Thêm mới hồ sơ nhận diện đối tượng thành công ", {
        variant: "success",
      });
      return ResultEnum.success;
    } catch (error) {
      handleError(error, "Thêm mới hồ sơ nhận diện đối tượng không thành công");
      return ResultEnum.error;
    }
  };

  // ************** --Get data-- *****************
  const handleGetData = React.useCallback(async () => {
    let companyId = profile?.company?.id ?? "";

    if (!companyId) return;
    setLoading(true);
    try {
      let params = {
        page: currentPage,
        page_break: true,
        data_search: search(),
      };

      let { data } = await personApi.getByCompany(params, companyId);
      let response: IPerson[] = formatPerson(data);
      setData(response);
    } catch (error) {
    } finally {
      setLoading(false);
    }
  }, [profile?.company?.id, currentPage, debounce]);

  // ************** --Get Count-- *****************
  const handleGetCount = React.useCallback(async () => {
    let companyId = profile?.company?.id ?? "";
    if (!companyId) return;
    try {
      let { data } = await personApi.getCount(
        { data_search: search() },
        companyId
      );
      setTotal(Number(data));
    } catch (error) {}
  }, [profile?.company?.id, debounce]);

  // ************** --Use Effect-- *****************
  useEffect(() => {
    handleGetData();
  }, [handleGetData]);

  useEffect(() => {
    handleGetCount();
  }, [handleGetCount]);

  useEffect(() => {
    if (debounce) {
      setPage("/identification-profile/user", 1);
    }
  }, [debounce]);

  const handleSearch = (search: string) => {
    let query: any = { ...router.query, search: search };
    delete query["index"];

    router.replace({
      pathname: "/identification-profile/user",
      query: query,
    });
  };

  return profile?.is_admin ? (
    <section className="p-[24px] h-full">
      <SeoPage title="Nhận diện đối tượng" />

      <MainHead searchValue={search()} onChange={handleSearch} />

      <LoadingPopup open={loading} />

      <div className="h-calc50 shadow-shadown1 rounded-[16px] relative">
        {/* table title */}
        <HeadContent
          key="setting-company"
          title={"Danh sách hồ sơ nhận diện"}
          tabData={tabData}
          tabIndex={"1"}
          handleChangeTab={(tab) => {
            if (router.pathname != tab.path) router.push(tab.path);
          }}
          hiddenCreateBtn
          hiddenUpdateBtn
          tabChildren={
            <>
              <div className="flex flex-row p-[4px] rounded-[8px] bg-[#F2F2F2]">
                <ActionItem
                  active={viewType === "GRID"}
                  onClick={() => onChangeViewType("GRID")}
                  icon={gridIcon}
                />
                <ActionItem
                  active={viewType === "LIST"}
                  onClick={() => onChangeViewType("LIST")}
                  icon={listIcon}
                />
              </div>
              <BigBtn
                text={"Tạo mới"}
                icon={addBlueIcon}
                onClick={() => setOpenCreate(true)}
                className={
                  "bg-primary hover:bg-[#026DA6] text-white h-10 truncate "
                }
                classIcon="bg-white"
              />
            </>
          }
        />

        <OpactityAnimation className={"h-calc112"}>
          <div className="flex-1 h-full pt-2">
            <div className="h-calc60 overflow-auto">
              <Scrollbar>
                {viewType === "LIST" && <TableHead dataHead={headData} />}

                <AnimatePresence initial={false}>
                  <div
                    className={clsx(
                      viewType === "GRID" && "grid-cols-1 grid",
                      viewType === "GRID" && "px-7 py-5 gap-10",
                      viewType === "GRID" && "xs:grid-cols-1",
                      viewType === "GRID" && "sm:grid-cols-2",
                      viewType === "GRID" && "md:grid-cols-3",
                      viewType === "GRID" && "tablet:grid-cols-4",
                      viewType === "GRID" && "laptop:grid-cols-5",
                      viewType === "GRID" && "desktop:grid-cols-6"
                    )}
                  >
                    {!data || data.length === 0 ? (
                      <EmptyData />
                    ) : (
                      data.map((value: IPerson, index) => {
                        return (
                          <UserTableItem
                            data={value}
                            key={value.id}
                            index={currentPage * LIMIT_ITEM + index + 1}
                            reload={handleGetData}
                            setTotal={() => setTotal(total - 1)}
                            viewType={viewType}
                          />
                        );
                      })
                    )}
                  </div>
                </AnimatePresence>
              </Scrollbar>
            </div>
            <PaginationTable
              total={total}
              currentPage={currentPage}
              currentCount={data.length}
              maxPage={maxPage}
              basePath={"/identification-profile/user"}
            />
          </div>
        </OpactityAnimation>
      </div>

      {/* create dialog */}
      <IdentificationUserDialog
        open={openCreate}
        handleClose={() => setOpenCreate(false)}
        submit={handleCreate}
      />
    </section>
  ) : null;
}

UserIdentificationProfile.Layout = HomeLayout;
