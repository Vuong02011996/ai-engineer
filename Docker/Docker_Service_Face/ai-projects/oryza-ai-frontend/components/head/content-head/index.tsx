import addBlueIcon from "@/assets/svgs/add-blue.svg";
import BackIcon from "@/assets/svgs/back-white.svg";
import gridIcon from "@/assets/svgs/grid.svg";
import listIcon from "@/assets/svgs/list.svg";
import { BigBtn } from "@/components/common";
import { ActionItem } from "@/components/file-action/item";
import { TabInterface } from "@/interfaces/tab";
import { Tabs, Tab, tabsClasses } from "@mui/material";
import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/navigation";
import * as React from "react";
import { useAuth } from "@/hooks/auth-hook";

export interface IHeadContentProps {
  title: string;
  subTitle?: string;
  subTitleApostrophe?: string;
  showGrid?: boolean;
  rootPage?: string;
  onClickCreatebtn?: () => void;
  onClickUpdatebtn?: () => void;
  hiddenCreateBtn?: boolean;
  hiddenUpdateBtn?: boolean;
  tabData?: TabInterface[];
  handleChangeTab?: (tab: any) => void;
  tabIndex?: string;
  children?: React.ReactNode;
  tabChildren?: React.ReactNode;
  showType?: "GRID" | "LIST";
}

export function HeadContent(props: IHeadContentProps) {
  const { profile } = useAuth();
  const currentUser = profile?.is_admin ? "ADMIN" : "USER";
  const {
    title,
    subTitle,
    showGrid,
    rootPage,
    onClickCreatebtn,
    onClickUpdatebtn,
    tabData,
    subTitleApostrophe,
  } = props;
  const showType = props.showType ?? "LIST";
  const router = useRouter();
  const [value, setValue] = React.useState(0);
  const handleChange = (event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };
  return (
    <div>
      <div className="h-[72px] px-[32px] py-[16px] flex flex-row justify-between items-center ">
        {/* title */}
        {subTitle ? (
          <div className="flex flex-row space-x-4 items-center ">
            <button
              onClick={() => router.back()}
              className="bg-[#808080] rounded-md w-6 h-6 flex items-center justify-center "
            >
              <BackIcon />
            </button>
            <Link href={rootPage ?? "#"}>
              <h1 className="text-primary text-[16px] font-medium md:text-xl truncate ">
                {title}
              </h1>
            </Link>
            <p className="text-[16px] md:text-xl  font-normal text-[#AFAFAF]">
              /
            </p>
            {subTitle && (
              <h1 className="text-blackOz text-[16px] md:text-xl font-medium truncate">
                {subTitle}
              </h1>
            )}
          </div>
        ) : subTitleApostrophe ? (
          <div className="flex flex-row space-x-4 items-center ">
            <button
              onClick={() => router.back()}
              className="bg-[#808080] rounded-md w-6 h-6 flex items-center justify-center "
            >
              <BackIcon />
            </button>
            <h1 className="text-blackOz text-[16px] md:text-xl font-medium truncate">
              {title} “
              <span className="text-primary">{subTitleApostrophe}</span>”
            </h1>
          </div>
        ) : (
          <h1 className="text-blackOz text-[16px] md:text-xl font-medium truncate">
            {title}
          </h1>
        )}

        {/* right */}
        <div className="flex flex-row space-x-[16px]  ">
          {showGrid && (
            <div className="flex flex-row p-[4px] rounded-[8px] bg-[#F2F2F2]">
              <ActionItem
                active={showType === "GRID"}
                onClick={() => {}}
                icon={gridIcon}
              />
              <ActionItem
                active={showType === "LIST"}
                onClick={() => {}}
                icon={listIcon}
              />
            </div>
          )}
          {props.children && props.children}

          {props.hiddenCreateBtn != true && profile?.is_admin && (
            <BigBtn
              text={"Tạo mới"}
              icon={addBlueIcon}
              className={
                "bg-primary hover:bg-[#026DA6] text-white h-10 truncate"
              }
              classIcon="bg-white"
              onClick={onClickCreatebtn}
            />
          )}
        </div>
      </div>
      {tabData && (
        <div className="h-10 flex flex-row px-5 justify-between items-center space-x-3">
          <Tabs
            value={value}
            onChange={handleChange}
            variant="scrollable"
            scrollButtons
            aria-label="scrollable auto tabs example"
            sx={{
              "& .MuiTabs-indicator": {
                display: "flex",
                justifyContent: "center",
                backgroundColor: "transparent",
              },
              [`& .${tabsClasses.scrollButtons}`]: {
                "&.Mui-disabled": { display: "none" },
                height: "40px",
              },
            }}
          >
            {tabData.map((tab) => {
              let active = tab.id === props?.tabIndex;

              // if current user is not admin, hide setting role tab
              if (tab.id === "4" && tab.role && !tab.role.includes(currentUser)) {
                return null;
              }

              return (
                <Tab
                  key={tab.id}
                  disableRipple
                  onClick={() => {
                    if (props.handleChangeTab) {
                      props.handleChangeTab(tab);
                    }
                  }}
                  label={
                    <p
                      className={[
                        "text-[16px] font-semibold transition-all duration-200  truncate normal-case",
                        `${active ? "text-primary" : "text-blackOz"}`,
                      ].join(" ")}
                    >
                      {tab.name}
                    </p>
                  }
                  iconPosition="start"
                  icon={
                    <Image
                      src={active ? tab.iconActive : tab.icon}
                      width={24}
                      height={24}
                      alt="icon"
                      className="mr-2"
                    />
                  }
                  sx={{
                    overflow: "hidden",
                    minHeight: "40px",
                    height: "40px",
                    borderRadius: "8px",
                    transition: "all .2s ease-in-out",
                    cursor: "pointer",
                    padding: "8px",
                    marginX: "8px",
                    userSelect: "none",
                    background: active ? "#EAF6FC" : "transparent",
                    ":hover": {
                      background: !active ? "#F2F2F2" : "transparent",
                    },
                  }}
                />
              );
            })}
          </Tabs>
          {props.tabChildren && (
            <div className="flex flex-row space-x-3 ">{props.tabChildren}</div>
          )}
        </div>
      )}
      {/* {tabData && (
        <div className="h-10 flex flex-row px-8 justify-between items-center space-x-3 ">
          <Scrollbar autoHide>
            <div className="flex flex-row space-x-3 flex-1 ">
              {tabData.map((tab) => {
                let active = tab.id === props?.tabIndex;

                return (
                  <div
                    onClick={() => {
                      if (props.handleChangeTab) {
                        props.handleChangeTab(tab);
                      }
                    }}
                    key={tab.id}
                    className={[
                      "h-10 rounded-lg transition-all duration-200 cursor-pointer flex items-center space-x-2 p-2 select-none   ",
                      `${active ? "bg-[#EAF6FC]" : "hover:bg-[#F2F2F2]"}`,
                    ].join(" ")}
                  >
                    <Image
                      src={active ? tab.iconActive : tab.icon}
                      width={24}
                      height={24}
                      alt="icon"
                    />
                    <p
                      className={[
                        " text-[16px] font-semibold transition-all duration-200  truncate",
                        `${active ? "text-primary" : "text-blackOz"}`,
                      ].join(" ")}
                    >
                      {tab.name}
                    </p>
                  </div>
                );
              })}
            </div>
          </Scrollbar>
          {props.tabChildren && (
            <div className="flex flex-row space-x-3 ">{props.tabChildren}</div>
          )}
        </div>
      )} */}
    </div>
  );
}
