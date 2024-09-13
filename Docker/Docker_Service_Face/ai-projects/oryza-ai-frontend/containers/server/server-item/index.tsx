import { serverApi } from "@/api-client/server";
import { Status, TableAction } from "@/components";
import { OutlineBtn } from "@/components/common";
import { DialogConfirm } from "@/components/dialog/confirm-dialog";
import { CreateServerDialog } from "@/components/dialog/craete-server";
import { useServers } from "@/context/server-context";
import { ServerRes } from "@/interfaces/server";
import dataMock from "@/mock/server";
import { CreateServer } from "@/models/server";
import { useRouter } from "next/navigation";
import { enqueueSnackbar } from "notistack";
import { useState } from "react";
import { SystemItem } from "./system-item";
import { CreateServiceDialog } from "@/components/dialog/create-service";
import { serviceApi } from "@/api-client/service";
import { InfoServer } from "@/models/redux.model";

export interface IServerItemProps {
  data: ServerRes;
  reload: () => void;
  serverInfo?: InfoServer;
}

export function ServerItem(props: IServerItemProps) {
  const { serverInfo } = props;
  const { setData, data } = useServers();
  const router = useRouter();

  const [openEditDialog, setOpenEditDialog] = useState(false);
  const [openRemoveDialog, setOpenRemoveDialog] = useState(false);
  const [openCreateServiceDialog, setOpenCreateServiceDialog] = useState(false);

  const handleUpdate = (formData: any) => {
    let payload: CreateServer = {
      name: formData?.name.trim() ?? "",
      ip_address: formData?.ip_address.trim() ?? "",
    };
    serverApi
      .update(payload, formData.id)
      .then((res) => {
        props.reload();
        enqueueSnackbar("Cập nhật server thành công", { variant: "success" });
      })
      .catch((error) => {
        enqueueSnackbar(
          error?.response?.data?.detail ?? "Cập nhật server không thành công",
          {
            variant: "error",
          }
        );
      });
  };

  const handleRemove = () => {
    serverApi
      .delete(props.data.id)
      .then((res) => {
        setData(data.filter((item) => item.id !== props.data.id));
        enqueueSnackbar("Xóa server thành công", { variant: "success" });
      })
      .catch((error) => {
        enqueueSnackbar("Xóa server không thành công", { variant: "error" });
      });
  };

  const handleCreateService = (formData: any) => {
    serviceApi
      .create({
        ...formData,
        server_id: props.data.id,
      })
      .then((res: any) => {
        enqueueSnackbar("Tạo mới service thành công", { variant: "success" });
      })
      .catch((error) => {
        const errorMsg =
          error?.response?.data?.detail ?? "Tạo mới service không thành công";
        enqueueSnackbar(errorMsg, {
          variant: "error",
        });
      });
  };

  const handleClick = (event: any) => {
    event.stopPropagation();

    router.push(`/server/${props.data.id}`);
  };

  return (
    <div className="rounded-2xl border border-[#F2F2F2] overflow-hidden cursor-pointer hover:shadow-shadown1 transition-all duration-300 ">
      {/* title */}
      <div>
        <div
          onClick={handleClick}
          className="flex flex-row justify-between p-[14px]"
        >
          <div className="space-y-1 flex-1  ">
            <div className="flex flex-row space-x-[8px]">
              <div>
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="24"
                  height="24"
                  viewBox="0 0 24 24"
                  fill="none"
                >
                  <path
                    d="M8.97076 0.000183105C6.86089 0.00551107 4.95347 0.378471 3.52025 1.02848C2.80098 1.35349 2.19891 1.74243 1.74604 2.22727C1.29849 2.70679 1.00012 3.2982 1.00012 3.94821L1.00546 9.23355C1.00294 9.25123 1.00115 9.269 1.00012 9.28683C1.00012 9.35076 1.00013 9.4147 1.00546 9.47331L1.01611 14.5402C1.00835 14.5717 1.00301 14.6038 1.00012 14.6361C1.00012 14.7214 1.00545 14.8119 1.01611 14.8918L1.02144 20.2411C1.02201 20.2769 1.02557 20.3125 1.0321 20.3477C1.23989 21.5625 2.33211 22.4149 3.74402 23.0063C5.16126 23.5924 6.98876 23.9334 8.98142 23.9334C11.9171 23.9334 14.4745 23.2514 15.9078 21.9994C16.0303 22.0047 16.1529 22.01 16.2754 22.01C16.7016 22.01 17.1279 21.9727 17.5435 21.8981C17.6546 21.8783 17.7584 21.8294 17.8445 21.7564C17.9306 21.6834 17.9959 21.5889 18.0336 21.4825L18.3746 20.5235C18.5558 20.4596 18.7316 20.385 18.9074 20.3051L19.8238 20.742C19.9263 20.7912 20.0401 20.8122 20.1534 20.8029C20.2667 20.7935 20.3755 20.7541 20.4685 20.6887C21.1611 20.1985 21.7685 19.5964 22.2534 18.8985C22.3178 18.8061 22.3566 18.6982 22.366 18.586C22.3754 18.4737 22.3549 18.3609 22.3067 18.2591L21.8698 17.3374C21.955 17.1669 22.0243 16.9857 22.0935 16.8099L23.0526 16.4689C23.1589 16.4312 23.2534 16.3659 23.3264 16.2798C23.3994 16.1938 23.4483 16.0899 23.4681 15.9788C23.5374 15.5578 23.5747 15.1369 23.5747 14.7107C23.5747 14.2845 23.5374 13.8636 23.4681 13.448C23.4492 13.3359 23.4007 13.2309 23.3276 13.1438C23.2546 13.0567 23.1596 12.9907 23.0526 12.9525L22.0935 12.6115C22.0296 12.4357 21.955 12.2545 21.8751 12.084L22.312 11.1623C22.3602 11.0605 22.3807 10.9477 22.3713 10.8354C22.362 10.7231 22.3231 10.6153 22.2587 10.5229C21.7685 9.82495 21.1611 9.2229 20.4685 8.73273C20.3755 8.66732 20.2667 8.62791 20.1534 8.61854C20.0401 8.60918 19.9263 8.6302 19.8238 8.67945L18.9074 9.11634C18.7316 9.03642 18.5558 8.96182 18.3746 8.89788L18.0336 7.93885C17.9959 7.83248 17.9306 7.738 17.8445 7.66501C17.7584 7.59202 17.6546 7.54312 17.5435 7.52328C17.3463 7.48598 17.1439 7.45934 16.9414 7.44336C16.9467 6.23924 16.952 5.06175 16.9574 3.94821C16.9574 3.2982 16.659 2.70147 16.2061 2.22195C15.7586 1.74244 15.1512 1.34817 14.4319 1.02316C12.988 0.373151 11.0806 0.000183105 8.97076 0.000183105ZM8.97076 1.27889C10.9261 1.27889 12.6897 1.6412 13.9045 2.18998C14.5118 2.46704 14.9807 2.78671 15.2737 3.09574C15.5668 3.41009 15.6787 3.68181 15.6787 3.94821C15.6787 4.21461 15.5668 4.48633 15.2737 4.80068C14.9807 5.10971 14.5118 5.42938 13.9045 5.70644C12.6897 6.25522 10.9261 6.61752 8.97076 6.61219C7.02073 6.61219 5.25716 6.24989 4.04772 5.70111C3.44033 5.42405 2.97147 5.10437 2.67843 4.79535C2.39072 4.48633 2.27883 4.21461 2.27883 3.94821C2.27883 3.68181 2.39072 3.41009 2.67843 3.10107C2.97147 2.78672 3.44033 2.46704 4.04772 2.19531C5.25716 1.64653 7.02073 1.28422 8.97076 1.27889ZM2.28417 6.14866C2.64114 6.42039 3.05672 6.65482 3.52025 6.86794C4.95347 7.51262 6.86089 7.8909 8.97076 7.8909C11.0806 7.89623 12.988 7.51795 14.4319 6.86794C14.8955 6.66015 15.311 6.42038 15.668 6.15398C15.668 6.58022 15.668 6.99581 15.6627 7.43803C15.4496 7.45401 15.2311 7.48066 15.0127 7.52328C14.9016 7.54312 14.7977 7.59202 14.7116 7.66501C14.6255 7.738 14.5603 7.83248 14.5225 7.93885L14.1815 8.89256C14.0004 8.96183 13.8245 9.03109 13.6487 9.11634L12.7323 8.67945C12.6298 8.6302 12.516 8.60918 12.4027 8.61854C12.2894 8.62791 12.1806 8.66732 12.0876 8.73273C11.395 9.2229 10.7876 9.82495 10.3028 10.5229C10.2383 10.6153 10.1995 10.7231 10.1901 10.8354C10.1808 10.9477 10.2012 11.0605 10.2495 11.1623L10.6011 11.9029C10.545 11.8917 10.4877 11.8881 10.4306 11.8922C9.96709 11.9348 9.47692 11.9561 8.97076 11.9561C7.02073 11.9561 5.25716 11.5885 4.04772 11.0397C3.44033 10.768 2.97147 10.4483 2.67843 10.1393C2.43334 9.8729 2.31613 9.63848 2.28417 9.40937V6.14866ZM16.2701 8.6901H16.2754C16.5045 8.6901 16.7336 8.70609 16.9627 8.73273L17.2717 9.60651C17.3054 9.70159 17.3611 9.78736 17.4342 9.85681C17.5074 9.92626 17.5959 9.97742 17.6926 10.0061C18.007 10.102 18.316 10.2299 18.6037 10.3844C18.6924 10.4327 18.7912 10.4594 18.8922 10.4622C18.9931 10.4649 19.0933 10.4438 19.1845 10.4004L20.021 10.0008C20.3779 10.2885 20.7029 10.6082 20.9853 10.9651L20.5857 11.807C20.5432 11.8974 20.5225 11.9966 20.5253 12.0966C20.5281 12.1965 20.5543 12.2944 20.6017 12.3824C20.7616 12.6754 20.8841 12.9791 20.98 13.2988C21.0087 13.3955 21.0598 13.484 21.1293 13.5572C21.1987 13.6303 21.2845 13.686 21.3796 13.7197L22.2534 14.0287C22.28 14.2525 22.296 14.4816 22.296 14.7107C22.296 14.9398 22.28 15.1689 22.2534 15.3927L21.3796 15.707C21.2851 15.7402 21.1997 15.795 21.1303 15.8672C21.0609 15.9394 21.0094 16.0269 20.98 16.1226C20.8841 16.437 20.7562 16.746 20.6017 17.0337C20.5534 17.1224 20.5267 17.2212 20.524 17.3221C20.5212 17.4231 20.5423 17.5233 20.5857 17.6144L20.9853 18.4509C20.7029 18.8132 20.3779 19.1329 20.021 19.4206L19.1791 19.021C19.0891 18.9777 18.9901 18.9561 18.8902 18.958C18.7902 18.9598 18.6921 18.9851 18.6037 19.0317C18.3107 19.1915 18.007 19.3194 17.6926 19.4153C17.5965 19.4434 17.5083 19.4938 17.4352 19.5623C17.3621 19.6308 17.3061 19.7155 17.2717 19.8096L16.9627 20.6834C16.7336 20.71 16.5045 20.7313 16.2754 20.7313C16.0516 20.7313 15.8225 20.71 15.5934 20.6887L15.2844 19.8096C15.25 19.7155 15.194 19.6308 15.1209 19.5623C15.0478 19.4938 14.9596 19.4434 14.8635 19.4153C14.5491 19.3194 14.2454 19.1915 13.9524 19.0317C13.864 18.9851 13.7659 18.9598 13.666 18.958C13.566 18.9561 13.4671 18.9777 13.377 19.021L12.5352 19.4206C12.1782 19.1329 11.8532 18.8132 11.5708 18.4563L11.9704 17.6144C12.0129 17.524 12.0336 17.4248 12.0308 17.3248C12.0281 17.2249 12.0019 17.127 11.9544 17.039C11.7999 16.746 11.672 16.4423 11.5761 16.1226C11.5474 16.0259 11.4963 15.9374 11.4268 15.8642C11.3574 15.7911 11.2716 15.7354 11.1765 15.7017L10.3028 15.3927C10.2761 15.1636 10.2601 14.9398 10.2601 14.7107C10.2601 14.4816 10.2761 14.2525 10.3028 14.0287L11.1765 13.7197C11.2716 13.686 11.3574 13.6303 11.4268 13.5572C11.4963 13.484 11.5474 13.3955 11.5761 13.2988C11.672 12.9791 11.7946 12.6754 11.9544 12.3824C12.0019 12.2944 12.0281 12.1965 12.0308 12.0966C12.0336 11.9966 12.0129 11.8974 11.9704 11.807L11.5708 10.9651C11.8532 10.6082 12.1782 10.2832 12.5352 10.0008L13.3717 10.4004C13.4628 10.4438 13.563 10.4649 13.664 10.4622C13.7649 10.4594 13.8637 10.4327 13.9524 10.3844C14.2401 10.2299 14.5491 10.102 14.8688 10.0061C14.9645 9.97669 15.052 9.92521 15.1242 9.8558C15.1964 9.78639 15.2513 9.701 15.2844 9.60651L15.5987 8.73273C15.8225 8.70609 16.0463 8.6901 16.2701 8.6901ZM2.28949 11.4979C2.64646 11.7643 3.05672 11.9988 3.52025 12.2066C4.9588 12.8566 6.86089 13.2295 8.97076 13.2349H9.1679C9.12872 13.3005 9.10166 13.3727 9.08798 13.448C9.01338 13.8636 8.98142 14.2845 8.98142 14.7107C8.98142 15.1316 9.01338 15.5578 9.08798 15.9734C9.10695 16.0855 9.15545 16.1905 9.2285 16.2776C9.30154 16.3647 9.3965 16.4307 9.50356 16.4689L10.4626 16.8099C10.5212 16.9751 10.5905 17.1349 10.6651 17.2948C10.5713 17.2533 10.469 17.2351 10.3667 17.2415C9.91914 17.2841 9.45561 17.3054 8.97076 17.3054C7.02073 17.3054 5.26249 16.9378 4.04772 16.389C3.44033 16.1173 2.97147 15.7923 2.67843 15.4833C2.44933 15.2382 2.33212 15.0197 2.29482 14.8013L2.28949 11.4979ZM2.29482 16.8472C2.65179 17.1136 3.06205 17.348 3.52025 17.5558C4.95347 18.2058 6.86089 18.5788 8.97076 18.5841C9.38634 18.5841 9.7966 18.5681 10.1962 18.5415C10.1955 18.6684 10.2326 18.7927 10.3028 18.8985C10.7876 19.5964 11.395 20.1985 12.0929 20.6887C12.1854 20.7531 12.2932 20.792 12.4055 20.8013C12.5177 20.8107 12.6305 20.7902 12.7323 20.742L13.6487 20.3051C13.8245 20.385 14.0004 20.4596 14.1815 20.5235L14.5012 21.4239C13.3077 22.1112 11.2778 22.6547 8.98142 22.6547C7.13794 22.6547 5.44898 22.3297 4.23953 21.8235C3.05139 21.328 2.40671 20.6727 2.30015 20.1612L2.29482 16.8472Z"
                    fill="#AFAFAF"
                  />
                  <path
                    d="M16.2702 10.6934C14.0644 10.6934 12.2583 12.4942 12.2583 14.7053C12.2583 16.9111 14.0644 18.7119 16.2702 18.7119C18.476 18.7119 20.2822 16.9111 20.2822 14.7053C20.2822 12.4942 18.476 10.6934 16.2702 10.6934ZM16.2702 11.9721C17.7834 11.9721 19.0035 13.1868 19.0035 14.7053C19.0035 16.2184 17.7834 17.4332 16.2702 17.4332C14.7517 17.4332 13.537 16.2184 13.537 14.7053C13.537 13.1868 14.7517 11.9721 16.2702 11.9721Z"
                    fill="#AFAFAF"
                  />
                </svg>
              </div>
              <p className="text-blackOz text-base font-semibold   ">
                {props.data.name}
              </p>
            </div>
            <p className="text-[#64686D] text-xs font-normal">
              Địa chỉ IP:{" "}
              <span className="text-[#55595d]">{props.data.ip_address}</span>
            </p>

            <p className="text-[#64686D] text-xs font-medium pb-1 text-start">
              Số AI service:{" "}
              <span className="text-blackOz">{props?.data?.count ?? 0}</span>
            </p>
          </div>
          <div className="justify-between items-end flex flex-col   ">
            <TableAction
              onEdit={() => setOpenEditDialog(true)}
              onRemove={() => setOpenRemoveDialog(true)}
            />
          </div>
        </div>
        <div className="flex flex-row justify-between px-[14px] pb-3">
          <div onClick={handleClick} className="flex flex-1 ">
            <Status status={props.data.is_alive ? "ONLINE" : "OFFLINE"} />
          </div>
          <OutlineBtn
            text={"Tạo service"}
            onClick={() => setOpenCreateServiceDialog(true)}
            className={
              "bg-white border-[#E3E5E5] border text-primary  hover:text-primaryDark min-w-[120px]"
            }
            icon="add-white"
            classIcon="bg-primary hover:bg-primaryDark"
          />
        </div>
      </div>

      {/* content */}
      <div
        onClick={handleClick}
        className="border-t border-[#F2F2F2] px-[14px] py-6 space-y-3"
      >
        <SystemItem
          percent={serverInfo?.cpu_percent || 0}
          name={"CPU"}
          unit={"GHz/s"}
        />
        <SystemItem
          percent={serverInfo?.ram_percent || 0}
          name={"RAM"}
          unit={"GB"}
          value={serverInfo?.ram_total ?? 0}
        />
        {serverInfo?.list_gpu &&
          serverInfo?.list_gpu.length > 0 &&
          serverInfo.list_gpu.map((gpu) => {
            return (
              <SystemItem
                key={gpu.gpu_id}
                percent={gpu?.gpu_memory_utilization ?? 0}
                name={"GPU"}
                unit={"GHz"}
                value={gpu?.gpu_memory_total ?? 0}
                subName={gpu?.gpu_name ?? ""}
              />
            );
          })}

        <SystemItem
          percent={serverInfo?.disk_percent ?? 0}
          name={"Dung lượng ổ đĩa"}
          unit={"GB"}
          value={serverInfo?.disk_total ?? 0}
        />
      </div>
      {/*  */}

      {/* update dialog */}
      {openEditDialog && (
        <CreateServerDialog
          open={openEditDialog}
          handleClose={() => setOpenEditDialog(false)}
          submit={handleUpdate}
          server={props.data}
        />
      )}

      {/* remove dialog  openRemoveDialog*/}
      {openRemoveDialog && (
        <DialogConfirm
          close={() => setOpenRemoveDialog(false)}
          action={handleRemove}
          image={"/icons/bin.svg"}
          title={"Bạn chắc chắn xoá không?"}
          description={"Sau khi xoá, dữ liệu sẽ không được phục hồi."}
        />
      )}

      <CreateServiceDialog
        open={openCreateServiceDialog}
        handleClose={function (): void {
          setOpenCreateServiceDialog(false);
        }}
        submit={handleCreateService}
      />
    </div>
  );
}
