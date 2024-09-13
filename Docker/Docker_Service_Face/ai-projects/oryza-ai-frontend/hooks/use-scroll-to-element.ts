import { generateURLWithQueryParams } from "@/utils/global-func";
import { useSearchParams } from "next/navigation";
import { useRouter } from "next/router";
import { useEffect, useMemo } from "react";

type OnClickHandler = (basePath: string, index: string) => void;

// Custom hook to handle scrolling to an element based on index in URL params
const useScrollToElement = (onClickHandler?: OnClickHandler) => {
  // Get search params from the current URL
  const searchParamAction = useSearchParams();
  const router = useRouter();

  // Memoized search params to avoid unnecessary computations
  const searchParams: { page: string | null } = useMemo(() => {
    let result: any = {};

    // Define keys to extract from search params
    const searchParamKeys = ["page", "search", "index"];

    // Iterate through keys and retrieve values from search params
    searchParamKeys.forEach((key) => {
      const value = searchParamAction.get(key);
      if (value) {
        result[key] = value;
      }
    });

    return result;
  }, [searchParamAction]);

  // Effect to scroll to element based on 'index' param in URL
  useEffect(() => {
    // Parse search params from current route
    const searchParams = new URLSearchParams(router.asPath.split("?")[1] || "");
    const index = searchParams.get("index");

    // If 'index' param exists, scroll to corresponding element
    if (index && typeof window !== "undefined") {
      const element = document.getElementById(index);
      if (element) {
        element.scrollIntoView({ behavior: "smooth", block: "center" });
      }
    }
  }, [router.asPath]);

  // Function to push route with updated 'index' param
  const handlePushRoute: OnClickHandler = (basePath, id) => {
    // Generate URL with updated query params including 'index'
    const url = generateURLWithQueryParams(basePath, {
      ...(searchParams as any),
      ["index"]: id,
    });

    // Replace current route with the new URL
    router.replace(url);

    // Call onClickHandler if provided
    if (onClickHandler) {
      onClickHandler(basePath, id);
    }
  };

  // Return handlePushRoute function for external use
  return { handlePushRoute };
};

export default useScrollToElement;
