import NextIcon from "@/assets/svgs/next-gray.svg";
import {
  formatNumberWithCommas,
  generateURLWithQueryParams,
} from "@/utils/global-func";
import KeyboardArrowLeftRoundedIcon from "@mui/icons-material/KeyboardArrowLeftRounded";
import { Stack, Typography } from "@mui/material";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

interface ITablePaginationGlobalLog {
  total: number;
  currentPage: number;
  currentCount: number;
  maxPage: number;
  searchParams?: any;
  basePath: string;
}
export const PaginationTable = (props: ITablePaginationGlobalLog) => {
  const {
    total,
    currentCount,
    currentPage,
    maxPage,
    searchParams: searchParams,
    basePath,
  } = props;
  const router = useRouter();
  const [searchPage, setSearchPage] = useState("");
  const pageItem = (p: number, allowMobile: boolean) => {
    return (
      <Stack
        onClick={() => {
          if (currentPage + 1 === p) {
            return;
          }

          const url = generateURLWithQueryParams(basePath, {
            ...(searchParams as any),
            ["page"]: p.toString(),
          });
          setSearchPage(p.toString());

          router.replace(url);
        }}
        sx={{
          padding: "8px",
          width: { xs: "28px", md: "30px", xl: "32px" },
          height: { xs: "28px", md: "30px", xl: "32px" },
          // display: { xs: allowMobile ? 'flex' : 'none', sm: 'flex' },
          justifyContent: "center",
          alignItems: "center",
          gap: "10px",
          cursor: "pointer",
          borderRadius: "8px",
          transition: "all ease .3s",
          backgroundColor: currentPage + 1 === p ? "#78C6E7" : "transparent",
          "&:hover ":
            currentPage + 1 === p
              ? {}
              : {
                  backgroundColor: "#F1F1F1",
                  "& * ": {
                    color: "#007DC0",
                  },
                },
        }}
      >
        <Typography
          sx={{
            color: currentPage + 1 === p ? "#fff" : "#323232",
            fontSize: { xs: "12px", md: "13px", xl: "14px" },
            fontStyle: "normal",
            fontWeight: 500,
            lineHeight: "normal",
            userSelect: "none",
          }}
        >
          {p}
        </Typography>
      </Stack>
    );
  };

  const handlerSearchPage = async () => {
    let newPage = Number(searchPage) <= 0 ? 1 : Number(searchPage);

    const url = generateURLWithQueryParams(basePath, {
      ...(searchParams as any),
      ["page"]: newPage,
    });

    router.replace(url);
  };

  useEffect(() => {
    setSearchPage((currentPage + 1).toString());
    return () => {
      setSearchPage("");
    };
  }, [currentPage]);

  return (
    <Stack
      direction="row"
      alignItems="center"
      sx={{
        gap: "16px",
        width: "100%",
        position: "relative",
        height: "60px",
        px: "24px",
      }}
      justifyContent="space-between"
    >
      <div className="min-w-[100px]">
        <p className="text-sm font-normal text-[#808080]">
          <span className="text-[16px] font-bold text-primary">
            {currentCount ?? 0}
          </span>
          <span className="text-[16px] font-bold text-grayOz">
            /{formatNumberWithCommas(total || 0)}
          </span>{" "}
          dữ liệu
        </p>
      </div>

      <Stack
        sx={{ gap: { xs: "8px", md: "10px", xl: "12px" } }}
        alignItems="center"
        direction="row"
      >
        <Stack
          sx={{
            width: { xs: "28px", md: "30px", xl: "32px" },
            height: { xs: "28px", md: "30px", xl: "32px" },
            padding: "8px",
            justifyContent: "center",
            alignItems: "center",
            flexShrink: 0,
            userSelect: currentPage === 0 ? "none" : "initial",
            borderRadius: "10px",
            transition: "all ease .3s",
            cursor: "pointer",
            backgroundColor: "transparent",
            "&:hover ":
              currentPage !== 0
                ? {
                    backgroundColor: "#F1F1F1",
                    "& > *": {
                      color: "#007DC0",
                    },
                  }
                : {},
          }}
          justifyContent="center"
          alignItems="center"
          onClick={() => {
            if (currentPage === 0) {
              return;
            }
            const url = generateURLWithQueryParams(basePath, {
              ...(searchParams as any),
              ["page"]: currentPage.toString(),
            });

            router.replace(url);
          }}
        >
          <KeyboardArrowLeftRoundedIcon
            sx={{
              color: currentPage !== 0 ? "#55595D" : "#d9d9d9",
              transition: "all ease .3s",
            }}
          />
        </Stack>

        <Stack
          direction="row"
          sx={{
            gap: "4px",
            borderRadius: "44px",
          }}
          alignItems="center"
        >
          {currentPage > 2 ? (
            <>
              {pageItem(1, true)}
              <Typography
                sx={{
                  color: "#55595D",
                  fontSize: "14px",
                  fontStyle: "normal",
                  fontWeight: 500,
                  lineHeight: "normal",
                }}
              >
                ...
              </Typography>
            </>
          ) : (
            <></>
          )}

          {currentPage - 1 > 0 ? pageItem(currentPage - 1, false) : <></>}
          {currentPage > 0 ? pageItem(currentPage, false) : <></>}
          {pageItem(currentPage + 1, true)}
          {currentPage + 2 <= maxPage ? (
            pageItem(currentPage + 2, false)
          ) : (
            <></>
          )}
          {currentPage + 3 <= maxPage ? (
            pageItem(currentPage + 3, false)
          ) : (
            <></>
          )}

          {currentPage < maxPage - 3 ? (
            <>
              <Typography
                sx={{
                  color: "#55595D",
                  fontSize: "14px",
                  fontStyle: "normal",
                  fontWeight: 500,
                  lineHeight: "normal",
                }}
              >
                ...
              </Typography>
              {pageItem(maxPage, true)}
            </>
          ) : (
            <></>
          )}
        </Stack>

        <Stack
          sx={{
            width: { xs: "28px", md: "30px", xl: "32px" },
            height: { xs: "28px", md: "30px", xl: "32px" },
            padding: "8px",
            gap: "10px",
            flexShrink: 0,
            borderRadius: "10px",
            transition: "all ease .3s",
            cursor: "pointer",
            userSelect: currentPage === maxPage - 1 ? "none" : "initial",
            backgroundColor: "transparent",
            "&:hover ":
              currentPage === maxPage - 1
                ? {}
                : {
                    backgroundColor: "#F1F1F1",
                    "& > *": {
                      color: "#007DC0",
                    },
                  },
          }}
          justifyContent="center"
          alignItems="center"
          onClick={() => {
            if (currentPage < maxPage - 1) {
              const url = generateURLWithQueryParams(basePath, {
                ...(searchParams as any),
                ["page"]: (currentPage + 2).toString(),
              });

              router.replace(url);
            }
          }}
        >
          <KeyboardArrowLeftRoundedIcon
            sx={{
              color: currentPage === maxPage - 1 ? "#d9d9d9" : "#55595D",
              transform: "rotate(180deg)",
              transition: "all ease .3s",
            }}
          />
        </Stack>
      </Stack>
      <div className="flex flex-row space-x-3 items-center ">
        <p>Trang</p>
        <input
          value={searchPage}
          onChange={(e) => {
            let newPage = Number(e.target.value);
            if (newPage >= maxPage) newPage = maxPage;
            if (newPage <= 0) newPage = 1;
            setSearchPage(newPage.toString());
          }}
          type="number"
          placeholder={(currentPage + 1).toString()}
          className="bg-transparent outline-none text-[#808080] font-medium text-base w-[56px] border border-[#CDD2D1] rounded-md text-center "
        />
        <button
          onClick={handlerSearchPage}
          className="bg-[#CDD2D1] rounded-lg w-8 h-8 flex items-center justify-center opacity-20 hover:opacity-100 transition-all duration-300 "
        >
          <NextIcon />
        </button>
      </div>
    </Stack>
  );
};
