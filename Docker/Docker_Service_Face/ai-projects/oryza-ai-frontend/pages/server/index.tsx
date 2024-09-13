import { serverApi } from "@/api-client/server";
import { MainHead } from "@/components";
import { OpactityAnimation, SeoPage } from "@/components/common";
import { CreateServerDialog } from "@/components/dialog/craete-server";
import { HeadContent } from "@/components/head/content-head";
import { ServerGrid } from "@/containers";
import SocketServer from "@/containers/server/socket";
import { ServerProvider, useServers } from "@/context/server-context";
import { useAuth } from "@/hooks/auth-hook";
import { useAppSelector } from "@/hooks/useReudx";
import HomeLayout from "@/layouts/home";
import { formatServerData } from "@/libs/server";
import { CreateServer } from "@/models/server";
import { enqueueSnackbar } from "notistack";
import { useEffect, useState } from "react";

export interface IServerPageProps {}

export function ServerComponents(props: IServerPageProps) {
  const { profile } = useAuth();

  const { setData, data } = useServers();
  const newData = useAppSelector((state) => state.server.server);
  const [textSearch, setTextSearch] = useState("");

  useEffect(() => {
    if (newData && textSearch.length == 0) {
      setData((prev) => {
        return prev.map((item) => {
          if (item.id === newData.id) {
            return {
              ...item,
              is_alive: Boolean(newData.is_alive),
            };
          }
          return item;
        });
      });
    }
  }, [newData]);

  const [open, setOpen] = useState(false);

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleCreateServer = (formData: any) => {
    let payload: CreateServer = {
      name: formData?.name.trim() ?? "",
      ip_address: formData?.ip_address.trim() ?? "",
    };
    serverApi
      .create(payload)
      .then((res) => {
        let response = formatServerData([res.data]);
        setData([response[0], ...data]);
        enqueueSnackbar("Tạo mới server thành công", { variant: "success" });
      })
      .catch((error: any) => {
        console.log("Errr", error);
        let errMsg =
          error?.response?.data?.detail ?? "Tạo mới server không thành công";
        enqueueSnackbar(errMsg, { variant: "error" });
      });
  };

  return profile?.is_superuser ? (
    <section className="p-[24px] h-full">
      <SeoPage title="Server" />
      {data.length > 0 && <SocketServer />}

      <MainHead searchValue={textSearch} onChange={setTextSearch} />

      <OpactityAnimation className="h-calc50 shadow-shadown1 rounded-[16px] relative overflow-hidden ">
        <HeadContent
          title={"Danh sách server"}
          onClickCreatebtn={handleClickOpen}
          hiddenCreateBtn={profile?.is_superuser !== true}
          hiddenUpdateBtn
          showType="GRID"
        />

        {/* table */}
        <div className="h-calc72">
          <ServerGrid search={textSearch} setSearch={setTextSearch} />
        </div>
      </OpactityAnimation>

      <CreateServerDialog
        open={open}
        handleClose={handleClose}
        submit={handleCreateServer}
      />
    </section>
  ) : null;
}

export default function ServerPage() {
  return (
    <ServerProvider>
      <ServerComponents />
    </ServerProvider>
  );
}
ServerPage.Layout = HomeLayout;
