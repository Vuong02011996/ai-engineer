import PaginateCustom from "@/components/pagination";
import HomeLayout from "@/layouts/home";
import { ManageLayout } from "@/layouts/manage";
import { useRouter } from "next/router";
export interface IFaceAiPageProps {}

export default function FaceAiPage(props: IFaceAiPageProps) {
  const router = useRouter();

  return (
    <ManageLayout
      tabIndex={""}
      handleChangeTab={(tab) => {
        if (router.pathname != tab.path) router.push("/manage/" + tab.path);
      }}
    >
      <div className="flex-1 h-full pt-2 ">
        <div className="h-calc60 overflow-auto"></div>

        {/*  */}
        <PaginateCustom
          maxPage={0}
          page={0}
          onChangePage={function (event: any, page: number): void {}}
          handlerSearchPage={undefined}
        />
      </div>
    </ManageLayout>
  );
}

FaceAiPage.Layout = HomeLayout;
