import { cameraApi } from "@/api-client/camera";
import { processApi } from "@/api-client/process";
import { MainHead } from "@/components";
import { OpactityAnimation, SeoPage } from "@/components/common";
import { CreateProcessDialog } from "@/components/dialog/create-process";
import { HeadContent } from "@/components/head/content-head";
import { ResultEnum } from "@/constants/enum";
import { CameraChildTable } from "@/containers/camera/child-table";
import SocketProcess from "@/containers/camera/socket/socket-process";
import { ProcessProvider, useProcess } from "@/context/process-context";
import useHandleError from "@/hooks/useHandleError";
import { useAppSelector } from "@/hooks/useReudx";
import { CameraRes } from "@/interfaces/camera";
import HomeLayout from "@/layouts/home";
import { formatCameraData } from "@/libs/camera";
import { formatProcess } from "@/libs/format-data";
import { useRouter } from "next/router";
import { enqueueSnackbar } from "notistack";
import { useEffect, useState } from "react";

export interface ICameraChildPageProps {}

function CameraChildPage(props: ICameraChildPageProps) {
  const { query } = useRouter();
  const {
    setCamera,
    camera,
    setData,
    data,
    setSearchData,
    searchKey,
    setSearchKey,
  } = useProcess();
  const handleError = useHandleError();

  const [openCreateDialog, setOpenCreateDialog] = useState(false);

  const newData = useAppSelector((state) => state.process.data);

  useEffect(() => {
    if (newData) {
      setData((prev) => {
        return prev.map((item) => {
          if (item.id === newData.id) {
            return {
              ...item,
              status: newData.status,
            };
          }
          return item;
        });
      });
    }
  }, [newData?.socketId]);

  function handleSearch(searchKey: string) {
    return data.filter((item) => {
      const serviceName = item.service.name.toLocaleLowerCase();
      const typeService = item.service.type_service.name.toLocaleLowerCase();
      const search = searchKey.toLocaleLowerCase();

      const searchName = serviceName.includes(search);
      const searchTypeService = typeService.includes(search);

      if (searchName || searchTypeService) return item;
    });
  }

  const getCamera = async () => {
    if (typeof query.id === "string") {
      try {
        const res = await cameraApi.getById(query.id);
        const camera: CameraRes = formatCameraData([res.data])[0];
        setCamera(camera);
        getProcessData(camera.id);
      } catch (error) {
        console.log("Error ", error);
      }
    }
  };

  const getProcessData = async (cameraId: string) => {
    processApi
      .getByCameraId(cameraId)
      .then((res) => {
        let response = formatProcess(res.data.data);
        setData(response);
      })
      .catch((error) => {
        console.log("Error: ", error);
      });
  };

  const handleCreateProcess = async (fomrData: any) => {
    if (typeof camera?.id !== "string") return ResultEnum.error;

    try {
      await processApi.create({ ...fomrData, camera_id: camera.id });
      getProcessData(camera?.id);
      enqueueSnackbar("Tạo mới process thành công", { variant: "success" });
      return ResultEnum.success;
    } catch (error) {
      handleError(error, "Tạo mới process không thành công");
      return ResultEnum.error;
    }
  };

  useEffect(() => {
    getCamera();
  }, [query.id]);

  return (
    <section className="p-[24px] h-full">
      <SeoPage title="Camera" />

      <SocketProcess />

      <MainHead
        searchValue={searchKey}
        onChange={(e) => {
          setSearchKey(e);
          if (data.length <= 0) return;
          const searchData = handleSearch(e.trim());
          setSearchData(searchData);
        }}
      />

      <div className="h-calc50 shadow-shadown1 rounded-[16px] relative overflow-hidden ">
        <HeadContent
          title={"Danh sách camera"}
          subTitle={camera?.name ?? "--"}
          rootPage="/camera"
          onClickCreatebtn={() => setOpenCreateDialog(true)}
        />

        {/* table */}
        <OpactityAnimation className="h-calc90 ">
          <CameraChildTable reload={() => getProcessData(camera?.id ?? "")} />
        </OpactityAnimation>
      </div>

      <CreateProcessDialog
        camera={camera}
        open={openCreateDialog}
        handleClose={function (): void {
          setOpenCreateDialog(false);
        }}
        submit={handleCreateProcess}
      />
    </section>
  );
}

export default function ProcessPage() {
  return (
    <ProcessProvider>
      <CameraChildPage />
    </ProcessProvider>
  );
}

ProcessPage.Layout = HomeLayout;
