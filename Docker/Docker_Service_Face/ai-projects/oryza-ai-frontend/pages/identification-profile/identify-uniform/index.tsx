import { uniformApi } from "@/api-client/identification-profile/uniform";
import { MainHead } from "@/components";
import {
  BigBtn,
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
import { UniformTable } from "@/containers/identification-profile/uniform/table-item";
import tabData from "@/data/identification-profile";
import { optionFilterCrow } from "@/data/identification-profile/crowd";
import { uniformHead } from "@/data/identification-profile/uniform";
import { usePaginationCustom } from "@/hooks/usePagination";
import { CameraCrowd } from "@/interfaces/identification-profile/crowd";
import HomeLayout from "@/layouts/home";
import { formatLoiteringData } from "@/libs/format-data";
import { useDebouncedValue } from "@mantine/hooks";
import router from "next/router";
import { useEffect, useState } from "react";
import addBlueIcon from "@/assets/svgs/add-blue.svg";
import updateIcon from "@/assets/svgs/update-icon-black.svg";
import { SettingCompanyUniformDialog } from "@/components/dialog/config-ai-uniform/setting-uniform-company";
import { ResultEnum } from "@/constants/enum";
import { enqueueSnackbar } from "notistack";
import { useAuth } from "@/hooks/auth-hook";
export interface IIdentifyUniformProps {}

export default function IdentifyUniform(props: IIdentifyUniformProps) {
  const { profile } = useAuth();
  // ************** --state-- *****************
  const [loading, setloading] = useState(false);
  const [data, setData] = useState<CameraCrowd[]>([]);
  const [total, setTotal] = useState(0);
  const [openSettingCompany, setOpenSettingCompany] = useState(false);
  const { maxPage, currentPage, setPage } = usePaginationCustom(
    total,
    LIMIT_ITEM
  );
  const [filter, setFilter] = useState("ALL");
  const [textSearch, setTextSearch] = useState("");
  const [debounce] = useDebouncedValue(textSearch, 500);
  const [companySettingData, setCompanySettingData] = useState<any>(null);

  // ************** --HANDLE GET ALL-- *****************
  const hanldeGetAll = async () => {
    setloading(true);
    try {
      const params = {
        page: currentPage,
        page_break: true,
        filter: filter,
        data_search: textSearch,
      };
      const { data } = await uniformApi.getAllInfo(params);

      const response = formatLoiteringData(data);
      setData(response);
    } catch (error) {
    } finally {
      setloading(false);
    }
  };

  // ************** --GET COUNT-- *****************
  const getCount = async () => {
    try {
      const params = {
        filter: filter,
        data_search: textSearch,
      };
      let { data } = await uniformApi.getCount(params);
      setTotal(Number(data));
    } catch (error) {
      console.log(error);
    }
  };

  // ************** --GET COMPANY SETTING UNIFORM-- *****************
  const getCompanySettingUniform = async () => {
    try {
      const params = {};
      let { data } = await uniformApi.getALlUniformConfig(params);
      setCompanySettingData(data);
    } catch (error) {
      console.log(error);
    }
  };
  // ************** --HANDLE SETTING UNIFORM-- *****************
  const handleSettingComanyUniform = async (formData: any) => {
    try {
      if (companySettingData === null) {
        await uniformApi.createSettingUniform(formData);
      } else {
        const formJson = Object.fromEntries(formData.entries());
        const id = companySettingData.id;
        if (formJson.rgb !== companySettingData?.rgb) {
          await uniformApi.updateSettingCompanyRgb(id, {
            rgb: formJson.rgb,
          });
        }
      }
      const msg = `Cập nhật cài đặt màu sắc đồng phục thành công`;
      enqueueSnackbar(msg, { variant: "success" });
      return ResultEnum.success;
    } catch (error) {
      const msg = `Cập nhật cài đặt màu sắc đồng phục không thành công`;
      enqueueSnackbar(msg, { variant: "error" });
      return ResultEnum.error;
    }
  };

  // ************** --USE EFFECT-- *****************
  useEffect(() => {
    hanldeGetAll();

    if (debounce) {
      setPage("/identification-profile/identify-uniform", 1);
    }

    return () => {
      setData([]);
    };
  }, [filter, debounce, currentPage]);

  useEffect(() => {
    getCount();
  }, [filter, debounce]);

  useEffect(() => {
    if (openSettingCompany === false) {
      getCompanySettingUniform();
    }
  }, [openSettingCompany]);

  return profile?.is_admin ? (
    <section className="p-[24px] h-full">
      <SeoPage title="Nhận diện đồng phục" />

      <MainHead searchValue={textSearch} onChange={setTextSearch} />

      <div className="h-calc50 shadow-shadown1 rounded-[16px] relative">
        {/* table title */}
        <HeadContent
          key="setting-company"
          title={"Danh sách hồ sơ nhận diện"}
          tabData={tabData}
          tabIndex={"7"}
          handleChangeTab={(tab) => {
            if (router.pathname != tab.path) router.push(tab.path);
          }}
          hiddenCreateBtn
          hiddenUpdateBtn
          tabChildren={
            <>
              <FilterComponents
                options={optionFilterCrow}
                value={filter}
                onChange={(e) => {
                  setFilter(e);
                  setPage("/identification-profile/identify-uniform", 1);
                }}
              />
              {companySettingData ? (
                <BigBtn
                  text={"Chỉnh sửa"}
                  icon={updateIcon}
                  className={
                    "bg-[#FFAC47] hover:bg-[#FE991E] text-black h-10 truncate"
                  }
                  classIcon=""
                  onClick={() => setOpenSettingCompany(true)}
                />
              ) : (
                <BigBtn
                  text={"Tạo mới"}
                  icon={addBlueIcon}
                  className={
                    "bg-primary hover:bg-[#026DA6] text-white h-10 truncate"
                  }
                  classIcon="bg-white"
                  onClick={() => setOpenSettingCompany(true)}
                />
              )}
            </>
          }
        />

        <OpactityAnimation className={"h-calc112"}>
          <div className="flex-1 h-full pt-2">
            <div className="h-calc60 overflow-auto">
              <Scrollbar>
                <TableHead dataHead={uniformHead} />

                {loading ? (
                  <>
                    <Loading></Loading>
                  </>
                ) : !data || data.length === 0 ? (
                  <EmptyData />
                ) : (
                  data.map((value, index) => {
                    return (
                      <UniformTable
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
              basePath={"/identification-profile/identify-uniform"}
            />
          </div>
        </OpactityAnimation>
      </div>
      <SettingCompanyUniformDialog
        open={openSettingCompany}
        handleClose={function (): void {
          setOpenSettingCompany(false);
        }}
        submit={handleSettingComanyUniform}
        data={companySettingData}
      />
    </section>
  ) : null;
}

IdentifyUniform.Layout = HomeLayout;
