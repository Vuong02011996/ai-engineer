import { cameraBrandApi } from "@/api-client/setting/camera-brand";
import addBlueIcon from "@/assets/svgs/add-blue.svg";
import gridIcon from "@/assets/svgs/grid.svg";
import listIcon from "@/assets/svgs/list.svg";
import { MainHead } from "@/components";
import {
  BigBtn,
  EmptyData,
  Loading,
  OpactityAnimation,
  SeoPage,
} from "@/components/common";
import Scrollbar from "@/components/common/scrollbar";
import { SettingCameraBrandDialog } from "@/components/dialog/create-setting-brand-camera";
import { ActionItem } from "@/components/file-action/item";
import { HeadContent } from "@/components/head/content-head";
import PaginateCustom from "@/components/pagination";
import { PaginationTable } from "@/components/pagination/pagination-search";
import { TableHead } from "@/components/table/table-head";
import { LIMIT_ITEM } from "@/constants/config";
import { ResultEnum } from "@/constants/enum";
import { TableItemSettingBrandCamera } from "@/containers/setting/camera-brand";
import headData from "@/data/camera-brand";
import tabData from "@/data/setting";
import useHandleError from "@/hooks/useHandleError";
import { usePaginationCustom } from "@/hooks/usePagination";
import { IBrandCamera } from "@/interfaces/brand-camera";
import HomeLayout from "@/layouts/home";
import { formatCameraBrand } from "@/libs/format-data";
import { useDebouncedValue } from "@mantine/hooks";
import router from "next/router";
import { enqueueSnackbar } from "notistack";
import { useCallback, useEffect, useState } from "react";
import { useAuth } from "@/hooks/auth-hook";
export interface ISettingBrandCameraProps {}

export default function SettingBrandCamera(props: ISettingBrandCameraProps) {
  const { profile } = useAuth();
  const [openCreateDialog, setOpenCreateDialog] = useState(false);

  const [data, setData] = useState<IBrandCamera[]>([]);
  const [textSearch, setTextSearch] = useState("");
  const [debounced] = useDebouncedValue(textSearch, 500);
  const [isLoading, setLoading] = useState(true);
  const [total, setTotal] = useState(1);
  const { maxPage, currentPage } = usePaginationCustom(total, LIMIT_ITEM);
  const handleError = useHandleError();

  const getCamera = useCallback(async () => {
    try {
      let { data } = await cameraBrandApi.getAll({
        page: currentPage,
        page_break: true,
        data_search: textSearch,
      });
      let response: IBrandCamera[] = formatCameraBrand(data?.data);
      setData(response);
    } catch (error) {
      console.log(error);
    } finally {
      setLoading(false);
    }
  }, [currentPage, debounced]);

  const getCount = async () => {
    try {
      let { data } = await cameraBrandApi.getCount({ data_search: textSearch });
      setTotal(Number(data?.count));
    } catch (error) {
      console.log(error);
    }
  };

  const handleCreate = async (formData: any) => {
    try {
      let payload = {
        name: formData?.name.trim(),
        key: formData?.key.trim(),
      };
      let res = await cameraBrandApi.create(payload);
      let response: IBrandCamera[] = formatCameraBrand([res?.data]);
      setData([response[0], ...data]);
      setTotal(total + 1);
      enqueueSnackbar("Thêm mới hãng camera thành công", {
        variant: "success",
      });
      return ResultEnum.success;
    } catch (error) {
      handleError(error, "Thêm mới hãng camera không thành công");
      return ResultEnum.error;
    }
  };

  useEffect(() => {
    getCamera();
  }, [getCamera]);

  useEffect(() => {
    getCount();
  }, [debounced]);

  return profile?.is_admin ? (
    <section className="p-[24px] h-full">
      <SeoPage title="Hãng Camera" />

      <MainHead
        showFileAciton={false}
        searchValue={textSearch}
        onChange={setTextSearch}
      />

      <div className="h-calc50 shadow-shadown1 rounded-[16px] relative">
        {/* table title */}
        <HeadContent
          key="managa"
          title={"Cài đặt cấu hình"}
          tabData={tabData}
          tabIndex={"5"}
          handleChangeTab={(tab) => {
            if (router.pathname != tab.path) router.push(tab.path);
          }}
          hiddenCreateBtn
          hiddenUpdateBtn
          tabChildren={
            <>
              <BigBtn
                text={"Tạo mới"}
                icon={addBlueIcon}
                className={
                  "bg-primary hover:bg-[#026DA6] text-white h-10 truncate"
                }
                classIcon="bg-white"
                onClick={() => setOpenCreateDialog(true)}
              />
            </>
          }
        />

        <OpactityAnimation className={"h-calc112 "}>
          <div className="flex-1 h-full pt-2">
            <div className="h-calc60 overflow-auto">
              <Scrollbar>
                <TableHead dataHead={headData} />
                {isLoading ? (
                  <>
                    <Loading></Loading>
                  </>
                ) : !data || data.length === 0 ? (
                  <EmptyData />
                ) : (
                  data.map((value: IBrandCamera, index) => {
                    return (
                      <TableItemSettingBrandCamera
                        data={value}
                        key={value.id}
                        index={currentPage * LIMIT_ITEM + index + 1}
                        reload={getCamera}
                        setTotal={() => setTotal(total - 1)}
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
              basePath={"/setting/brand-camera"}
            />
          </div>
        </OpactityAnimation>
      </div>
      <SettingCameraBrandDialog
        open={openCreateDialog}
        handleClose={() => setOpenCreateDialog(false)}
        submit={handleCreate}
      />
    </section>
  ) : null;
}
SettingBrandCamera.Layout = HomeLayout;
