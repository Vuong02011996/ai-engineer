import { MainHead } from "@/components";
import { SeoPage } from "@/components/common";
import { OpactityAnimation } from "@/components/common/animations";
import Scrollbar from "@/components/common/scrollbar";
import { HeadContent } from "@/components/head/content-head";
import PaginateCustom from "@/components/pagination";
import { FilterComponents } from "@/components/popup/filter";
import { FilterSmallIcon } from "@/components/popup/filter/filter-small-icon";
import { TableHead } from "@/components/table";
import { TableItemHistory } from "@/containers/history";
import { PickTimeHistory } from "@/containers/history/pick-time";
import tableHead, {
  optionActionHistory,
  optionFilterHistory,
} from "@/data/history";
import HomeLayout from "@/layouts/home";

export interface IHistoryPageProps {}

export default function HistoryPage(props: IHistoryPageProps) {
  return (
    <div className="p-[24px] h-full">
      <SeoPage title="Lịch sử" />
      <MainHead />
      <div className="h-calc50 shadow-shadown1 rounded-[16px] relative overflow-hidden ">
        <HeadContent title={"Lịch sử hoạt động"} hiddenCreateBtn>
          <FilterSmallIcon
            options={optionActionHistory}
            onChange={function (value: any): void {}}
          />
          <FilterComponents options={optionFilterHistory} />
          <PickTimeHistory />
        </HeadContent>
        <OpactityAnimation className="h-calc72">
          <div className="flex-1 h-full">
            <TableHead dataHead={tableHead} />
            <div className="h-calc92 overflow-auto">
              <Scrollbar>
                {[...Array(50)].map((data: any, index) => {
                  return (
                    <TableItemHistory
                      key={index}
                      data={undefined}
                      index={index + 1}
                      reload={function (): void {}}
                    />
                  );
                })}
              </Scrollbar>
            </div>

            {/*  */}
            <PaginateCustom
              maxPage={0}
              page={0}
              onChangePage={function (event: any, page: number): void {}}
              handlerSearchPage={undefined}
            />
          </div>
        </OpactityAnimation>
      </div>
    </div>
  );
}
HistoryPage.Layout = HomeLayout;
