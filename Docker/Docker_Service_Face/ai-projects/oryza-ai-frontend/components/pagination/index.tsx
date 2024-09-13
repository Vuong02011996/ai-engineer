import NextIcon from "@/assets/svgs/next-gray.svg";
import { Pagination, styled } from "@mui/material";
import * as React from "react";

export interface IPaginateCustomProps {
  total?: number;
  count?: number;
  maxPage: number;
  page: number;
  onChangePage: (event: any, page: number) => void;
  searchPage?: string;
  onSearch?: React.ChangeEventHandler<HTMLInputElement> | undefined;
  handlerSearchPage: React.MouseEventHandler<HTMLButtonElement> | undefined;
}

export default function PaginateCustom(props: IPaginateCustomProps) {
  const {
    maxPage,
    page,
    onChangePage,
    searchPage,
    onSearch,
    handlerSearchPage,
  } = props;
  return (
    <div className="h-[60px] flex flex-row justify-between items-center px-8 py-[14px] ">
      <div>
        <p className="text-sm font-normal text-[#808080]">
          <span className="text-[16px] font-bold text-primary">
            {props.count ?? 0}
          </span>
          <span className="text-[16px] font-bold text-grayOz">
            /{props.total ?? 0}
          </span>{" "}
          dữ liệu
        </p>
      </div>

      <Pagination
        count={maxPage}
        page={page}
        onChange={onChangePage}
        shape="rounded"
        variant="text"
        boundaryCount={1}
        siblingCount={0}
        sx={{
          ".MuiPaginationItem-root": {
            color: "#55595d",
            background: "transparent",
            fontSize: 14,
            fontWeight: 500,
            ":hover": {
              background: "#78C6E7 !important",
              color: "#fff",
            },
          },
          ".Mui-selected": {
            color: "white",
            background: "#78C6E7 !important",
            fontSize: 14,
            fontWeight: 500,
          },
          transition: "all .3s",
        }}
      />
      <div className="flex flex-row space-x-3 items-center ">
        <p>Trang</p>
        <input
          value={searchPage}
          onChange={onSearch}
          type="number"
          placeholder={page.toString()}
          className="bg-transparent outline-none text-[#808080] font-medium text-base w-[56px] border border-[#CDD2D1] rounded-md text-center "
        />
        <button
          onClick={handlerSearchPage}
          className="bg-[#CDD2D1] rounded-lg w-8 h-8 flex items-center justify-center opacity-20 hover:opacity-100 transition-all duration-300 "
        >
          <NextIcon />
        </button>
      </div>
    </div>
  );
}
