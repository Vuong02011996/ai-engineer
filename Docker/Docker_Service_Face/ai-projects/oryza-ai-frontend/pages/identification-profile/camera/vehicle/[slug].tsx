import { MainHead } from "@/components";
import { OpactityAnimation, SeoPage } from "@/components/common";
import { HeadContent } from "@/components/head/content-head";
import { cameraSlugTabData } from "@/data/identification-profile/camera";
import HomeLayout from "@/layouts/home";
import router from "next/router";

export interface IVehicleCameraPageProps {}

export default function VehicleCameraPage(props: IVehicleCameraPageProps) {
  return (
    <section className="p-[24px] h-full">
      <SeoPage title="Nhận diện đối tượng" />

      <MainHead />

      <div className="h-calc50 shadow-shadown1 rounded-[16px] relative">
        {/* table title */}
        <HeadContent
          key="setting-company"
          title={"Danh sách hồ sơ nhận diện"}
          tabData={cameraSlugTabData}
          tabIndex={"2"}
          handleChangeTab={(tab) => {
            if (router.pathname != tab.path)
              router.replace(
                tab.path +
                  router?.query?.slug +
                  `?type_camera=${router.query?.type_camera}`
              );
          }}
          hiddenCreateBtn
          hiddenUpdateBtn
        />

        <OpactityAnimation className={"h-calc112"}>
          <div className="flex-1 h-full pt-2">
            <div className="h-calc92 overflow-auto">
              <div className="flex-1 h-full pt-2 flex items-center justify-center ">
                comming soon
              </div>
            </div>
          </div>
        </OpactityAnimation>
      </div>
    </section>
  );
}

VehicleCameraPage.Layout = HomeLayout;
