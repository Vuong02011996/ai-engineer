import { SeoPage } from "@/components/common";
import { LoginForm } from "@/components/forms/login";
import Image from "next/image";

export interface ILoginPageProps {}

export default function LoginPage(props: ILoginPageProps) {
  return (
    <div className="w-screen h-screen items-center justify-between bg-white flex flex-col pt-[5%] pb-[30px] ">
      <SeoPage title="Đăng nhập" />
      <Image
        src="/images/logo-oryza.png"
        width={160}
        height={94}
        alt="logo"
        className="scale-[2]"
      />

      <LoginForm />
      <footer className="flex flex-col items-center">
        <Image
          src="/images/logo-oryza-small.png"
          width={80}
          height={80}
          alt="logo"
        />
        <p className="text-xs font-normal text-grayOz">
          © 2024 Bản quyền thuộc Oryza JSC. Bảo lưu mọi quyền.
        </p>
      </footer>
    </div>
  );
}
