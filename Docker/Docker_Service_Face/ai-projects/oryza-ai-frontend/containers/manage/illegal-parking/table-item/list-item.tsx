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

      <div className="w-[10%] py-6 pr-10 flex flex-col justify-start break-all">
        <div className="mb-2">{_renderText(data?.camera_name)}</div>
        <div>{_renderText(data?.camera_ip)}</div>
      </div>

      <div className="w-[8%] py-6 pr-3 flex justify-start break-all">
        <div style={{ marginRight: '10px' }}>{_renderText(data.license_plate)}</div>
        <CopyBtn text={data.license_plate} title="Biển số"/>
      </div>

      <div className="w-[13%] py-3 pr-3 flex justify-start">
        <PreviewImage
          className="w-full h-[90px] relative  justify-start flex"
          src={data.license_plate_url ?? "null"}
        >
          <ImageFallback
            src={data.license_plate_url ?? "null"}
            fallbackSrc={"/images/logo-oryza.png"}
            width={160}
            height={90}
            alt={"Hình ảnh biển số"}
            style={{
              objectFit: "contain",
              background: "#CFD3D8",
            }}
          />
        </PreviewImage>
      </div>

      <div className="w-[10%] py-6 pr-3 flex justify-start break-all">
        {
          data?.status
            ? _renderText(data?.status) 
            : "--"
        }
      </div>

      <div className="w-[10%] py-6 pr-3 flex flex-col justify-start">
        {data?.start_time ? (
          <>
            <div className="mb-2">{_renderText(formatDateTime(data.start_time, "DD/MM/yyyy"))}</div>
            <div>{_renderText(formatDateTime(data.start_time, "HH:mm:ss"))}</div>
          </>
        ) : (
          "--"
        )}
      </div>

      <div className="w-[10%] py-6 pr-3 flex flex-col justify-start">
        {data?.end_time ? (
          <>
            <div className="mb-2">{_renderText(formatDateTime(data.end_time, "DD/MM/yyyy"))}</div>
            <div>{_renderText(formatDateTime(data.end_time, "HH:mm:ss"))}</div>
          </>
        ) : (
          "--"
        )}
      </div>

      <div className="w-[13%] py-3 pr-3 flex justify-start">
        <PreviewImage
          className="w-full h-[90px] relative justify-start flex "
          src={data.image_start ?? "null"}
        >
          <ImageFallback
            src={data.image_start ?? "null"}
            fallbackSrc={"/images/logo-oryza.png"}
            width={160}
            height={90}
            alt={"Hình ảnh bắt đầu"}
            style={{
              objectFit: "contain",
              background: "#CFD3D8",
            }}
          />
        </PreviewImage>
      </div>

      <div className="w-[13%] py-3 pr-3 flex justify-start">
        <PreviewImage
          className="w-full h-[90px] relative justify-start flex "
          src={data.image_end ?? "null"}
        >
          <ImageFallback
            src={data.image_end ?? "null"}
            fallbackSrc={"/images/logo-oryza.png"}
            width={160}
            height={90}
            alt={"Hình ảnh kết thúc"}
            style={{
              objectFit: "contain",
              background: "#CFD3D8",
            }}
          />
        </PreviewImage>
      </div>

      <div className="w-[8%] py-6 pr-3 flex justify-start">
      {
        data?.duration_time ? _renderTime(data.duration_time) : "--"
      }
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

function _renderTime(duration: number) {
  let seconds = duration % 60;
  let minutes = Math.floor(duration / 60) % 60;
  let hours = Math.floor(duration / 3600);

  let result = [];

  if (hours > 0) result.push(`${hours} giờ`);
  if (minutes > 0) result.push(`${minutes} phút`);
  if (seconds > 0 || result.length === 0) result.push(`${seconds} giây`);

  return <p className="font-medium text-grayOz text-sm">{result.join(' ') || "--"}</p>;
}

function formatDateTime(date: any, format: string) {
  const momentDate = moment(date);
  if (momentDate.isValid()) {
    return momentDate.format(format);
  } else {
    return "--";
  }
}