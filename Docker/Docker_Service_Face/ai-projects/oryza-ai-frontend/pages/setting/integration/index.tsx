"use client";
import { vmsApi } from "@/api-client/setting/vms";
import { MainHead } from "@/components";
import { OpactityAnimation, SeoPage } from "@/components/common";
import { LoadingPopup } from "@/components/common/loading/loading-popup";
import { HeadContent } from "@/components/head/content-head";
import { TitleBox } from "@/containers";
import { IntegrationFrom } from "@/containers/setting/integration/form";
import tabData from "@/data/setting";
import { VmsInterface } from "@/interfaces/vms";
import HomeLayout from "@/layouts/home";
import { Grid } from "@mui/material";
import Image from "next/image";
import router from "next/router";
import { useEffect, useState } from "react";
import { useAuth } from "@/hooks/auth-hook";

export interface ISettingIntegrationProps {}

export default function SettingIntegration(props: ISettingIntegrationProps) {
  const { profile } = useAuth();
  const [data, setData] = useState<VmsInterface | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    setLoading(true);
    try {
      let { data } = await vmsApi.getByCompany();

      setData(data);
    } catch (error) {
      //
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    return () => {
      setData(null);
    };
  }, []);

  return profile?.is_admin ? (
    <section className="p-[24px] h-full">
      <SeoPage title="Tích hợp" />

      <MainHead showFileAciton={false} />

      <div className="h-calc50 shadow-shadown1 rounded-[16px] relative">
        {/* table title */}
        <HeadContent
          key="managa"
          title={"Cài đặt cấu hình"}
          tabData={tabData}
          tabIndex={"6"}
          handleChangeTab={(tab) => {
            if (router.pathname != tab.path) router.push(tab.path);
          }}
          hiddenCreateBtn
          hiddenUpdateBtn
        />

        <OpactityAnimation className={"h-calc112 "}>
          <div className="flex-1 h-full  ">
            <TitleBox />
            <Grid container>
              <Grid item xs={12} lg={7}>
                {loading ? (
                  <LoadingPopup open={loading} />
                ) : (
                  <IntegrationFrom data={data} setData={setData} />
                )}
              </Grid>
              <Grid
                item
                xs={12}
                lg={5}
                p={"32px"}
                display={{ xs: "none", lg: "flex" }}
              >
                <Image
                  src="/images/imac.svg"
                  alt="imac"
                  width={200}
                  height={150}
                  style={{
                    width: "100%",
                    height: "100%",
                    objectFit: "contain",
                  }}
                />
              </Grid>
            </Grid>
          </div>
        </OpactityAnimation>
      </div>
    </section>
  ) : null;
}
SettingIntegration.Layout = HomeLayout;
