import gridIcon from "@/assets/svgs/grid.svg";
import listIcon from "@/assets/svgs/list.svg";
import { MainHead } from "@/components";
import { OpactityAnimation, SeoPage } from "@/components/common";
import { ActionItem } from "@/components/file-action/item";
import { HeadContent } from "@/components/head/content-head";
import {
  ProcessPageProvider,
  useProcessPage,
} from "@/context/process-page-context";
import * as React from "react";

export interface IProcessLayoutProps {
  children: React.ReactNode;
  tabIndex: string;
  handleChangeTab: (tab: any) => void;
}

const ProcessComponents = (props: IProcessLayoutProps) => {
  const { tabData, textSearch, setTextSearch } = useProcessPage();

  return (
    <section className="p-[24px] h-full">
      <SeoPage title="Quản lý tiến trình" />

      <MainHead searchValue={textSearch} onChange={setTextSearch} />

      <div className="h-calc50 shadow-shadown1 rounded-[16px] relative">
        <HeadContent
          key="manage"
          title={"Danh sách tiến trình"}
          tabData={tabData}
          tabIndex={props.tabIndex}
          handleChangeTab={(v) => {
            props.handleChangeTab(v);
            setTextSearch("");
          }}
          hiddenCreateBtn
          hiddenUpdateBtn
          // tabChildren={
          //   <div className="flex flex-row space-x-3">
          //     <div className="flex flex-row p-[4px] rounded-[8px] bg-[#F2F2F2]">
          //       <ActionItem active={false} onClick={() => {}} icon={gridIcon} />
          //       <ActionItem active={true} onClick={() => {}} icon={listIcon} />
          //     </div>
          //   </div>
          // }
        />

        <OpactityAnimation className={"h-calc112  "}>
          {props.children}
        </OpactityAnimation>
      </div>
    </section>
  );
};
export function ProcessLayout(props: IProcessLayoutProps) {
  return (
    <ProcessPageProvider>
      <ProcessComponents
        children={props.children}
        tabIndex={props.tabIndex}
        handleChangeTab={props.handleChangeTab}
      />
    </ProcessPageProvider>
  );
}
