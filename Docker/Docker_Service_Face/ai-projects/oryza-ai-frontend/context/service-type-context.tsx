import { serviceTypeApi } from "@/api-client/setting";
import { ServerRes } from "@/interfaces/server";
import { TypeServiceRes } from "@/interfaces/type-service";
import { useDebouncedValue } from "@mantine/hooks";
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

export type TypeServiceContextType = {
  data: TypeServiceRes[];
  setData: Dispatch<SetStateAction<TypeServiceRes[]>>;
  total: number;
  setTotal: Dispatch<SetStateAction<number>>;
  textSearch: string;
  setTextSearch: Dispatch<SetStateAction<string>>;
};

export const TypeServiceContext = createContext({} as TypeServiceContextType);

type TProps = {
  children: React.ReactNode;
};

export const TypeServiceProvider = ({ children }: TProps) => {
  const [data, setData] = useState<TypeServiceRes[]>([]);
  const [total, setTotal] = useState(0);
  const [textSearch, setTextSearch] = useState("");
  const [debounced] = useDebouncedValue(textSearch, 500);

  const getCount = useCallback(async () => {
    await serviceTypeApi
      .getCount({ data_search: textSearch })
      .then((res: any) => {
        setTotal(Number(res.data?.count ?? 0));
      })
      .catch((e) => {
        console.log("get count  Error: ", e);
      });
  }, [debounced]);

  useEffect(() => {
    getCount();
  }, [getCount]);

  const value = useMemo(
    () => ({
      data,
      setData,
      total,
      setTotal,
      textSearch,
      setTextSearch,
    }),
    [data, setData, setTotal, total, textSearch, setTextSearch]
  );

  return (
    <TypeServiceContext.Provider value={value}>
      {children}
    </TypeServiceContext.Provider>
  );
};

export const useTypeService = () => useContext(TypeServiceContext);
