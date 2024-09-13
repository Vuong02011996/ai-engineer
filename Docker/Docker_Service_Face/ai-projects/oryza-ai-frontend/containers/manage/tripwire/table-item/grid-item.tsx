import ImageFallback from "@/components/common/image-fallback";
import { PreviewImage } from "@/components/common/preview-img";
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
  const { data } = props;

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
      className="h-full space-y-2 select-none"
    >
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
              width={1000}
              height={1000}
              style={{ height: "200px", objectFit: "contain" }}
            />
          </PreviewImage>
          <motion.div
            id="image-children"
            className={clsx(
              "absolute left-0 right-0 bottom-0 bg-gradient-to-t  h-[70px] p-2 text-white pt-5",
              "flex justify-between items-center"
            )}
          >
            <p className="flex-1 truncate"></p>
          </motion.div>
        </div>
        {/* content */}
        <div className=" justify-between items-center ">
          <p className="text-[16px] font-medium capitalize flex-1 truncate text-grayOz">
            {data.camera_name}
          </p>
          <p className="text-[12px] font-medium capitalize flex-1 truncate text-grayOz text-start">
            {data.timestamp
              ? moment(data.timestamp).format("HH:mm:ss DD/MM/yyyy")
              : "--"}
          </p>
        </div>
      </div>
    </motion.div>
  );
}
