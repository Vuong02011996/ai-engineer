import { serviceTypeApi } from "@/api-client/setting";
import { TabInterface } from "@/interfaces/tab";
import { TypeServiceRes } from "@/interfaces/type-service";
import { formatTypeService, typeServiceToTab } from "@/libs/format-data";
import { usePathname } from "next/navigation";
import { useRouter } from "next/router";
import {
  Dispatch,
  SetStateAction,
  createContext,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";

const currentTime = new Date();

export type ManageContextType = {
  tabData: TabInterface[];
  settabData: Dispatch<SetStateAction<TabInterface[]>>;
  startTime: Date;
  endTime: Date;
  setStartTime: Dispatch<SetStateAction<Date>>;
  setEndTime: Dispatch<SetStateAction<Date>>;
  textSearch: string;
  setTextSearch: Dispatch<SetStateAction<string>>;
  filter: any;
  setFilter: any;
  imagesList: string[];
  setImagesList: any;
  eventIds: string[];
  setEventIds: any;
  viewType: "LIST" | "GRID";
  onChangeViewType: (type: "LIST" | "GRID") => void;
};

export const ManageContext = createContext({} as ManageContextType);

type TProps = {
  children: React.ReactNode;
};

export const ManageProvider = ({ children }: TProps) => {
  // ************** --init state-- *****************
  const [tabData, settabData] = useState<TabInterface[]>([]);
  const path = usePathname();
  const router = useRouter();
  const [startTime, setStartTime] = useState(
    new Date(
      currentTime.getFullYear(),
      currentTime.getMonth(),
      currentTime.getDate() - 30,
      0,
      0,
      0
    )
  );
  const [endTime, setEndTime] = useState(
    new Date(
      currentTime.getFullYear(),
      currentTime.getMonth(),
      currentTime.getDate(),
      23,
      59,
      59
    )
  );
  const [textSearch, setTextSearch] = useState("");
  const [filter, setFilter] = useState<"ALL" | "search_unknown">("ALL");
  const [imagesList, setImagesList] = useState<string[]>([]);
  const [eventIds, setEventIds] = useState<string[]>([]);
  const [viewType, setViewType] = useState<"LIST" | "GRID">("LIST");

  // ************** --get type service-- *****************
  const getTypeService = async () => {
    try {
      let { data } = await serviceTypeApi.getAll({
        page: 0,
        page_break: true,
        data_search: "",
      });
      let response = formatTypeService(data?.data);
      let tab = typeServiceToTab(response);
      settabData(tab.reverse());

      if (path === "/manage") {
        router.replace("/manage/" + tab[0].path + "?id=" + tab[0].id);
      }
    } catch (error) {
      console.log("error", error);
    }
  };

  // ************** --on change view type-- *****************
  const onChangeViewType = (type: "LIST" | "GRID") => {
    // TODO: change view type
    setViewType(type);

    localStorage.setItem("manage_view_type", type);
  };

  useEffect(() => {
    if (typeof window === "undefined") return;

    const type = localStorage.getItem("manage_view_type");
    if (type === "LIST" || type === "GRID") {
      onChangeViewType(type);
    }
  }, []);

  useEffect(() => {
    getTypeService();
  }, []);

  const value = useMemo(
    () => ({
      tabData,
      settabData,
      startTime,
      endTime,
      setStartTime,
      setEndTime,
      setTextSearch,
      textSearch,
      filter,
      setFilter,
      imagesList,
      setImagesList,
      eventIds,
      setEventIds,
      viewType,
      onChangeViewType,
    }),
    [
      tabData,
      startTime,
      endTime,
      textSearch,
      filter,
      setFilter,
      imagesList,
      setImagesList,
      eventIds,
      setEventIds,
      viewType,
      onChangeViewType,
    ]
  );

  return (
    <ManageContext.Provider value={value}>{children}</ManageContext.Provider>
  );
};

export const useManagement = () => useContext(ManageContext);
