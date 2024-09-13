import { authApi } from "@/api-client";
import { OpactityAnimation, SeoPage } from "@/components/common";
import ImageFallback from "@/components/common/image-fallback";
import { DialogConfirm } from "@/components/dialog/confirm-dialog";
import { AVATAR_URL } from "@/constants/avatar";
import { EmailComponents } from "@/containers/profile/email";
import { ProfileItem } from "@/containers/profile/item";
import { PasswordComponents } from "@/containers/profile/password";
import { useAuth } from "@/hooks/auth-hook";
import HomeLayout from "@/layouts/home";
import Image from "next/image";
import { enqueueSnackbar } from "notistack";
import { useState } from "react";

export interface IProfilePageProps {}

export default function ProfilePage(props: IProfilePageProps) {
  const { profile, logout } = useAuth();

  const [confirmDialog, setConfirmDialog] = useState(false);

  const handleDeleteUser = () => {
    if (profile?.id) {
      authApi
        .delelteUser(profile.id)
        .then((res) => {
          logout();
        })
        .catch((error) => {
          enqueueSnackbar(
            error?.response?.data?.detail ?? "Xóa tài khoản không thành công",
            {
              variant: "error",
            }
          );
        });
    }
  };

  return (
    <section className="p-[24px] h-full">
      <SeoPage title="Thông tin tài khoản" />
      <OpactityAnimation className="h-full shadow-shadown1 rounded-[16px] relative overflow-hidden ">
        {/* title */}
        <div className="px-8 py-6 bg-aquaTranquil -z-0">
          <p className="text-xl leading-6 font-medium text-white">
            Thông tin tài khoản
          </p>
        </div>
        {/* content */}
        <div className="h-full p-8 ">
          {/* avatar */}
          <div className="flex flex-row justify-between items-start  ">
            <div className="flex flex-row space-x-6 items-center pb-6">
              <div className="rounded-full relative shadow-shadown2">
                <ImageFallback
                  fallbackSrc={AVATAR_URL}
                  src={profile?.avatar || ""}
                  width={70}
                  height={70}
                  alt={"avatar"}
                  style={{
                    borderRadius: "50%",
                  }}
                />
                <Image
                  src="/icons/add-new.svg"
                  width={20}
                  height={20}
                  alt={"icon"}
                  className="absolute bottom-1 left-2/4 -translate-x-2/4 "
                />
              </div>
              <div>
                <p className="text-grayOz text-xl font-medium ">
                  {profile?.full_name ?? profile?.username}
                </p>
                <p className="text-grayOz text-[16px] font-medium ">
                  {profile?.company?.name ?? ""}
                </p>
              </div>
            </div>
            <div
              onClick={() => logout()}
              className="shadow-shadown1 px-3 py-2 rounded-lg flex flex-row space-x-2 select-none cursor-pointer "
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="20"
                height="21"
                viewBox="0 0 20 21"
                fill="none"
              >
                <path
                  d="M12.4999 9.66679C12.0391 9.66679 11.6666 9.29341 11.6666 8.83351L11.6666 5.5001C11.6666 5.04097 11.2933 4.66682 10.8332 4.66682L8.33323 4.66682L8.33323 17.1667C8.33323 17.8784 7.87989 18.5142 7.19829 18.7509L6.95155 18.8334L10.8332 18.8334C11.2933 18.8334 11.6666 18.4593 11.6666 18L11.6666 15.5C11.6666 15.0401 12.0391 14.6668 12.4999 14.6668C12.9607 14.6668 13.3332 15.0401 13.3332 15.5L13.3332 18C13.3332 19.3783 12.2115 20.5 10.8332 20.5L1.87499 20.5C1.84325 20.5 1.8167 20.4858 1.78588 20.4817C1.74575 20.485 1.70745 20.5 1.66671 20.5C0.747523 20.5 1.30674e-07 19.7526 2.9139e-07 18.8334L2.91406e-06 3.83354C3.03849e-06 3.12188 0.453339 2.48605 1.13494 2.24939L6.15002 0.577645C6.32 0.525155 6.48907 0.500131 6.66668 0.500131C7.58586 0.500131 8.33323 1.24765 8.33323 2.16684L8.33323 3.00012L10.8332 3.00012C12.2115 3.00012 13.3332 4.12178 13.3332 5.5001L13.3332 8.83351C13.3332 9.29341 12.9607 9.66679 12.4999 9.66679Z"
                  fill="#007DC0"
                />
                <path
                  d="M19.7555 12.7558L16.4221 16.0891C16.1839 16.3274 15.8255 16.3992 15.5139 16.2701C15.2031 16.1408 14.9997 15.8367 14.9997 15.5L14.9997 13L11.6664 13C11.2064 13 10.833 12.6268 10.833 12.1667C10.833 11.7067 11.2064 11.3334 11.6664 11.3334L14.9997 11.3334L14.9997 8.83345C14.9997 8.49669 15.2031 8.19258 15.5139 8.06334C15.8255 7.93425 16.1839 8.00597 16.4221 8.24416L19.7555 11.5776C20.0813 11.9033 20.0813 12.4301 19.7555 12.7558Z"
                  fill="#007DC0"
                />
              </svg>
              <p>Đăng xuất</p>
            </div>
          </div>
          {/* email */}
          <EmailComponents />
          <PasswordComponents />
          {/* <ProfileItem
            title={"Duy trì đăng nhập"}
            summary={
              "Nếu bạn tắt trình duyệt. Tài khoản của bạn có thể đăng nhập lại mà không cần nhập lại mật khẩu"
            }
          >
            <SwitchBtn />
          </ProfileItem> */}
          <ProfileItem
            title={"Xoá tài khoản"}
            summary={
              "Toàn bộ dữ liệu của bạn sẽ mất đi và không khôi phục lại được."
            }
          >
            <button
              onClick={() => setConfirmDialog(true)}
              className="px-3 py-2 rounded-lg bg-white text-[#EF5350] text-[14px] font-medium hover:text-[#F95959] hover:shadow-shadown1 transition-all duration-300"
            >
              Xóa
            </button>
          </ProfileItem>
        </div>
      </OpactityAnimation>

      {confirmDialog && (
        <DialogConfirm
          close={() => setConfirmDialog(false)}
          action={handleDeleteUser}
          image={"/icons/bin.svg"}
          title={"Bạn chắc chắn xoá không?"}
          description={"Sau khi xoá, dữ liệu sẽ không được phục hồi."}
        />
      )}
    </section>
  );
}
ProfilePage.Layout = HomeLayout;
