import { MainHead } from "@/components";
import { SeoPage } from "@/components/common";
import { HeadContent } from "@/components/head/content-head";
import tabData from "@/data/setting";
import * as React from "react";
import { useEffect, useState } from "react";
import HomeLayout from "./home";
import { useRouter } from "next/router";
export interface ISettingLayoutProps {
  children: React.ReactNode;
}

export default function SettingLayout(props: ISettingLayoutProps) {
  const { children } = props;

  const [tabIndex, setTabIndex] = useState("999");

  const router = useRouter();

  useEffect(() => {
    let tab = tabData.find((item) => item.path === router.pathname);
    if (tabIndex === tab?.id) return;
    if (tab) {
      setTabIndex(tab.id);
    }
  }, [router]);

  return (
    <HomeLayout>
      <section className="p-[24px] h-full">
        <SeoPage title="Cài đặt" />

        <MainHead />

        <div className="h-calc50 shadow-shadown1 rounded-[16px] relative">
          {/* table title */}
          <HeadContent
            title={"Quản lý"}
            tabData={tabData}
            tabIndex={tabIndex}
            handleChangeTab={(tab) => {
              setTabIndex(tab.id);
              if (router.pathname != tab.path) router.push(tab.path);
            }}
          />

          <div className={"h-calc112 "}>{children}</div>
        </div>
      </section>
    </HomeLayout>
  );
}
