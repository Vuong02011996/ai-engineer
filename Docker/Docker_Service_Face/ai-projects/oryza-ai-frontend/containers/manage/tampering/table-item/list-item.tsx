import ImageFallback from "@/components/common/image-fallback";
import { PreviewImage } from "@/components/common/preview-img";
import { EventData } from "@/interfaces/manage/event";
import moment from "moment";

export interface IListItemTableProps {
  data: EventData;
  index: number;
}

export function ListItemTable(props: IListItemTableProps) {
  const { data, index } = props;

  return (
    <div className="w-full flex flex-row min-w-[1200px] table-row-custom items-center border-b-2 border-[#F8F8F8]">
      <div className="w-[60px] py-6 flex justify-center">
        {_renderText(index.toString())}
      </div>

      <div className="w-[40%] py-6 pr-3 flex flex-col justify-start">
        <div className="mb-2">{_renderText(data?.camera_name)}</div>
        <div>{_renderText(data?.camera_ip)}</div>
      </div>

      <div className="w-[40%] py-6 pr-3 flex justify-start">
        {data.timestamp
          ? _renderText(moment(data.timestamp).format("DD/MM/yyyy HH:mm:ss"))
          : "--"}
      </div>
      <div className="w-[20%] py-3 pr-3 flex justify-start">
        <PreviewImage
          className="w-full h-[90px] relative  justify-start flex "
          src={data.image_url}
        >
          <ImageFallback
            src={data.image_url}
            fallbackSrc={"/images/logo-oryza.png"}
            width={160}
            height={90}
            alt={"Hình ảnh ghi nhận"}
            style={{
              objectFit: "contain",
              background: "#CFD3D8",
            }}
          />
        </PreviewImage>
      </div>
    </div>
  );
}
function _renderText(text?: string) {
  return <p className="font-medium text-grayOz text-sm">{text || "--"}</p>;
}
