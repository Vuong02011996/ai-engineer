import SearchIcon from "@/assets/svgs/search-gray.svg";
import { FileAction } from "../file-action";
import moment from "moment";

export interface IMainHeadProps {
  showFileAciton?: boolean;
  expiryDate?: Date;
  searchValue?: string;
  onChange?: (e: any) => void;
}

export function MainHead(props: IMainHeadProps) {
  const showFileAciton = props.showFileAciton ?? true;
  const { expiryDate } = props;
  return (
    <div className="px-[32px] pb-[12px] flex flex-row justify-between align-top h-[50px]">
      <div className="flex flex-row space-x-[16px] items-center ">
        <SearchIcon />
        <input
          value={props.searchValue}
          onChange={(e) => {
            if (props.onChange) props.onChange(e.target.value);
          }}
          type="text"
          className="bg-transparent outline-none text-[#808080] font-medium text-base"
          placeholder="Tìm kiếm dữ liệu..."
        />
      </div>
      {/* {showFileAciton && <FileAction />} */}
      {expiryDate && (
        <p className="text-[#808080] text-[14px] font-normal">
          Thời hạn sử dụng:{" "}
          <span className="text-primary text-[14px] font-medium">
            {moment(expiryDate).format("DD/MM/yyyy")}
          </span>
        </p>
      )}
    </div>
  );
}
