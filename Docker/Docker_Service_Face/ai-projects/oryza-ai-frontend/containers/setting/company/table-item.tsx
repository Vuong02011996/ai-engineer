import { companyApi } from "@/api-client/setting/company";
import { TableAction } from "@/components";
import { DialogConfirm } from "@/components/dialog/confirm-dialog";
import { CreateCompanyDialog } from "@/components/dialog/create-company";
import { CompanyRes } from "@/interfaces/company";
import { CreateCompany } from "@/models/company";
import { enqueueSnackbar } from "notistack";
import { useState } from "react";
import moment from "moment";
import { useSettingCompany } from "@/context/company-context";
import useHandleError from "@/hooks/useHandleError";
import { ResultEnum } from "@/constants/enum";
import { NotifiMsg } from "@/constants/notifi-msg";
import { LoadingPopup } from "@/components/common/loading/loading-popup";

export interface ITableItemSettingCompanyProps {
  data: CompanyRes;
  index: number;
  reload: () => void;
}

export function TableItemSettingCompany(props: ITableItemSettingCompanyProps) {
  const { index } = props;
  const { data, setData, total, setTotal } = useSettingCompany();
  const handleError = useHandleError();

  const [openEditDialog, setOpenEditDialog] = useState(false);
  const [openRemoveDialog, setOpenRemoveDialog] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleUpdate = async (formData: any) => {
    try {
      let payload: CreateCompany = {
        name: formData.name.trim(),
        domain: formData.domain.trim(),
      };
      await companyApi.update(payload, props.data.id);
      props.reload();
      enqueueSnackbar(NotifiMsg.updateCompany, { variant: "success" });
      return ResultEnum.success;
    } catch (error) {
      handleError(error, NotifiMsg.updateCompanyErr);
      return ResultEnum.error;
    }
  };

  const handleRemove = async () => {
    setLoading(true);
    try {
      await companyApi.delete(props.data.id);
      setData(data.filter((item) => item.id !== props.data.id));
      setTotal(total - 1);
      enqueueSnackbar(NotifiMsg.deleteCompany, { variant: "success" });
    } catch (error) {
      handleError(error, NotifiMsg.deleteCompanyErr);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full flex flex-row min-w-[1200px] table-row-custom items-center">
      <div className="w-[60px] py-6 flex justify-center">
        {_renderText(index.toString())}
      </div>
      <div className="w-[30%] py-6 flex justify-start">
        {_renderText(props.data?.name ?? "")}
      </div>
      <div className="w-[40%] py-6 flex justify-start">
        {_renderText(props.data?.domain ?? "")}
      </div>
      <div className="w-[20%] py-6 flex justify-start">
        {_renderText(moment(props.data.created).format("DD/MM/yyyy HH:mm:ss"))}
      </div>

      <div className="w-[10%] py-6 flex justify-center">
        <TableAction
          onEdit={() => setOpenEditDialog(true)}
          onRemove={() => setOpenRemoveDialog(true)}
        />
      </div>

      {/* update dialog */}
      {openEditDialog && (
        <CreateCompanyDialog
          open={openEditDialog}
          handleClose={() => setOpenEditDialog(false)}
          submit={handleUpdate}
          data={props.data}
        />
      )}

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
