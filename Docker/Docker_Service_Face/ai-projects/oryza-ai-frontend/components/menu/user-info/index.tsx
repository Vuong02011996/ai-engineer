import * as React from "react";
import Image from "next/image";
import Icon from "@/components/common/icon";
import { useAuth } from "@/hooks/auth-hook";
import { useRouter } from "next/navigation";
import { AVATAR_URL } from "@/constants/avatar";
import ImageFallback from "@/components/common/image-fallback";

export interface IUserInfoProps {
  openMenu: boolean;
}

export function UserInfo({ openMenu }: IUserInfoProps) {
  const { profile } = useAuth();
  const router = useRouter();

  return (
    <div
      onClick={() => router.push("/profile")}
      className={`${
        openMenu
          ? "px-[16px]  bg-[#64686D] hover:bg-blackOz rounded-[8px] flex flex-row space-x-[16px] items-center  "
          : ""
      }    overflow-hidden py-[24px] transition-all duration-300 cursor-pointer`}
    >
      <div className="relative w-[50px] h-[50px] min-w-[50px] border-2 border-white rounded-full">
        <ImageFallback
          fallbackSrc={AVATAR_URL}
          className="object-cover w-full h-full rounded-full "
          src={profile?.avatar || ""}
          alt="avatar user"
          fill
          priority
        />
        <div className="w-[10px] h-[10px] rounded-full bg-[#B5FFC1] top-0 right-0 absolute"></div>
      </div>

      <div
        className={
          openMenu ? "relative w-[40px] h-[40px] min-w-[40px] flex-1" : "hidden"
        }
      >
        <p className="font-medium text-[16px] text-white ">
          {profile?.full_name ?? profile?.username}
        </p>
        <p className="font-medium text-[12px] text-[#CDD2D1] ">
          {profile?.email}
        </p>
      </div>
      <div className={openMenu ? "" : "hidden"}>
        <Icon name={"more-vertical"} />
      </div>
    </div>
  );
}
