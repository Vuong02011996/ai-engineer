import { changeTheme } from "@/utils/helper";
import { useLocalStorage } from "@mantine/hooks";
import { useEffect, useState } from "react";
import clsx from "clsx";

const ThemeComp = () => {
  const [theme, setTheme] = useLocalStorage({
    key: "color-scheme",
    defaultValue: "",
  });
  const handleThemeChange = (value: any) => {
    changeTheme(value);
    setTheme(value);
  };
  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Theme Manager</h1>
      <div className="mb-4">
        <label htmlFor="theme" className="mr-2">
          Choose Theme:
        </label>

        <div className="flex flex-row space-x-3">
          <button
            className="bg-primary p-2 rounded-md text-text-on-primary"
            onClick={() => handleThemeChange("")}
          >
            Default
          </button>
          <button
            className="bg-primary p-2 rounded-md text-text-on-primary"
            onClick={() => handleThemeChange("theme1")}
          >
            theme1
          </button>
          <button
            className="bg-primary p-2 rounded-md text-text-on-primary"
            onClick={() => handleThemeChange("theme2")}
          >
            theme2
          </button>
          <button
            className="bg-primary p-2 rounded-md text-text-on-primary"
            onClick={() => handleThemeChange("theme3")}
          >
            theme3
          </button>
        </div>
      </div>
    </div>
  );
};

export interface IComponentsPageProps {}

export default function ComponentsPage(props: IComponentsPageProps) {
  const [light, setLight] = useState<"RED" | "GREEN" | "YELLOW">("RED");

  useEffect(() => {
    let intervalId: NodeJS.Timeout;
    const second = (s: number) => s * 1000;

    const switchLight = () => {
      switch (light) {
        case "RED":
          setLight("GREEN");
          intervalId = setTimeout(() => setLight("YELLOW"), second(3)); // 20 seconds green, then 5 seconds yellow
          break;
        case "GREEN":
          setLight("YELLOW");
          intervalId = setTimeout(() => setLight("RED"), second(1)); // 5 seconds yellow, then 30 seconds red
          break;
        case "YELLOW":
          setLight("RED");
          intervalId = setTimeout(() => setLight("GREEN"), second(3)); // 30 seconds red, then 20 seconds green
          break;
        default:
          setLight("RED");
          break;
      }
    };

    intervalId = setTimeout(switchLight, second(1.5));

    return () => {
      clearTimeout(intervalId);
    };
  }, [light]);
  return (
    <div className={`min-h-screen `}>
      <ThemeComp />
      <div className="shadow-shadown1 mt-6 mx-12 p-5 min-h-[300px]">
        <div className="w-[440px] space-y-3">
          <LightTraffic light={light} />
          <LightTraffic light={"LONG"} />
        </div>
      </div>
    </div>
  );
}

type LightTrafficType = "RED" | "GREEN" | "YELLOW" | "LONG";
const LightTraffic = ({ light }: { light: LightTrafficType }) => {
  return (
    <div className="bg-black px-4 py-2 rounded-full w-fit flex gap-2">
      <div
        className={clsx(
          "w-10 h-10 rounded-full shadow-light bg-[#FF0000]",
          light === "RED" ? "opacity-100" : "opacity-50"
        )}
      />
      <div
        className={clsx(
          "w-10 h-10 rounded-full shadow-light bg-[#FFFF00] ",
          light === "YELLOW" && "opacity-100",
          light === "LONG" && "opacity-100 animate-pulse",
          (light === "RED" || light === "GREEN") && "opacity-50"
        )}
      />
      <div
        className={clsx(
          "w-10 h-10 rounded-full shadow-light bg-[#00FF00]",
          light === "GREEN" ? "opacity-100" : "opacity-50"
        )}
      />
    </div>
  );
};
