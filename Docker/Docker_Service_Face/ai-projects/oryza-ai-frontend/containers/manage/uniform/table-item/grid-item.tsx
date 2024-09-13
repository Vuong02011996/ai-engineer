import { EventData } from "@/interfaces/manage/event";
import { motion } from "framer-motion";
import * as React from "react";
import Image from "next/image";
import moment from "moment";
import CheckboxCustom2 from "@/components/common/checkbox/checbox-2";
import { useManagement } from "@/context/manage-context";
import clsx from "clsx";
import ImageFallback from "@/components/common/image-fallback";
import { PreviewImage } from "@/components/common/preview-img";
import { Stack } from "@mui/material";
import { watchVideo } from "@/api-client/event";

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
      className={clsx(
        "shadow-shadown2 rounded-[10px] overflow-hidden h-[300px] bg-gray-500 relative card-parrent ",
        data?.error_type === 0 && "shadow-success border-2 border-success",
        data?.error_type === 1 && "shadow-error border-2 border-error"
      )}
    >
      <Stack
        sx={{
          height: "100%",
          ":hover": {
            "#watch-video-btn": {
              height: "40px",
            },
          },
          "#watch-video-btn": {
            height: 0,
            transition: "all .3s",
          },
        }}
      >
        <PreviewImage
          src={data.image_url}
          className={"w-full h-full cursor-pointer "}
        >
          <ImageFallback
            fallbackSrc={"/images/logo-oryza.png"}
            src={data.image_url}
            width={200}
            height={200}
            quality={100}
            style={{
              height: "100%",
              width: "100%",
              objectFit: "cover",
            }}
            alt="photo"
          />
        </PreviewImage>
        <div className="absolute bottom-0 left-0 right-0 text-white bg-gradient-to-t from-[#00000080] via-[#00000080]  to-transparent ">
          <div className="px-5 pb-1 pt-6 ">
            <p className="font-medium truncate text-[12px]">{data.camera_name}</p>
            <p className="text-[10px]">
              {data.timestamp
                ? moment(data.timestamp).format("DD/MM/yyyy HH:mm:ss")
                : "--"}
            </p>
          </div>
          <div
            id="watch-video-btn"
            onClick={() => watchVideo(data.event_id)}
            className="overflow-hidden bg-[#37415190] flex items-center justify-center cursor-pointer select-none"
          >
            <p className="text-center uppercase ">Xem video</p>
          </div>
        </div>
      </Stack>
    </motion.div>
  );
}
