import { serviceApi } from "@/api-client/service";
import { MainHead } from "@/components";
import { OpactityAnimation, SeoPage } from "@/components/common";
import { CreateServiceDialog } from "@/components/dialog/create-service";
import { HeadContent } from "@/components/head/content-head";
import { ServerChildTable } from "@/containers/server/child-table";
import SocketService from "@/containers/server/socket/socket-service";
import { ServiceProvider, useService } from "@/context/service-context";
import HomeLayout from "@/layouts/home";
import { useRouter } from "next/router";
import { enqueueSnackbar } from "notistack";
import { useState } from "react";

export interface IServerChildPageProps {}

function ServerChildPage(props: IServerChildPageProps) {
  const [openCreateServiceDialog, setOpenCreateServiceDialog] = useState(false);
  const { serverData, data, setData, total, setTotal } = useService();

  const { query } = useRouter();

  const handleCreateService = (formData: any) => {
    if (typeof query.id !== "string") return;
    let payload = {
      ...formData,
      server_id: query.id,
      name: formData?.name.trim(),
    };
    serviceApi
      .create(payload)
      .then((res: any) => {
        setData([res.data, ...data]);
        setTotal(total + 1);
        enqueueSnackbar("Tạo mới service thành công", { variant: "success" });
      })
      .catch((error) => {
        const errorMsg =
          error?.response?.data?.detail || "Tạo mới service không thành công";
        enqueueSnackbar(errorMsg, { variant: "error" });
      });
  };

  return (
    <section className="p-[24px] h-full">
      <SeoPage title="Server" />

      {data.length > 0 && <SocketService />}

      <MainHead />

      <div className="h-calc50 shadow-shadown1 rounded-[16px] relative overflow-hidden ">
        <HeadContent
          title={"Danh sách server"}
          subTitle={serverData?.name || ""}
          rootPage="/server"
          onClickCreatebtn={() => setOpenCreateServiceDialog(true)}
        />

        {/* table */}
        <OpactityAnimation className="h-calc72 ">
          <ServerChildTable />
        </OpactityAnimation>
      </div>

      <CreateServiceDialog
        open={openCreateServiceDialog}
        handleClose={function (): void {
          setOpenCreateServiceDialog(false);
        }}
        submit={handleCreateService}
      />
    </section>
  );
}

export default function ServicePage() {
  return (
    <ServiceProvider>
      <ServerChildPage />
    </ServiceProvider>
  );
}

ServicePage.Layout = HomeLayout;
