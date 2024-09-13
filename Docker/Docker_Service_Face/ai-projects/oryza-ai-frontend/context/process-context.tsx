import { CameraRes } from "@/interfaces/camera";
import { PorcessRes } from "@/interfaces/process";
import { ServerRes } from "@/interfaces/server";
import {
  Dispatch,
  SetStateAction,
  createContext,
  useContext,
  useMemo,
  useState,
} from "react";

export type ProcessContextType = {
  data: PorcessRes[];
  setData: Dispatch<SetStateAction<PorcessRes[]>>;
  camera: CameraRes | null;
  setCamera: Dispatch<SetStateAction<CameraRes | null>>;
  searchData: PorcessRes[];
  setSearchData: Dispatch<SetStateAction<PorcessRes[]>>;
  searchKey: string;
  setSearchKey: Dispatch<SetStateAction<string>>;
};

export const ProcessContext = createContext({} as ProcessContextType);

type TProps = {
  children: React.ReactNode;
};

export const ProcessProvider = ({ children }: TProps) => {
  const [data, setData] = useState<PorcessRes[]>([]);
  const [camera, setCamera] = useState<CameraRes | null>(null);
  const [searchData, setSearchData] = useState<PorcessRes[]>([]);
  const [searchKey, setSearchKey] = useState("");

  const value = useMemo(
    () => ({
      data,
      setData,
      camera,
      setCamera,
      searchData,
      setSearchData,
      searchKey,
      setSearchKey,
    }),
    [
      data,
      setData,
      camera,
      setCamera,
      searchData,
      setSearchData,
      searchKey,
      setSearchKey,
    ]
  );

  return (
    <ProcessContext.Provider value={value}>{children}</ProcessContext.Provider>
  );
};

export const useProcess = () => useContext(ProcessContext);
