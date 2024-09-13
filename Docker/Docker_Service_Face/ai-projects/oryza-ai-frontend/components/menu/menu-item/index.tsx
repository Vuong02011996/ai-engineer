import Icon from "@/components/common/icon";
import clsx from "clsx";

export interface IMenuItemProps {
  active?: boolean;
  text: string;
  icon: string;
}

export function MenuItem(props: IMenuItemProps) {
  const { active, text, icon } = props;

  return (
    <div
      title={text}
      className={clsx(
        "h-[50px] flex items-center rounded-[8px] cursor-pointer active:bg-[#6A6E78] hover:bg-blackOz",
        "space-x-[16px] p-[12px] transition-all duration-300 ease-in-out  justify-start overflow-hidden"
      )}
    >
      <Icon
        name={icon}
        className={clsx(
          "w-[26px] h-[26px] min-w-[26px] transition-all duration-600 ease-in-out",
          active ? "stroke-[#78C6E7]" : "stroke-[#fff]"
        )}
      />

      <p
        className={`truncate use select-none font-semibold text-base ${
          active ? "text-[#78C6E7]" : "text-[#CDD2D1]"
        } `}
      >
        {text}
      </p>
    </div>
  );
}
