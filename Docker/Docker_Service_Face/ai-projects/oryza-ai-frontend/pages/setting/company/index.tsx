import { companyApi } from "@/api-client/setting/company";
import addBlueIcon from "@/assets/svgs/add-blue.svg";
import gridIcon from "@/assets/svgs/grid.svg";
import listIcon from "@/assets/svgs/list.svg";
import { MainHead } from "@/components";
import { BigBtn, OpactityAnimation, SeoPage } from "@/components/common";
import { CreateCompanyDialog } from "@/components/dialog/create-company";
import { ActionItem } from "@/components/file-action/item";
import { HeadContent } from "@/components/head/content-head";
import { ResultEnum } from "@/constants/enum";
import { NotifiMsg } from "@/constants/notifi-msg";
import { TableCompany } from "@/containers/setting/company";
import { CompanyProvider, useSettingCompany } from "@/context/company-context";
import tabData from "@/data/setting";
import useHandleError from "@/hooks/useHandleError";
import { CompanyRes } from "@/interfaces/company";
import HomeLayout from "@/layouts/home";
import { formatCompanyData } from "@/libs/company";
import { CreateCompany } from "@/models/company";
import router from "next/router";
import { enqueueSnackbar } from "notistack";
import { useState } from "react";
import { useAuth } from "@/hooks/auth-hook";

export interface ISettingCompanyProps {}

export function SettingCompany(props: ISettingCompanyProps) {
  const { profile } = useAuth();
  const [openCreateDialog, setOpenCreateDialog] = useState(false);
  const { data, setData, total, setTotal, textSearch, setTextSearch } =
    useSettingCompany();
  const handleError = useHandleError();

  const handleCreateCamera = async (formData: any) => {
    try {
      let payload: CreateCompany = {
        name: formData.name.trim(),
        domain: formData.domain.trim(),
      };

      let res = await companyApi.create(payload);
      let response: CompanyRes[] = formatCompanyData([res.data]);

      setData([response[0], ...data]);
      setTotal(total + 1);

      enqueueSnackbar(NotifiMsg.createCompany, { variant: "success" });
      return ResultEnum.success;
    } catch (error) {
      handleError(error, NotifiMsg.createCompanyErr);
      return ResultEnum.error;
    }
  };

  return profile?.is_admin ? (
    <section className="p-[24px] h-full">
      <SeoPage
        title="Công ty"
        description="Tối ưu hóa cấu trúc và thông tin công ty với trang Cấu hình Công ty. Cập nhật thông tin liên hệ và mô tả công ty của bạn một cách chuyên nghiệp để thu hút khách hàng."
      />
      <MainHead
        showFileAciton={false}
        searchValue={textSearch}
        onChange={setTextSearch}
      />

      <div className="h-calc50 shadow-shadown1 rounded-[16px] relative">
        {/* table title */}
        <HeadContent
          key="setting-company"
          title={"Cài đặt cấu hình"}
          tabData={tabData}
          tabIndex={"3"}
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
                  "bg-primary hover:bg-[#026DA6] text-white h-10 truncate "
                }
                classIcon="bg-white"
                onClick={() => setOpenCreateDialog(true)}
              />
            </>
          }
        />

        <OpactityAnimation className={"h-calc112"}>
          <TableCompany />
        </OpactityAnimation>
      </div>
      {/* dialog */}
      <CreateCompanyDialog
        open={openCreateDialog}
        handleClose={function (): void {
          setOpenCreateDialog(false);
        }}
        submit={handleCreateCamera}
      />
    </section>
  ) : null;
}

const CompanyPage = () => {
  return (
    <CompanyProvider>
      <SettingCompany />
    </CompanyProvider>
  );
};
export default CompanyPage;

CompanyPage.Layout = HomeLayout;
