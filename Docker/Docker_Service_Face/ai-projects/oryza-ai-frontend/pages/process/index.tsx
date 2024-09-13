import PaginateCustom from "@/components/pagination";
import HomeLayout from "@/layouts/home";
import { ProcessLayout } from "@/layouts/process";
import { useRouter } from "next/router";
import { useAuth } from "@/hooks/auth-hook";
export interface IProcessPageProps {}

export default function ProcessPage(props: IProcessPageProps) {
  const { profile } = useAuth();
  const router = useRouter();

  return profile?.is_admin ? (
    <ProcessLayout
      tabIndex={""}
      handleChangeTab={(tab) => {
        if (router.pathname != tab.path) router.push("/process/" + tab.path);
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
    </ProcessLayout>
  ) : null;
}

ProcessPage.Layout = HomeLayout;
