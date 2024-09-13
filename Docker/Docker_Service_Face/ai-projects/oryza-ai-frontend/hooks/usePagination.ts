import { generateURLWithQueryParams } from "@/utils/global-func";
import { useRouter, useSearchParams } from "next/navigation";
import { useMemo } from "react";

export const usePaginationCustom = (total: number, limit: number) => {
  const searchParamAction = useSearchParams();
  const router = useRouter();

  const searchParams: { page: string | null } = useMemo(() => {
    let result: any = {};
    if (searchParamAction.get("page")) {
      result["page"] = searchParamAction.get("page");
    }
    if (searchParamAction.get("search")) {
      result["search"] = searchParamAction.get("search");
    }
    if (searchParamAction.get("index")) {
      result["index"] = searchParamAction.get("index");
    }

    return result;
  }, [searchParamAction]);

  const currentPage = useMemo(() => {
    return searchParams.page &&
      !Number.isNaN(Number(searchParams.page)) &&
      Number.isInteger(Number(searchParams.page))
      ? Number(searchParams.page) - 1
      : 0;
  }, [searchParams.page]);

  const maxPage = useMemo(() => {
    const sizePage = total === 0 ? 0 : Math.ceil(total / limit);
    return sizePage;
  }, [total, limit]);

  const setPage = (basePath: string, nextPage: number) => {
    const url = generateURLWithQueryParams(basePath, {
      ...(searchParams as any),
      ["page"]: nextPage,
    });

    router.replace(url);
  };

  return { currentPage, maxPage, searchParams, setPage };
};
