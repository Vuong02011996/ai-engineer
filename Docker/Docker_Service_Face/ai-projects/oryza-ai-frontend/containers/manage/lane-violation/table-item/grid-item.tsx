import { CopyBtn } from "@/components/common/button/copy-btn";
import ImageFallback from "@/components/common/image-fallback";
import { PreviewImage } from "@/components/common/preview-img";
import { EventData } from "@/interfaces/manage/event";
import { WatchVideoBtn } from "@/components/ui";
import { watchVideo } from "@/api-client/event";
import { Stack } from "@mui/material";
import clsx from "clsx";
import { motion } from "framer-motion";
import moment from "moment";

export interface IGridItemTableProps {
  data: EventData;
  index: number;
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
    >
      <div className="bg-gray-200 p-2 rounded-lg">
        <div className="h-full space-y-2 select-none">
          {/* image */}
          <Stack
            className={clsx("rounded-xl overflow-hidden relative bg-[#CFD3D8]")}
            sx={{
              "#image-children": {
                background:
                  "linear-gradient(to top, #00000080, #00000080, transparent)",
              },
            }}
          >
            <PreviewImage
              className={
                "cursor-pointer w-full h-full flex items-center justify-center"
              }
              src={data.full_img ?? ""}
            >
              <ImageFallback
                src={data.full_img ?? ""}
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
              <div>
                <p className="truncate text-[11px]">
                  <span>Camera:</span> {data?.camera_name || "--"}
                </p>
              </div>
              <div>
                <p className="truncate text-[11px]">
                  <span>Thời gian:</span> {data.timestamp
                    ? moment(data.timestamp).format("HH:mm:ss DD/MM/yyyy")
                    : "--"}
                </p>
              </div>
            </motion.div>
          </Stack>
          {/* content */}
          <div className="flex justify-between items-center">
            <div className="flex gap-2 items-center w-full">
              <div className="w-[100px] h-[50px] overflow-hidden min-w-[100px]">
                <ImageFallback
                  src={data.crop_plate || ""}
                  fallbackSrc={"/images/logo-oryza.png"}
                  alt="photo"
                  width={100}
                  height={50}
                  className="h-[50px] object-contain bg-gray-600"
                />
              </div>
              <div className="w-[80%] py-3 pr-3 flex justify-start">
                <p className="truncate text-[11px]">{data.license_plate}</p>
                <CopyBtn text={data?.license_plate} title="biển số" />
              </div>
              <div className="w-[20%] py-3 flex justify-end">
                <WatchVideoBtn onClick={() => watchVideo(data.event_id)} />
              </div>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}