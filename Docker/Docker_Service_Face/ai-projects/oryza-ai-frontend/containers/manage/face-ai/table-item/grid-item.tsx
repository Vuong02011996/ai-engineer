import { EventData } from "@/interfaces/manage/event";
import { motion } from "framer-motion";
import * as React from "react";
import Image from "next/image";
import moment from "moment";
import CheckboxCustom2 from "@/components/common/checkbox/checbox-2";
import { useManagement } from "@/context/manage-context";
import clsx from "clsx";
import ImageFallback from "@/components/common/image-fallback";

export interface IGridItemTableProps {
  data: EventData;
  index: number;
}

export function GridItemTable(props: IGridItemTableProps) {
  const { data } = props;
  const { imagesList, setImagesList, eventIds, setEventIds } = useManagement();

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
      className="shadow-shadown2 rounded-[10px] overflow-hidden h-[300px] bg-gray-500 relative card-parrent "
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
      <div className="absolute bottom-0 left-0 right-0 text-white px-5 pb-2 pt-6 bg-gradient-to-t from-[#00000080] via-[#00000080] to-transparent">
        <p className="font-semibold truncate text-[16px] pb-1">{data.name}</p>
        <p className="font-medium truncate text-[12px]">{data.camera_name? data.camera_name : data.camera_ip}</p>
        <p className="text-[10px]">
          {data.timestamp
            ? moment(data.timestamp).format("DD/MM/yyyy HH:mm:ss")
            : "--"}
        </p>
      </div>
      {/* checkbox */}
      <div
        id="checkbox-custom"
        className={clsx(
          data.user_id !== "Unknown"
            ? "hidden"
            : "absolute bottom-1 right-1 opacity-100"
        )}
      >
        <motion.div
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="rounded-full scale-90"
          title="Chọn"
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
        </motion.div>
      </div>
    </motion.div>
  );
}
