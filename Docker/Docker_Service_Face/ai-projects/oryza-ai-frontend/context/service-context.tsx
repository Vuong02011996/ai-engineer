import { serviceApi } from "@/api-client/service";
import { ServerRes } from "@/interfaces/server";
import { ServiceRes } from "@/interfaces/service";
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

export type ServiceContextType = {
  data: ServiceRes[];
  setData: Dispatch<SetStateAction<ServiceRes[]>>;
  total: number;
  setTotal: Dispatch<SetStateAction<number>>;
  serverData: ServerRes | null;
  setServerData: Dispatch<SetStateAction<ServerRes | null>>;
};

export const ServiceContext = createContext({} as ServiceContextType);

type TProps = {
  children: React.ReactNode;
};

export const ServiceProvider = ({ children }: TProps) => {
  const [data, setData] = useState<ServiceRes[]>([]);
  const [total, setTotal] = useState(0);
  const [serverData, setServerData] = useState<ServerRes | null>(null);

  const getCount = useCallback(async () => {
    if (!serverData) return;
    await serviceApi
      .getCountByServer({ server_id: serverData.id })
      .then((res: any) => {
        setTotal(Number(res.data?.count ?? 0));
      })
      .catch((error: any) => {
        console.log("error ", error);
      });
  }, [serverData]);

  useEffect(() => {
    getCount();
  }, [getCount]);

  const value = useMemo(
    () => ({
      data,
      setData,
      total,
      setTotal,
      serverData,
      setServerData,
    }),
    [data, setData, setTotal, total, serverData, setServerData]
  );

  return (
    <ServiceContext.Provider value={value}>{children}</ServiceContext.Provider>
  );
};

export const useService = () => useContext(ServiceContext);
