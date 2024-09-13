import { serviceTypeApi } from "@/api-client/setting";
import { TabInterface } from "@/interfaces/tab";
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

export type ProcessPageContextType = {
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
};

export const ProcessPageContext = createContext({} as ProcessPageContextType);

type TProps = {
  children: React.ReactNode;
};

export const ProcessPageProvider = ({ children }: TProps) => {
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

      if (path === "/process") {
        router.replace("/process/" + tab[0].path + "?id=" + tab[0].id);
      }
    } catch (error) {
      console.log("error", error);
    }
  };

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
    ]
  );

  return (
    <ProcessPageContext.Provider value={value}>
      {children}
    </ProcessPageContext.Provider>
  );
};

export const useProcessPage = () => useContext(ProcessPageContext);
