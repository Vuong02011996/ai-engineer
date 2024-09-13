import { webhookApi } from "@/api-client/setting/webhook";
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
import { SettingWebhookDialog } from "@/components/dialog/create-setting-webhook";
import { ActionItem } from "@/components/file-action/item";
import { HeadContent } from "@/components/head/content-head";
import { PaginationTable } from "@/components/pagination/pagination-search";
import { TableHead } from "@/components/table";
import { LIMIT_ITEM } from "@/constants/config";
import { ResultEnum } from "@/constants/enum";
import { TableItemSettingWebhook } from "@/containers/setting/webhook";
import { WebhookProvider, useWebhook } from "@/context/webhook-context";
import tabData from "@/data/setting";
import tableHead from "@/data/webhook";
import useHandleError from "@/hooks/useHandleError";
import { usePaginationCustom } from "@/hooks/usePagination";
import { WebhookRes } from "@/interfaces/webhook";
import HomeLayout from "@/layouts/home";
import { formatWebhook } from "@/libs/format-data";
import { useDebouncedValue } from "@mantine/hooks";
import router from "next/router";
import { enqueueSnackbar } from "notistack";
import { useCallback, useEffect, useState } from "react";
import { useAuth } from "@/hooks/auth-hook";
export interface ISettingWebHookProps {}

function SettingWebHook(props: ISettingWebHookProps) {
  const { profile } = useAuth();
  // * * * * * * * * STATE * * * * * * * * * *
  const [openCreateDialog, setOpenCreateDialog] = useState(false);
  const { data, setData, total, setTotal, textSearch, setTextSearch } =
    useWebhook();
  const [isLoading, setLoading] = useState(true);
  const { maxPage, currentPage } = usePaginationCustom(total, LIMIT_ITEM);

  const [debounced] = useDebouncedValue(textSearch, 500);
  const handleError = useHandleError();

  const fetchData = useCallback(async () => {
    try {
      let { data } = await webhookApi.getAll({
        page: currentPage,
        page_break: true,
        data_search: textSearch,
      });
      let response: WebhookRes[] = formatWebhook(data?.data);
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

  const handleCreateWebhook = async (formData: any) => {
    try {
      let payload = {
        ...formData,
        status: true,
        name: formData?.name.trim(),
        endpoint: formData?.endpoint.trim(),
        token: formData?.token.trim(),
        auth_type: formData?.auth_type.trim(),
      };
      let res = await webhookApi.create(payload);
      let response: WebhookRes[] = formatWebhook([res?.data]);
      setData([response[0], ...data]);
      setTotal(total + 1);
      enqueueSnackbar("Thêm mới cấu hình webhook thành công", {
        variant: "success",
      });
      return ResultEnum.success;
    } catch (error: any) {
      handleError(error, "Thêm mới cấu hình webhook không thành công");
      return ResultEnum.error;
    }
  };

  return profile?.is_admin ? (
    <section className="p-[24px] h-full">
      <SeoPage
        title="Cấu hình Webhook"
        description="Kết nối và tùy chỉnh webhook của bạn với trang Cấu hình Webhook. Tìm hiểu cách tích hợp và điều chỉnh webhook một cách dễ dàng và linh hoạt nhất cho ứng dụng của bạn."
      />
      <MainHead
        showFileAciton={false}
        searchValue={textSearch}
        onChange={setTextSearch}
      />

      <div className="h-calc50 shadow-shadown1 rounded-[16px] relative">
        {/* table title */}
        <HeadContent
          key="setting-webhook"
          title={"Cài đặt cấu hình"}
          tabData={tabData}
          tabIndex={"2"}
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
            <div className="h-calc60 overflow-auto    ">
              {isLoading ? (
                <Loading />
              ) : data.length > 0 ? (
                <Scrollbar>
                  <TableHead dataHead={tableHead} />
                  {data.map((service: WebhookRes, index) => {
                    return (
                      <TableItemSettingWebhook
                        data={service}
                        key={service.id}
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
              basePath={"/setting/webhook"}
            />
          </div>
        </OpactityAnimation>
      </div>
      <SettingWebhookDialog
        open={openCreateDialog}
        handleClose={function (): void {
          setOpenCreateDialog(false);
        }}
        submit={handleCreateWebhook}
      />
    </section>
  ) : null;
}

export default function SettingWebHookPage() {
  return (
    <WebhookProvider>
      <SettingWebHook />
    </WebhookProvider>
  );
}

SettingWebHookPage.Layout = HomeLayout;
