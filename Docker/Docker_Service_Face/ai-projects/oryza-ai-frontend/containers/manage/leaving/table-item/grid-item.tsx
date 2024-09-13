import ImageFallback from "@/components/common/image-fallback";
import { PreviewImage } from "@/components/common/preview-img";
import { WatchVideoBtn } from "@/components/ui";
import { EventData } from "@/interfaces/manage/event";
import clsx from "clsx";
import { motion } from "framer-motion";
import moment from "moment";

export interface IGridItemTableProps {
  data: EventData;
  index: number;
  handleWatchVideo: any;
}

export function GridItemTable(props: IGridItemTableProps) {
  const { data, handleWatchVideo } = props;

  return (
    <motion.div
      initial={{
        opacity: 0,
      }}
      animate={{
        opacity: 1,
        transition: {
          duration: 0.5,
        },
      }}
      exit={{
        opacity: 0,
        transition: {
          duration: 0.5,
        },
      }}
    >
      <div className="bg-gray-200 p-2 rounded-lg">
        <div className="h-full space-y-2 select-none">
          {/* image */}
          <div
            className={clsx(
              "rounded-xl overflow-hidden relative cursor-pointer bg-[#CFD3D8]"
            )}
          >
            <PreviewImage className="w-full h-full" src={data.image_url}>
              <ImageFallback
                src={data.image_url}
                fallbackSrc={"/images/logo-oryza.png"}
                alt="post-photo"
                width={350}
                height={250}
                style={{ objectFit: "contain", width: "350px", height: "200px" }}
              />
            </PreviewImage>
            <motion.div
              id="image-children"
              className={clsx(
                "absolute left-0 right-0 bottom-0 bg-gradient-to-t h-fit p-2 text-white pt-7",
                "flex flex-col items-start"
              )}
            >
              <p className="flex-1 truncate"></p>
            </motion.div>
          </div>
          {/* content */}
          <div className="flex justify-between items-center ">
            <div>
              <p className="text-[14px] font-medium capitalize flex-1 truncate text-grayOz">
                Camera:   {data.camera_name}
              </p>
              <p className="text-[12px] font-medium capitalize flex-1 truncate text-grayOz">
                Thời gian:   {data.timestamp
                  ? moment(data.timestamp).format("HH:mm:ss DD/MM/yyyy")
                  : "--"}
              </p>
            </div>
            <WatchVideoBtn onClick={() => handleWatchVideo(data.event_id)} />
          </div>
        </div>
      </div>
    </motion.div>
  );
}
