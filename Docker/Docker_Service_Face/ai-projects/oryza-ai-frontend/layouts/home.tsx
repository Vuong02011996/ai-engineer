import { MenuBar } from "@/components";
import { useAuth } from "@/hooks/auth-hook";
import { useRouter } from "next/router";
import * as React from "react";
import { useEffect } from "react";
export interface IHomeLayoutProps {
  children: React.ReactNode;
}

export default function HomeLayout({ children }: IHomeLayoutProps) {
  const { firstLoading, profile } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (firstLoading) return;

    if (!profile) {
      router.replace("/login");
    }
  }, [profile, firstLoading]);

  return (
    <div className="w-screen h-screen bg-white flex flex-row">
      <nav className="flex-none h-full pt-[16px] pl-[16px] pb-[16px] ">
        <MenuBar />
      </nav>
      <main className="flex-1 overflow-hidden">{children}</main>
    </div>
  );
}
