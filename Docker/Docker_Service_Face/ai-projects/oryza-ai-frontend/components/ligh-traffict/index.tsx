import clsx from "clsx";

export type LightTrafficType = "RED" | "GREEN" | "YELLOW" | "LONG" | "UNKNOWN";
export const LightTraffic = ({ light }: { light: LightTrafficType }) => {
  return (
    <div className="bg-blackOz px-2 py-1 rounded-full w-fit flex gap-1">
      <div
        className={clsx(
          "w-5 h-5 rounded-full  bg-[#FF0000]",
          light === "RED" ? "opacity-100 shadow-light" : "opacity-35"
        )}
      />
      <div
        className={clsx(
          "w-5 h-5 rounded-full shadow-light bg-[#FFFF00] ",
          light === "YELLOW" && "opacity-100 shadow-light",
          light === "LONG" && "opacity-100 animate-pulse shadow-light",
          (light === "RED" || light === "GREEN") && "opacity-35"
        )}
      />
      <div
        className={clsx(
          "w-5 h-5 rounded-full shadow-light bg-[#00FF00]",
          light === "GREEN" ? "opacity-100 shadow-light" : "opacity-35"
        )}
      />
    </div>
  );
};
