import { personApi } from "@/api-client/identification-profile/person";
import { LoadingPopup } from "@/components/common/loading/loading-popup";
import { DialogConfirm } from "@/components/dialog/confirm-dialog";
import { IdentificationUserDialog } from "@/components/dialog/create-identification-user";
import { ResultEnum } from "@/constants/enum";
import useScrollToElement from "@/hooks/use-scroll-to-element";
import useHandleError from "@/hooks/useHandleError";
import { IPerson } from "@/interfaces/identification-profile/person";
import { useRouter } from "next/navigation";
import { enqueueSnackbar } from "notistack";
import { useState } from "react";
import { GridItemTable } from "./grid-item";
import { ListItemTable } from "./list-item";

export interface IUserTableItemProps {
  data: IPerson;
  index: number;
  reload: any;
  setTotal: any;
  viewType: "GRID" | "LIST";
}

export function UserTableItem(props: IUserTableItemProps) {
  const { data, viewType } = props;
  const [openEditDialog, setOpenEditDialog] = useState(false);
  const [openRemoveDialog, setOpenRemoveDialog] = useState(false);
  const handleError = useHandleError();
  const [loading, setloading] = useState(false);
  const router = useRouter();

  const handleUpdate = async (formData: any) => {
    try {
      const formJson = Object.fromEntries(formData.entries());

      const payload = {
        name: formJson.name,
        other_info: {
          gender: JSON.parse(formJson.other_info).gender,
          address: JSON.parse(formJson.other_info).address,
        },
      };

      await personApi.update(payload, props.data.id);
      props.reload();
      enqueueSnackbar("Cập nhật hồ sơ nhận diện đối tượng thành công", {
        variant: "success",
      });
      return ResultEnum.success;
    } catch (error) {
      handleError(error, "Cập nhật hồ sơ nhận diện đối tượng không thành công");
      return ResultEnum.error;
    }
  };

  const handleRemove = () => {
    setloading(true);
    personApi
      .delete(props.data.id)
      .then((res) => {
        props.reload();
        props.setTotal();
        enqueueSnackbar("Xóa hồ sơ nhận diện đối tượng thành công", {
          variant: "success",
        });
      })
      .catch((error) => {
        enqueueSnackbar("Xóa hồ sơ nhận diện đối tượng không thành công", {
          variant: "error",
        });
      })
      .finally(() => {
        setloading(false);
      });
  };

  const { handlePushRoute } = useScrollToElement();

  const handleClick = () => {
    handlePushRoute("/identification-profile/user", data.id);
    router.push("/identification-profile/user/" + data.id);
  };

  return (
    <div id={data.id}>
      {viewType === "GRID" ? (
        <GridItemTable
          data={data}
          index={props.index}
          reload={props.reload}
          setTotal={props.setTotal}
          handleClick={handleClick}
          setOpenEditDialog={setOpenEditDialog}
          setOpenRemoveDialog={setOpenRemoveDialog}
        />
      ) : (
        <ListItemTable
          data={data}
          index={props.index}
          reload={props.reload}
          setTotal={props.setTotal}
          handleClick={handleClick}
          setOpenEditDialog={setOpenEditDialog}
          setOpenRemoveDialog={setOpenRemoveDialog}
        />
      )}

      {openEditDialog && (
        <IdentificationUserDialog
          open={openEditDialog}
          handleClose={() => {
            setOpenEditDialog(false);
            props.reload();
          }}
          submit={handleUpdate}
          data={props.data}
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
