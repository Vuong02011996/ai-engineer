import Image from "next/image";
import { useCallback } from "react";

export interface ITableItemHistoryProps {
  data: any;
  index: number;
  reload: () => void;
}

export function TableItemHistory(props: ITableItemHistoryProps) {
  const { data, index } = props;

  return (
    <div className="w-full flex flex-row min-w-[1200px] table-row-custom items-center">
      <div className="w-[60px] py-6 flex justify-center">
        {_renderText(index.toString())}
      </div>
      <div className="w-[20%] py-6 flex justify-start">
        {_renderAction(
          index % 3 == 0 ? "UPDATE" : index % 2 == 0 ? "EDIT" : "CREATE"
        )}
      </div>
      <div className="w-[40%] py-6 flex justify-start">
        {_renderText("Đã xoá cấu hình Weehook/Websocket tên Erp")}
      </div>
      <div className="w-[20%] py-6 flex justify-start">
        {_renderText("02/02/2024 15:15:01")}
      </div>
      <div className="w-[20%] py-6 flex justify-start">
        {_renderText("Username1234")}
      </div>
    </div>
  );
}

function _renderText(text: string) {
  return <p className="font-medium text-grayOz text-sm">{text}</p>;
}
function _renderAction(action: "CREATE" | "EDIT" | "UPDATE") {
  const data = useCallback(() => {
    switch (action) {
      case "CREATE":
        return {
          iconUrl: "/icons/create.svg",
          text: "Tạo",
        };
      case "EDIT":
        return {
          iconUrl: "/icons/edit-icon.svg",
          text: "Sửa",
        };
      case "UPDATE":
        return {
          iconUrl: "/icons/remove.svg",
          text: "Xóa",
        };

      default:
        return {
          iconUrl: "/icons/edit-icon.svg",
          text: "Sửa",
        };
    }
  }, [action]);
  return (
    <div className="flex flex-row items-center space-x-2">
      <div className="w-6 h-6 flex items-center justify-center">
        <Image src={data().iconUrl} width={17} height={17} alt="icon" />
      </div>
      <p className="font-medium text-grayOz text-sm"> {data().text}</p>
    </div>
  );
}
