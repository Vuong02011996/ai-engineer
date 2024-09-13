import { companyApi } from "@/api-client/setting/company";
import { EmptyData, Loading } from "@/components/common";
import Scrollbar from "@/components/common/scrollbar";
import PaginateCustom from "@/components/pagination";
import { TableHead } from "@/components/table";
import { useSettingCompany } from "@/context/company-context";
import tableHead from "@/data/company";
import { usePaginationCustom } from "@/hooks/usePagination";
import { CompanyRes } from "@/interfaces/company";
import { formatCompanyData } from "@/libs/company";
import { useCallback, useEffect, useState } from "react";
import { TableItemSettingCompany } from "./table-item";
import { LIMIT_ITEM } from "@/constants/config";
import { PaginationTable } from "@/components/pagination/pagination-search";
import { useDebouncedValue } from "@mantine/hooks";

export interface ITableCompanyProps {}

export function TableCompany(props: ITableCompanyProps) {
  const { data, setData, total, textSearch } = useSettingCompany();
  const [isLoading, setLoading] = useState(true);
  const { maxPage, currentPage } = usePaginationCustom(total, LIMIT_ITEM);
  const [debounced] = useDebouncedValue(textSearch, 500);

  const getCamera = useCallback(async () => {
    try {
      let { data } = await companyApi.getAll({
        page: currentPage,
        page_break: true,
        data_search: textSearch,
      });
      let response: CompanyRes[] = formatCompanyData(data?.data);
      setData(response);
    } catch (error) {
      console.log(error);
    } finally {
      setLoading(false);
    }
  }, [currentPage, debounced]);

  useEffect(() => {
    getCamera();
  }, [getCamera]);

  if (isLoading) return <Loading />;
  if (!data) return <EmptyData />;

  return (
    <div className="flex-1 h-full pt-2">
      <div className="h-calc60 overflow-auto ">
        <Scrollbar>
          <TableHead dataHead={tableHead} />
          {data.map((company: CompanyRes, index) => {
            return (
              <TableItemSettingCompany
                data={company}
                key={index}
                index={currentPage * LIMIT_ITEM + index + 1}
                reload={getCamera}
              />
            );
          })}
        </Scrollbar>
      </div>

      {/*  */}
      <PaginationTable
        total={total}
        currentPage={currentPage}
        currentCount={data.length}
        maxPage={maxPage}
        basePath={"/setting/company"}
      />
    </div>
  );
}
