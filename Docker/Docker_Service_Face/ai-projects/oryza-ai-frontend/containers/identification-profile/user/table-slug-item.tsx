import { personCameraApi } from "@/api-client/identification-profile/person-camera";
import { Status } from "@/components";
import CheckboxCustom2 from "@/components/common/checkbox/checbox-2";
import { LoadingPopup } from "@/components/common/loading/loading-popup";
import { SwitchBtn } from "@/components/common/switch/switch-btn";
import { DialogConfirm } from "@/components/dialog/confirm-dialog";
import { IdentificationUserDialog } from "@/components/dialog/create-identification-user";
import { ResultEnum } from "@/constants/enum";
import useHandleError from "@/hooks/useHandleError";
import { ICameraAI } from "@/interfaces/identification-profile/camera-ai";
import { useRouter } from "next/router";
import { enqueueSnackbar } from "notistack";
import clsx from "clsx";

import { useState } from "react";

export interface IUserSlugTableItemProps {
  data: ICameraAI;
  index: number;
  isOn: boolean;
  reload: any;
  disablePadding?: boolean;
}

export function UserSlugTableItem(props: IUserSlugTableItemProps) {
  const { data, disablePadding } = props;

  const [openEditDialog, setOpenEditDialog] = useState(false);
  const [openRemoveDialog, setOpenRemoveDialog] = useState(false);
  const handleError = useHandleError();
  const [loading, setloading] = useState(false);
  const router = useRouter();

  const handleUpdate = async (formData: any) => {
    try {
      let newPayload = {
        ...formData,
      };
      // if (formData?.name && data.name.trim() !== newPayload?.name.trim()) {
      //   newPayload.name = formData?.name.trim();
      // } else {
      //   delete newPayload.name;
      // }
      // if (Object.keys(newPayload).length === 0) {
      //   enqueueSnackbar("Cập nhật hãng camera thành công", {
      //     variant: "success",
      //   });
      //   return ResultEnum.success;
      // }
      // await cameraBrandApi.update(newPayload, props.data.id);
      // props.reload();
      // enqueueSnackbar("Cập nhật hãng camera thành công", {
      //   variant: "success",
      // });
      return ResultEnum.success;
    } catch (error) {
      handleError(error, "Cập nhật hồ sơ nhận diện đối tượng không thành công");
      return ResultEnum.error;
    }
  };

  const handleRemove = () => {
    // setloading(true);
    // cameraBrandApi
    //   .delete(props.data.id)
    //   .then((res) => {
    //     props.reload();
    //     props.setTotal();
    //     enqueueSnackbar("Xóa hãng camera thành công", { variant: "success" });
    //   })
    //   .catch((error) => {
    //     enqueueSnackbar("Xóa hãng camera không thành công", {
    //       variant: "error",
    //     });
    //   })
    //   .finally(() => {
    //     setloading(false);
    //   });
  };

  const hanldeAddPersonToCamera = async () => {
    if (loading) return;

    setloading(true);
    try {
      const payload = {
        person_id: router.query.slug,
        id_camera: data.id,
        key_camera: data.brand_camera.key,
        // host_camera: data.ip_address,
        // username_camera: data.username,
        // password_camera: data.password,
        // port_camera: data.port.toString(),
      };
      await personCameraApi.create(payload);
      props.reload();
    } catch (error) {
      enqueueSnackbar("Thêm đối tượng không thành công", {
        variant: "error",
      });
    } finally {
      setloading(false);
    }
  };

  const hanldeRemovePersonToCamera = async () => {
    if (!data.idCameraPerson || loading) return;
    setloading(true);

    try {
      const payload = {
        key_camera: data.brand_camera.key,
        id_camera: data.id,
        // host_camera: data.ip_address,
        // username_camera: data.username,
        // password_camera: data.password,
        // port_camera: data.port.toString(),
      };

      await personCameraApi.remove(payload, data.idCameraPerson);
      props.reload();
    } catch (error) {
      enqueueSnackbar("Tắt AI không thành công", {
        variant: "error",
      });
    } finally {
      setloading(false);
    }
  };

  return (
    <div className="w-full flex flex-row min-w-[1200px] table-row-custom items-center">
      {/* <div className="w-[60px] py-6 flex justify-center">
        {_renderCheckbox(data.id, handleCheck, checkedIds)}
      </div> */}
      <div
        className={clsx(
          "w-[60px] flex justify-center",
          disablePadding ? "py-2" : "py-6"
        )}
      >
        {_renderText(props.index.toString())}
      </div>
      <div
        className={clsx(
          "w-[30%] flex justify-start",
          disablePadding ? "py-2" : "py-6"
        )}
      >
        {_renderText(data?.name)}
      </div>
      <div
        className={clsx(
          "w-[20%] flex justify-start",
          disablePadding ? "py-2" : "py-6"
        )}
      >
        {_renderText(data?.type_camera)}
      </div>
      <div
        className={clsx(
          "w-[30%] flex justify-start",
          disablePadding ? "py-2" : "py-6"
        )}
      >
        {_renderText(data.ip_address)}
      </div>
      <div
        className={clsx(
          "w-[20%] flex justify-start",
          disablePadding ? "py-2" : "py-6"
        )}
      >
        <SwitchBtn
          checked={props.isOn}
          onChange={(value, checked) => {
            if (checked) {
              hanldeAddPersonToCamera();
            } else {
              hanldeRemovePersonToCamera();
            }
          }}
        />
      </div>
      {/* <div className="w-[20%] py-6 flex justify-start">
        <Status status="OFFLINE" />
      </div> */}

      {openEditDialog && (
        <IdentificationUserDialog
          open={openEditDialog}
          handleClose={() => setOpenEditDialog(false)}
          submit={handleUpdate}
        />
      )}

      {openRemoveDialog && (
        <DialogConfirm
          close={() => setOpenRemoveDialog(false)}
          action={handleRemove}
          image={"/icons/bin.svg"}
          title={"Bạn chắc chắn xoá không?"}
          description={"Sau khi xoá, dữ liệu sẽ không được phục hồi."}
        />
      )}

      <LoadingPopup open={loading} />
    </div>
  );
}

function _renderText(text?: string) {
  return <p className="font-medium text-grayOz text-sm">{text ?? ""}</p>;
}
function _renderCheckbox(value: any, handleCheck: any, checkedIds: string[]) {
  return (
    <div>
      <CheckboxCustom2
        checked={checkedIds.includes(value)}
        onChange={(checked) => {
          handleCheck(value, checked);
        }}
      />
    </div>
  );
}
