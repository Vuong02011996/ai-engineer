import Icon from "@/components/common/icon";
import Link from "next/link";
import * as React from "react";
import styles from "./style.module.css";
import { useState } from "react";
import Logo from "@/assets/svgs/small-logo.svg";
import { useMediaQuery, useTheme } from "@mui/material";

export interface ILogoBoxProps {
  toggleMenu: () => void;
  openMenu: boolean;
}

export function LogoBox({ toggleMenu, openMenu }: ILogoBoxProps) {
  const theme = useTheme();
  const mdScreen = useMediaQuery(theme.breakpoints.down("lg"));
  return (
    <div
      className={`flex z-50 items-center rounded-[8px] cursor-pointer space-x-[16px] transition-all duration-300 ease-in-out  justify-start relative ${styles.logo}`}
    >
      <div>
        <Logo
          onClick={toggleMenu}
          className="   fill-[#78C6E7]  w-[50px] h-[50px] "
        />
      </div>
      <p className="flex-1 text-white font-medium  text-[24px] truncate">
        Oryza AI
      </p>
      {!mdScreen && (
        <div
          title={"Mở rộng"}
          onClick={toggleMenu}
          className={
            openMenu
              ? "hidden"
              : `absolute top-[50%]  right-[-60px] bg-[#323232] p-[10px] translate-y-[-50%] rounded-[8px] ${styles.menuIcon} transition-all duration-300`
          }
        >
          <Icon name="menu" className="   fill-[#CDD2D1]  w-[28px] h-[28px]" />
        </div>
      )}

      <div
        title={"Thu gọn"}
        id="menu-icon"
        onClick={toggleMenu}
        className={openMenu ? "" : "hidden"}
      >
        <Icon name="menu" className="   fill-[#CDD2D1]  w-[28px] h-[28px]" />
      </div>
    </div>
  );
}
