import { serviceTypeApi } from "@/api-client/setting/service-type";
import { TableAction } from "@/components";
import { LoadingPopup } from "@/components/common/loading/loading-popup";
import { DialogConfirm } from "@/components/dialog/confirm-dialog";
import { SettingServiceDialog } from "@/components/dialog/create-setting-service";
import { ResultEnum } from "@/constants/enum";
import { TypeServiceKey } from "@/constants/type-service";
import { useTypeService } from "@/context/service-type-context";
import useHandleError from "@/hooks/useHandleError";
import { TypeServiceRes } from "@/interfaces/type-service";
import { getIconActiveByKey, getIconByKey } from "@/libs/type-service";
import moment from "moment";
import Image from "next/image";
import { enqueueSnackbar } from "notistack";
import { useState } from "react";

export interface ITableItemSettingServiceProps {
  data: TypeServiceRes;
  index: number;
  reload: () => void;
}

export function TableItemSettingService(props: ITableItemSettingServiceProps) {
  const { data, index } = props;
  const [openEditDialog, setOpenEditDialog] = useState(false);
  const [openRemoveDialog, setOpenRemoveDialog] = useState(false);
  const { total, setTotal } = useTypeService();
  const handleError = useHandleError();
  const [loading, setLoading] = useState(false);

  const handleUpdate = async (formData: any) => {
    try {
      let payload = {
        ...formData,
        name: formData?.name.trim(),
        key: formData?.key.trim(),
      };
      await serviceTypeApi.update(payload, data.id);
      props.reload();

      enqueueSnackbar("Cập nhật cấu hình loại AI thành công", {
        variant: "success",
      });
      return ResultEnum.success;
    } catch (error) {
      handleError(error, "Cập nhật cấu hình loại AI không thành công");
      return ResultEnum.error;
    }
  };

  const handleRemove = async () => {
    setLoading(true);
    serviceTypeApi
      .delete(data.id)
      .then(() => {
        props.reload();
        setTotal(total - 1);
        enqueueSnackbar("Xóa loại AI thành công", { variant: "success" });
      })
      .catch((error) => {
        handleError(error, "Xóa loại AI không thành công");
      })
      .finally(() => {
        setLoading(false);
      });
  };

  return (
    <div className="w-full flex flex-row min-w-[1200px] table-row-custom items-center">
      <div className="w-[60px] py-6 flex justify-center">
        {_renderText(index.toString())}
      </div>
      <div className="w-[10%] py-6 flex justify-start">
        <Image
          src={getIconActiveByKey(data.key as TypeServiceKey)}
          width={24}
          height={24}
          alt="icon"
        />
      </div>
      <div className="w-[30%] py-6 flex justify-start">
        {_renderText(data?.name ?? "")}
      </div>
      <div className="w-[30%] py-6 flex justify-start">
        {_renderText(data?.key ?? "")}
      </div>
      <div className="w-[20%] py-6 flex justify-start">
        {_renderText(moment(data.created).format("DD/MM/yyyy HH:mm"))}
      </div>
      <div className="w-[10%] py-6 flex justify-center">
        <TableAction
          onEdit={() => setOpenEditDialog(true)}
          onRemove={() => setOpenRemoveDialog(true)}
        />
      </div>

      {/* update dialog */}
      <SettingServiceDialog
        open={openEditDialog}
        handleClose={() => setOpenEditDialog(false)}
        submit={handleUpdate}
        data={data}
      />

      {/* remove dialog */}
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

function _renderText(text: string) {
  return <p className="font-medium text-grayOz text-sm">{text}</p>;
}
