import { serviceTypeApi } from "@/api-client/setting";
import { webhookApi } from "@/api-client/setting/webhook";
import { ServerRes } from "@/interfaces/server";
import { WebhookRes } from "@/interfaces/webhook";
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

export type WebhookContextType = {
  data: WebhookRes[];
  setData: Dispatch<SetStateAction<WebhookRes[]>>;
  total: number;
  setTotal: Dispatch<SetStateAction<number>>;
  textSearch: string;
  setTextSearch: Dispatch<SetStateAction<string>>;
};

export const WebhookContext = createContext({} as WebhookContextType);

type TProps = {
  children: React.ReactNode;
};

export const WebhookProvider = ({ children }: TProps) => {
  const [data, setData] = useState<WebhookRes[]>([]);
  const [total, setTotal] = useState(0);
  const [textSearch, setTextSearch] = useState("");
  const [debounced] = useDebouncedValue(textSearch, 500);

  const getCount = async () => {
    await webhookApi
      .getCount({ data_search: textSearch })
      .then((res: any) => {
        setTotal(Number(res.data?.count ?? 0));
      })
      .catch((e) => {
        console.log("get count webhoo Error: ", e);
      });
  };

  useEffect(() => {
    getCount();
  }, [debounced]);

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
    <WebhookContext.Provider value={value}>{children}</WebhookContext.Provider>
  );
};

export const useWebhook = () => useContext(WebhookContext);
