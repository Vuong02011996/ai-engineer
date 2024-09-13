import { cameraApi } from "@/api-client/camera";
import { CameraRes } from "@/interfaces/camera";
import { useDebouncedValue } from "@mantine/hooks";
import { useSearchParams } from "next/navigation";
import {
  Dispatch,
  SetStateAction,
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";

// Camera Context

export type CameraContextType = {
  data: CameraRes[];
  setData: Dispatch<SetStateAction<CameraRes[]>>;
  total: number;
  setTotal: Dispatch<SetStateAction<number>>;
};

export const CameraContext = createContext({} as CameraContextType);

// Camera Context Provider

type TProps = {
  children: React.ReactNode;
};

export const CameraProvider = ({ children }: TProps) => {
  const [data, setData] = useState<CameraRes[]>([]);
  const [total, setTotal] = useState(0);
  const searchParams = useSearchParams();

  const search = useCallback(() => {
    if (searchParams.has("search")) {
      return searchParams.get("search") || "";
    }
    return "";
  }, [searchParams]);

  const [debounce] = useDebouncedValue(search, 500);

  const getCount = async () => {
    await cameraApi
      .getCount({ data_search: search().trim() })
      .then((res: any) => {
        setTotal(Number(res.data?.count ?? 0));
      })
      .catch((e) => {
        console.log("get count  Error: ", e);
      });
  };

  useEffect(() => {
    getCount();
  }, [debounce]);

  const value = useMemo(
    () => ({
      data,
      setData,
      total,
      setTotal,
    }),
    [data, setData, setTotal, total]
  );

  return (
    <CameraContext.Provider value={value}>{children}</CameraContext.Provider>
  );
};

// Camera Context hooks

export const useCameras = () => useContext(CameraContext);
