import { MainHead } from "@/components";
import Scrollbar from "@/components/common/scrollbar";
import { SettingRoleDialog } from "@/components/dialog/create-setting-role";
import { ActionItem } from "@/components/file-action/item";
import { HeadContent } from "@/components/head/content-head";
import { TableHead } from "@/components/table";
import { TableItemSettingRole } from "@/containers/setting/role";
import { getColumns } from "@/data/role";
import tabData from "@/data/setting";
import HomeLayout from "@/layouts/home";
import router from "next/router";
import gridIcon from "@/assets/svgs/grid.svg";
import listIcon from "@/assets/svgs/list.svg";
import addBlueIcon from "@/assets/svgs/add-blue.svg";
import {
  BigBtn,
  EmptyData,
  Loading,
  OpactityAnimation,
  SeoPage,
} from "@/components/common";
import { usePaginationCustom } from "@/hooks/usePagination";
import { LIMIT_ITEM } from "@/constants/config";
import { UserProvider, useUser } from "@/context/user-context";
import { useCallback, useEffect, useState } from "react";
import { userApi } from "@/api-client/setting/user";
import { formatUser } from "@/libs/format-data";
import { UserRes } from "@/interfaces/user";
import { PaginationTable } from "@/components/pagination/pagination-search";
import useHandleError from "@/hooks/useHandleError";
import { enqueueSnackbar } from "notistack";
import { ResultEnum } from "@/constants/enum";
import { useAuth } from "@/hooks/auth-hook";
import { useDebouncedValue } from "@mantine/hooks";

export interface ISettingUserProps {}

function SettingRole(props: ISettingUserProps) {
  const [openCreateDialog, setOpenCreateDialog] = useState(false);
  const { data, setData, total, setTotal, textSearch, setTextSearch } =
    useUser();
  const [debounced] = useDebouncedValue(textSearch, 500);
  const [isLoading, setLoading] = useState(true);
  const { maxPage, currentPage } = usePaginationCustom(total, LIMIT_ITEM);
  const [columns, setColumns] = useState<any>([]);

  const { profile } = useAuth();
  useEffect(() => {
    if (!profile?.id) return;
    const userRole = profile.is_superuser
      ? "SUPERUSER"
      : profile.is_admin
      ? "ADMIN"
      : "USER";

    setColumns(getColumns(userRole));
  }, [profile?.id, profile?.is_admin, profile?.is_superuser]);

  // const columns = getColumns(userRole);
  const handleError = useHandleError();

  const handleCreateRole = async (formData: any) => {
    try {
      let payload = {
        username: formData?.username.trim(),
        password: formData?.password.trim(),
        email: formData?.email.trim(),
        is_admin: formData?.is_admin,
        is_active: formData?.is_active,
        company_id: formData?.company,
        avatar: formData?.avatar,
      };

      await userApi.create(payload);
      fetchData();
      setTotal(total + 1);
      enqueueSnackbar("Tạo mới người dùng thành công", { variant: "success" });
      setOpenCreateDialog(false);
      return ResultEnum.success;
    } catch (error) {
      console.log(error);
      handleError(error, "Thêm mới người dùng thất bại");
      return ResultEnum.error;
    }
  };

  const fetchData = useCallback(async () => {
    try {
      let { data } = await userApi.getAll({
        page: currentPage,
        page_break: true,
        data_search: textSearch.trim(),
      });
      let response: UserRes[] = formatUser(data?.data);
      setData(response);
    } catch (error) {
      console.log(error);
    } finally {
      setLoading(false);
    }
  }, [currentPage, debounced, setData, textSearch]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return profile?.is_admin ? (
    <section className="p-[24px] h-full">
      <SeoPage
        title="Phân quyền"
        description="Tinh chỉnh quyền hạn và truy cập với trang Cấu hình Phân quyền. Quản lý và điều chỉnh quyền truy cập vào tính năng và dữ liệu của hệ thống một cách linh hoạt và an toàn nhất."
      />
      <MainHead
        showFileAciton={false}
        searchValue={textSearch}
        onChange={setTextSearch}
      />

      <div className="h-calc50 shadow-shadown1 rounded-[16px] relative">
        {/* table title */}
        <HeadContent
          key="seting-role"
          title={"Cài đặt cấu hình"}
          tabData={tabData}
          tabIndex={"4"}
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
                  <TableHead dataHead={columns} />
                  {data.map((service: UserRes, index) => {
                    return (
                      <TableItemSettingRole
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
              basePath={"/setting/role"}
            />
          </div>
        </OpactityAnimation>
      </div>
      <SettingRoleDialog
        open={openCreateDialog}
        handleClose={function (): void {
          setOpenCreateDialog(false);
        }}
        submit={handleCreateRole}
      />
    </section>
  ) : null;
}

export default function SettingRolePage() {
  return (
    <UserProvider>
      <SettingRole />
    </UserProvider>
  );
}

SettingRolePage.Layout = HomeLayout;
