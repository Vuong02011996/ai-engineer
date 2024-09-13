import { cameraApi } from "@/api-client/camera";
import { MainHead } from "@/components";
import { SeoPage } from "@/components/common";
import { OpactityAnimation } from "@/components/common/animations";
import { CreateCameraDialog } from "@/components/dialog/create-camera";
import { HeadContent } from "@/components/head/content-head";
import { ResultEnum } from "@/constants/enum";
import { CameraTable } from "@/containers";
import { CameraProvider, useCameras } from "@/context/camera-context";
import useHandleError from "@/hooks/useHandleError";
import { CameraRes } from "@/interfaces/camera";
import HomeLayout from "@/layouts/home";
import { formatCameraData } from "@/libs/camera";
import { CreateCamera } from "@/models/camera";
import { useSearchParams } from "next/navigation";
import { useRouter } from "next/router";
import { enqueueSnackbar } from "notistack";
import { useCallback, useState } from "react";
import { useAuth } from "@/hooks/auth-hook";

export interface ICameraPageProps {}

const CameraComponents = (props: ICameraPageProps) => {
  const { profile } = useAuth();
  /**
   * Destructures setData and data from useCameras hook.
   * Destructures profile from useAuth hook.
   * Initializes state for open with useState, defaulting to false.
   */
  const { setData, data, setTotal, total } = useCameras();
  const router = useRouter();
  const [open, setOpen] = useState(false);
  const handleError = useHandleError();
  const searchParams = useSearchParams();

  const search = useCallback(() => {
    if (searchParams.has("search")) {
      return searchParams.get("search") || "";
    }
    return "";
  }, [searchParams]);

  /**
   * Sets the state of open to true.
   */
  const handleClickOpen = () => {
    setOpen(true);
  };

  /**
   * Sets the state of open to false.
   */
  const handleClose = () => {
    setOpen(false);
  };

  /* 
    This function handles the search input and updates the query parameters in the URL accordingly.
    @param {string} search - The search term entered by the user.
    Steps:
    1. Create a copy of the current query parameters from the router.
    2. If the search term is not empty, add/update the 'search' parameter in the query.
    3. If the search term is empty, remove the 'search' parameter from the query.
    4. Replace the current URL with the updated query parameters, navigating to the '/camera' route.
  */
  const handleSearch = (search: string) => {
    let query: any = { ...router.query, search: search };
    delete query["index"];

    router.replace({
      pathname: "/camera",
      query: query,
    });
  };

  /**
   * Function to handle the creation of a camera.
   * @param formData The form data for creating the camera.
   */
  const handleCreateCamera = async (formData: any) => {
    try {
      let payload: CreateCamera = {
        ip_address: formData?.ip_address.trim() ?? "",
        name: formData?.name.trim() ?? "",
        password: formData?.password.trim() ?? "",
        rtsp: formData?.rtsp.trim() ?? "",
        username: formData?.username.trim() ?? "",
        is_ai: formData?.is_ai ?? false,
        brand_camera_id: formData?.brand_camera_id ?? "",
        type_service_ids: formData?.type_service_ids ?? [],
        other_info: formData?.other_info ?? "",
        ward_id: formData?.ward_id ?? "",
      };
      if (formData?.port && formData?.port !== "") {
        payload.port = Number(formData?.port);
      }
      let res = await cameraApi.create(payload);
      let response: CameraRes[] = formatCameraData([res.data]);
      enqueueSnackbar("Thêm camera thành công", { variant: "success" });
      setData([response[0], ...data]);
      setTotal(total + 1);

      return ResultEnum.success;
    } catch (error) {
      handleError(error, "Thêm mới cấu hình webhook không thành công");
      return ResultEnum.error;
    }
  };

  return profile?.is_admin ? (
    <section className="p-[24px] h-full">
      <SeoPage title="Camera" />

      <MainHead searchValue={search()} onChange={handleSearch} />

      <div className="h-calc50 shadow-shadown1 rounded-[16px] relative overflow-hidden ">
        <HeadContent
          title={"Danh sách camera"}
          onClickCreatebtn={handleClickOpen}
          hiddenUpdateBtn
        />

        <OpactityAnimation className="h-calc72">
          <CameraTable />
        </OpactityAnimation>

        <CreateCameraDialog
          open={open}
          handleClose={handleClose}
          submit={handleCreateCamera}
        />
      </div>
    </section>
  ) : null;
};

export default function CameraPage() {
  return (
    <CameraProvider>
      <CameraComponents />
    </CameraProvider>
  );
}

CameraPage.Layout = HomeLayout;
