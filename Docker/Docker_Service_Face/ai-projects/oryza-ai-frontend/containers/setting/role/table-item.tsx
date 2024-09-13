import { Status, TableAction } from "@/components";
import { DialogConfirm } from "@/components/dialog/confirm-dialog";
import { enqueueSnackbar } from "notistack";
import { useState } from "react";
import Image from "next/image";
import { AVATAR_URL } from "@/constants/avatar";
import {UserRes} from "@/interfaces/user";
import { useUser } from "@/context/user-context";
import useHandleError from "@/hooks/useHandleError";
import { ResultEnum } from "@/constants/enum";
import { userApi } from "@/api-client/setting/user";
import { SettingRoleDialog } from "@/components/dialog/create-setting-role";
import { useAuth } from "@/hooks/auth-hook";
import { LoadingDialog } from "@/components/dialog/loading-dialog";
import { LoadingPopup } from "@/components/common/loading/loading-popup";
import { useEffect } from "react";
export interface ITableItemSettingRoleProps {
  data: UserRes;
  index: number;
  reload: () => void;
}

export function TableItemSettingRole(props: ITableItemSettingRoleProps) {
  const {index, data} = props;
  const {total, setTotal, isSuperUser} = useUser();
  const [openEditDialog, setOpenEditDialog] = useState(false);
  const [openRemoveDialog, setOpenRemoveDialog] = useState(false);
  const [loading, setLoading] = useState(false);
  const [openReloadDialog, setOpenReloadDialog] = useState(false);
  const handleError = useHandleError();

  const [avatarUpdateKey, setAvatarUpdateKey] = useState(0);

  const handleUpdate = async (formData: any) => {
    console.log("handleUpdate is called")
    try {
        let newPayload = {
            ...formData
        };
        if (formData?.new_password) {
            newPayload.new_password = formData?.new_password.trim();
        }
        if (Object.keys(newPayload).length === 0) return ResultEnum.success;
        console.log('update payload', newPayload)
        await userApi.update(newPayload, props.data.id);
        setAvatarUpdateKey(prevKey => prevKey + 1);
        props.reload();
        enqueueSnackbar("Cập nhật người dùng thành công", { variant: "success" });
        return ResultEnum.success;
    } catch (error) {
        console.log('Error occurred, setting openReloadDialog to false');
        handleError(error, "Đã xảy ra lỗi khi cập nhật người dùng");
        return ResultEnum.error;
    } finally {
      setLoading(false);
    }
  };

  const handleErrorWithHook = useHandleError();
  const { profile } = useAuth();
  const handleRemove = async () => {
      console.log("handleRemove is called")
      setLoading(true);
      if (profile?.id === props.data.id) {
          enqueueSnackbar("Không thể xóa tài khoản đang đăng nhập", { variant: "error" });
          return;
      }
      try { 
          await userApi.delete(props.data.id);
          props.reload();
          setTotal(total - 1);
          enqueueSnackbar("Xóa người dùng thành công", { variant: "success" });
      } catch (error) {
        handleErrorWithHook(error, "Đã xảy ra lỗi khi xóa người dùng");
      } finally {
          setLoading(false);
      }
  };

  const ActionButton =  () => (
    <TableAction
      onEdit={() => {
        if (isSuperUser || !data?.is_superuser) {
          setOpenEditDialog(true);
        }
      }}
      onRemove={() => {
        if (isSuperUser || !data?.is_superuser) {
          setOpenRemoveDialog(true);
        }
      }}
    />
  );
  
  
  // Dont show super user in the list
  // if (data.is_superuser) {
  //   return null;
  // } 
  // Update the imageUrl state whenever props.data.avatar changes
  const [imageUrl, setImageUrl] = useState(`${props.data.avatar || AVATAR_URL}?v=${Date.now()}`);
    
  useEffect(() => {
    setImageUrl(`${props.data.avatar || AVATAR_URL}?v=${avatarUpdateKey}`);
  }, [props.data.avatar, avatarUpdateKey]);

  return (
    <div className="w-full flex flex-row min-w-[1200px] table-row-custom items-center">
      {/* index id=1 */}
      <div className="w-[60px] py-6 flex justify-center">
        {_renderText(index.toString())}
      </div>
      {/* image & username id=2 */}
      <div className="w-[15%] py-6 flex justify-start">
      <div className="flex flex-row space-x-2 items-center">
        <Image
          key={imageUrl}
          className="object-cover rounded-full"
          src={imageUrl}
          alt="avatar user"
          width={40}
          height={40}
          layout="fixed"
          style={{ borderRadius: '50%', width: '40px', height: '40px', objectFit: 'cover' }}
        />
        {_renderText(props.data.username)}
      </div>
    </div>
      {/* role id=3 */}
      <div className={`${isSuperUser ? "w-[10%]" : "w-[15%]"} py-6 flex justify-start`}>
        {_renderText(props.data.is_superuser ? "ORYZA" : props.data.is_admin ? "Quản trị viên" : "Người dùng")}
      </div>
      {/* email id=4 */}
      <div className={`${isSuperUser ? "w-[20%]" : "w-[25%]"} py-6 flex justify-start`}>
        {_renderText(props.data.email)}
      </div>
      {/* company id=5 */}
      {isSuperUser && (
        <div className="w-[20%] py-6 flex justify-start">
          {_renderText(props.data.company.name)}
        </div>
      )}
      {/* time created id=6 */}
      <div className={`${isSuperUser ? "w-[15%]" : "w-[20%]"} py-6 flex justify-start`}>
        {_renderText(new Date(props.data.created).toLocaleString('en-GB').replace(',', ''))}
      </div>
      {/* status id=7 */}
      <div className={`${isSuperUser ? "w-[10%]" : "w-[15%]"} py-6 flex justify-start`}>
        <Status status = {props.data.is_active ?  "ACTIVE" : "INACTIVE"} />
      </div>
      {/* action id=8 */}
      <div className="w-[0%] py-6 justify-start">
        <ActionButton />
      </div>
      <SettingRoleDialog
        open={openEditDialog}
        handleClose={() => setOpenEditDialog(false)}
        submit={handleUpdate}
        data={props.data}
      />
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

      <LoadingDialog
        open={openReloadDialog}
        onClose={function (): void {
          setOpenReloadDialog(false);
        }}
        text="Đang tải lại dữ liệu..."
      />
    </div>
  );
}



function _renderText(text: string) {
  return <p className="font-medium text-grayOz text-sm">{text}</p>;
}
