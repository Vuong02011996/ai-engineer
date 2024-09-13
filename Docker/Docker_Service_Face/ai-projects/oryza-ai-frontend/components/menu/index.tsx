import menus from "@/data/menu";
import Link from "next/link";
import { useRouter } from "next/router";
import { useState } from "react";
import { LogoBox } from "./logo-box";
import { MenuItem } from "./menu-item";
import { SearchBox } from "./search";
import { UserInfo } from "./user-info";
import { useMediaQuery, useTheme } from "@mui/material";
import { useAuth } from "@/hooks/auth-hook";
import { UserRole } from "@/constants/role";

export interface IMenuBarProps {}

export function MenuBar(props: IMenuBarProps) {
  const [openMenu, setOpenMenu] = useState(true);
  const { pathname } = useRouter();
  const { profile } = useAuth();

  const path = pathname.split("/")[1];

  const toggleMenu = () => {
    setOpenMenu(!openMenu);
  };

  const theme = useTheme();
  const mdScreen = useMediaQuery(theme.breakpoints.down("lg"));

  const width = mdScreen ? "w-[90px]" : openMenu ? "w-[308px]" : "w-[90px]";

  return (
    <div
      className={`${width} h-full flex-col flex  bg-[#55595D]  transition-all duration-300 ease-in-out px-[20px] py-[40px] space-y-[32px] rounded-[16px]`}
    >
      <LogoBox toggleMenu={toggleMenu} openMenu={mdScreen ? false : openMenu} />

      <SearchBox />

      <div className="flex-1">
        {menus.map((menu) => {
          if (
            (menu.role === UserRole.ADMIN && profile?.is_admin !== true) ||
            (menu.role === UserRole.SUPER_ADMIN && profile?.is_superuser !== true)
          ) {
            return <div key={menu.id}></div>;
          } else {
            return (
              <Link href={"/" + menu.path} key={menu.id}>
                <MenuItem
                  active={path === menu.path.split("/")[0]}
                  text={menu.name}
                  icon={menu.icon}
                />
              </Link>
            );
          }
        })}
      </div>

      <div className="space-y-[32px]">
        <div>
          <MenuItem text={"Hỗ trợ"} icon={"info"} />
          {(profile?.is_admin) && (
              <Link href={"/setting/service"}>
                <MenuItem
                  active={path === "setting"}
                  text={"Cài đặt"}
                  icon={"setting"}
                />
              </Link>
            )}
        </div>
        <UserInfo openMenu={mdScreen ? false : openMenu} />
      </div>
    </div>
  );
}
