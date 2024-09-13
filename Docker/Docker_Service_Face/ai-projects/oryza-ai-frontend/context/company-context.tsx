import { companyApi } from "@/api-client/setting";
import { CompanyRes } from "@/interfaces/company";
import { useDebouncedValue } from "@mantine/hooks";
import {
  Dispatch,
  SetStateAction,
  createContext,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";

export type CompanyContextType = {
  data: CompanyRes[];
  setData: Dispatch<SetStateAction<CompanyRes[]>>;
  total: number;
  setTotal: Dispatch<SetStateAction<number>>;
  textSearch: string;
  setTextSearch: Dispatch<SetStateAction<string>>;
};

export const CompanyContext = createContext({} as CompanyContextType);

type TProps = {
  children: React.ReactNode;
};

export const CompanyProvider = ({ children }: TProps) => {
  const [data, setData] = useState<CompanyRes[]>([]);
  const [total, setTotal] = useState(0);
  const [textSearch, setTextSearch] = useState("");
  const [debounce] = useDebouncedValue(textSearch, 500);

  const getCount = async () => {
    await companyApi
      .getCount({ data_search: textSearch })
      .then((res: any) => {
        setTotal(Number(res.data?.count ?? 0));
      })
      .catch((e) => {
        console.log("get count company Error: ", e);
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
      textSearch,
      setTextSearch,
    }),
    [data, setData, total, setTotal, textSearch, setTextSearch]
  );

  return (
    <CompanyContext.Provider value={value}>{children}</CompanyContext.Provider>
  );
};

export const useSettingCompany = () => useContext(CompanyContext);
