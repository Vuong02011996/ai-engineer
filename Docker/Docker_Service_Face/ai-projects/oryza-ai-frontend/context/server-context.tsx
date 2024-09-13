import { ServerRes } from "@/interfaces/server";
import {
  Dispatch,
  SetStateAction,
  createContext,
  useContext,
  useMemo,
  useState,
} from "react";

export type ServerContextType = {
  data: ServerRes[];
  setData: Dispatch<SetStateAction<ServerRes[]>>;
};

export const ServerContext = createContext({} as ServerContextType);

type TProps = {
  children: React.ReactNode;
};

export const ServerProvider = ({ children }: TProps) => {
  const [data, setData] = useState<ServerRes[]>([]);

  const value = useMemo(
    () => ({
      data,
      setData,
    }),
    [data, setData]
  );

  return (
    <ServerContext.Provider value={value}>{children}</ServerContext.Provider>
  );
};

// Camera Context hooks

export const useServers = () => useContext(ServerContext);
