import { Popover } from "@mui/material";
import * as React from "react";
import { useState } from "react";
import Image from "next/image";

export interface IFilterSmallIconProps {
  options: {
    id: number;
    name: string;
    key: string;
  }[];
  onChange: (value: any) => void;
}

export function FilterSmallIcon(props: IFilterSmallIconProps) {
  const { options, onChange } = props;

  const [anchorEl, setAnchorEl] = React.useState<HTMLButtonElement | null>(
    null
  );

  const handleClick = (event: any) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const open = Boolean(anchorEl);
  const id = open ? "simple-popover" : undefined;

  const [value, setValue] = useState("ALL");

  const displayName = React.useCallback(() => {
    return options.find((i) => i.key === value)?.name ?? "";
  }, [value]);

  return (
    <div title="Bộ lọc">
      <div
        onClick={handleClick}
        className={[
          "px-3 py-2 rounded-lg border-2   bg-white transition-all duration-300 h-10 flex flex-row items-center space-x-1 cursor-pointer",
          open ? " border-[#78C6E7]" : "shadow-shadown1 border-transparent",
        ].join(" ")}
      >
        <Image
          src="/icons/filter-icon.svg"
          width={20}
          height={20}
          alt="filter"
        />
      </div>
      <Popover
        id={id}
        open={open}
        anchorEl={anchorEl}
        onClose={handleClose}
        anchorOrigin={{
          vertical: "bottom",
          horizontal: "right",
        }}
        transformOrigin={{
          vertical: "top",
          horizontal: "right",
        }}
        slotProps={{
          paper: {
            sx: {
              mt: "4px",
              borderRadius: "8px",
              overflow: "hidden",
              minWidth: "135px",
            },
          },
        }}
      >
        {options.map((item) => {
          const isActive = item.key === value;
          return (
            <div
              key={item.id}
              onClick={() => {
                setValue(item.key);
                onChange(item.key);
              }}
              className={[
                "px-2 py-1   cursor-pointer flex flex-row items-center justify-between  transition-all duration-300",
                isActive ? "bg-[#55595d]  " : "bg-white hover:bg-[#F2F2F2]",
              ].join(" ")}
            >
              <p
                className={[
                  "font-medium text-[14px] ",
                  isActive ? "  text-white" : "  text-[#808080]",
                ].join(" ")}
              >
                {item.name}
              </p>
              {isActive && (
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="16"
                  height="16"
                  viewBox="0 0 16 16"
                  fill="none"
                >
                  <path
                    fillRule="evenodd"
                    clipRule="evenodd"
                    d="M13.8048 4.19526C14.0651 4.45561 14.0651 4.87772 13.8048 5.13807L7.13815 11.8047C6.87781 12.0651 6.45569 12.0651 6.19534 11.8047L2.86201 8.4714C2.60166 8.21107 2.60166 7.78893 2.86201 7.5286C3.12236 7.26827 3.54447 7.26827 3.80482 7.5286L6.66675 10.3905L12.862 4.19526C13.1223 3.93491 13.5445 3.93491 13.8048 4.19526Z"
                    fill="white"
                  />
                </svg>
              )}
            </div>
          );
        })}
      </Popover>
    </div>
  );
}
