import { serviceTypeApi } from "@/api-client/setting";
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
import { SettingServiceDialog } from "@/components/dialog/create-setting-service";
import { ActionItem } from "@/components/file-action/item";
import { HeadContent } from "@/components/head/content-head";
import { PaginationTable } from "@/components/pagination/pagination-search";
import { TableHead } from "@/components/table";
import { LIMIT_ITEM } from "@/constants/config";
import { ResultEnum } from "@/constants/enum";
import { TableItemSettingService } from "@/containers";
import {
  TypeServiceProvider,
  useTypeService,
} from "@/context/service-type-context";
import tabData from "@/data/setting";
import tableHead from "@/data/type-server";
import useHandleError from "@/hooks/useHandleError";
import { usePaginationCustom } from "@/hooks/usePagination";
import { TypeServiceRes } from "@/interfaces/type-service";
import HomeLayout from "@/layouts/home";
import { formatTypeService } from "@/libs/format-data";
import { useDebouncedValue } from "@mantine/hooks";
import router from "next/router";
import { enqueueSnackbar } from "notistack";
import { useCallback, useEffect, useState } from "react";
import { useAuth } from "@/hooks/auth-hook";  

export interface ISettingServiceProps {}

function SettingService(props: ISettingServiceProps) {
  const { profile } = useAuth();
  // * * * * * * * * STATE * * * * * * * * * *
  const [openCreateDialog, setOpenCreateDialog] = useState(false);
  const { data, setData, total, setTotal, textSearch, setTextSearch } =
    useTypeService();
  const [isLoading, setLoading] = useState(true);
  const { maxPage, currentPage } = usePaginationCustom(total, LIMIT_ITEM);
  const handleError = useHandleError();
  const [debounced] = useDebouncedValue(textSearch, 500);

  // * * * * * * * * CREATE TYPE SERVICE * * * * * * * * * *
  const handleCreateService = async (formData: any) => {
    try {
      let payload = {
        ...formData,
        name: formData?.name.trim(),
        key: formData?.key.trim(),
      };
      await serviceTypeApi.create(payload);
      fetchData();
      setTotal(total + 1);
      enqueueSnackbar("Thêm mới cấu hình loại AI thành công", {
        variant: "success",
      });
      setOpenCreateDialog(false);
      return ResultEnum.success;
    } catch (error) {
      handleError(error, "Thêm mới cấu hình loại AI không thành công");
      return ResultEnum.error;
    }
  };

  // * * * * * * * * GET DATA * * * * * * * * * *
  const fetchData = useCallback(async () => {
    try {
      let { data } = await serviceTypeApi.getAll({
        page: currentPage,
        page_break: true,
        data_search: textSearch.trim(),
      });
      let response = formatTypeService(data?.data);
      setData(response);
    } catch (error) {
      console.log(error);
    } finally {
      setLoading(false);
    }
  }, [currentPage, debounced]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return profile?.is_admin ? (
    <section className="p-[24px] h-full">
      <SeoPage
        title="Cấu hình Loại AI"
        description="Tối ưu hóa và quản lý dịch vụ của bạn với trang Cấu hình Dịch vụ. Tìm kiếm hướng dẫn và tài liệu để điều chỉnh và tùy chỉnh dịch vụ theo nhu cầu cụ thể của doanh nghiệp của bạn."
      />
  
      <MainHead
        showFileAciton={false}
        searchValue={textSearch}
        onChange={setTextSearch}
      />
  
      <div className="h-calc50 shadow-shadown1 rounded-[16px] relative">
        {/* table title */}
        <HeadContent
          key="setting-service"
          title={"Cài đặt cấu hình"}
          tabData={tabData}
          tabIndex={"1"}
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
              {isLoading ? (
                <Loading />
              ) : data.length > 0 ? (
                <Scrollbar>
                  <TableHead dataHead={tableHead} />
                  {data.map((service: TypeServiceRes, index) => {
                    return (
                      <TableItemSettingService
                        data={service}
                        key={index}
                        index={currentPage * LIMIT_ITEM + index + 1}
                        reload={fetchData}
                      />
                    );
                  })}
                </Scrollbar>
              ) : (
                <EmptyData />
              )}
            </div>
  
            <PaginationTable
              total={total}
              currentPage={currentPage}
              currentCount={data.length}
              maxPage={maxPage}
              basePath={"/setting/service"}
            />
          </div>
        </OpactityAnimation>
      </div>
      <SettingServiceDialog
        open={openCreateDialog}
        handleClose={function (): void {
          setOpenCreateDialog(false);
        }}
        submit={handleCreateService}
      />
    </section>
  ) : null;
}
export default function SettingServicePage() {
  return (
    <TypeServiceProvider>
      <SettingService />
    </TypeServiceProvider>
  );
}

SettingServicePage.Layout = HomeLayout;
