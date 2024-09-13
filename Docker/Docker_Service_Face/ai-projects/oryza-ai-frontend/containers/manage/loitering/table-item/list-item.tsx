import { CopyBtn } from "@/components/common/button/copy-btn";
import ImageFallback from "@/components/common/image-fallback";
import ImageMagnifyComponent from "@/components/common/image-with-hover-effect/zoom";
import { PreviewImage } from "@/components/common/preview-img";
import { WatchVideoBtn } from "@/components/ui";
import { EventData } from "@/interfaces/manage/event";
import { Stack } from "@mui/material";
import moment from "moment";

export interface IListItemTableProps {
  data: EventData;
  index: number;
  handleWatchVideo: any;
}

export function ListItemTable(props: IListItemTableProps) {
  const { data, index, handleWatchVideo } = props;

  return (
    <div className="w-full flex flex-row min-w-[1200px] table-row-custom items-center border-b-2 border-[#F8F8F8]">
      <div className="w-[60px] py-6 flex justify-center">
        {_renderText(index.toString())}
      </div>

      <div className="w-[15%] py-6 pr-3 flex flex-col justify-start">
        <div className="mb-2">{_renderText(data?.camera_name)}</div>
        <div>{_renderText(data?.camera_ip)}</div>
      </div>

      <div className="w-[15%] py-6 pr-3 flex justify-start">
        {data?.start_time
          ? _renderText(moment(data.start_time).format("DD/MM/yyyy HH:mm:ss"))
          : "--"}
      </div>
      <div className="w-[15%] py-6 pr-3 flex justify-start">
        {data?.end_time
          ? _renderText(moment(data.end_time).format("DD/MM/yyyy HH:mm:ss"))
          : "--"}
      </div>
      <div className="w-[15%] py-6 pr-3 flex justify-start">
        {data?.duration_time? _renderText(data.duration_time.toString()): _renderText("--")}
      </div>
      <div className="w-[15%] py-3 pr-3 flex justify-start">
        <PreviewImage
          className="w-full h-[90px] relative  justify-start flex "
          src={data.image_start ?? "null"}
        >
          <ImageFallback
            src={data.image_start ?? "null"}
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
      <div className="w-[20%] py-3 pr-3 flex justify-start">
        <PreviewImage
          className="w-full h-[90px] relative  justify-start flex "
          src={data.image_end ?? "null"}
        >
          <ImageFallback
            src={data.image_end ?? "null"}
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
      <div className="w-[5%] py-3 pr-3 flex justify-center">
        <WatchVideoBtn onClick={() => handleWatchVideo(data.event_id)} />
      </div>
    </div>
  );
}
function _renderText(text?: string) {
  return <p className="font-medium text-grayOz text-sm">{text || "--"}</p>;
}
