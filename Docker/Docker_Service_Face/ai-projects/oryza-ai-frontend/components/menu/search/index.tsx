import Icon from "@/components/common/icon";
import clsx from "clsx";

export interface ISearchBoxProps {}

export function SearchBox(props: ISearchBoxProps) {
  return (
    <div
      className={clsx(
        "bg-[#64686D] h-[50px] flex  items-center rounded-[8px] cursor-pointer active:bg-[#6A6E78]  space-x-[16px] p-[12px] ",
        "transition-all duration-300 ease-in-out  justify-start overflow-hidden"
      )}
    >
      <Icon
        name="search"
        className={`w-[24px] h-[24px] min-w-[24px] transition-all duration-600 ease-in-out ${"stroke-[#fff]"}`}
      />

      <input
        type="text"
        name=""
        id=""
        className="bg-transparent outline-none text-[#E3E5E5] font-medium text-base"
        placeholder="Tìm kiếm"
      />
    </div>
  );
}
