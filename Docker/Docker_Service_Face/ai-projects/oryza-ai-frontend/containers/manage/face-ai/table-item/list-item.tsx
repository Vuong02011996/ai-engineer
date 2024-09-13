import CheckboxCustom2 from "@/components/common/checkbox/checbox-2";
import ImageFallback from "@/components/common/image-fallback";
import { PreviewImage } from "@/components/common/preview-img";
import { useManagement } from "@/context/manage-context";
import { EventData } from "@/interfaces/manage/event";
import clsx from "clsx";
import moment from "moment";

export interface IListItemTableProps {
  data: EventData;
  index: number;
}

export function ListItemTable(props: IListItemTableProps) {
  const { data, index } = props;
  const { imagesList, setImagesList, eventIds, setEventIds } = useManagement();

  return (
    <div className="w-full flex flex-row min-w-[1200px] table-row-custom items-center border-b-2 border-[#F8F8F8]">
      <div className="w-[40px] py-6 flex justify-center items-center">
        <div
          className={clsx(
            "w-full flex items-center justify-center",
            data.user_id !== "Unknown" ? "hidden" : ""
          )}
        >
          <CheckboxCustom2
            checked={imagesList.includes(data?.image_url)}
            onChange={(checked) => {
              if (checked) {
                setImagesList([...imagesList, data?.image_url]);
                setEventIds([...eventIds, data?.event_id]);
              } else {
                setImagesList(
                  imagesList.filter((item) => item !== data?.image_url)
                );
                setEventIds(
                  imagesList.filter((item) => item !== data?.event_id)
                );
              }
            }}
          />
        </div>
      </div>

      <div className="w-[60px] py-6 flex justify-center">
        {_renderText(index.toString())}
      </div>

      <div className="w-[40%] py-6 pr-3 flex justify-start">
        {_renderText(data.name)}
      </div>

      <div className="w-[20%] py-6 pr-3 flex flex-col justify-start">
        <div className="mb-2">{_renderText(data?.camera_name)}</div>
        <div>{_renderText(data?.camera_ip)}</div>
      </div>

      <div className="w-[20%] py-6 pr-3 flex flex-col justify-start">
        <div className="mb-2">{_renderText(formatDateTime(data.timestamp, "DD/MM/yyyy"))}</div>
        <div>{_renderText(formatDateTime(data.timestamp, "HH:mm:ss"))}</div>
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
function formatDateTime(date: any, format: string) {
  const momentDate = moment(date);
  if (momentDate.isValid()) {
    return momentDate.format(format);
  } else {
    return "--";
  }
}