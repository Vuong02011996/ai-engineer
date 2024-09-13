import ImageFallback from "@/components/common/image-fallback";
import { PreviewImage } from "@/components/common/preview-img";
import { WatchVideoBtn } from "@/components/ui";
import { EventData } from "@/interfaces/manage/event";
import { motion } from "framer-motion";
import moment from "moment";
import { EffectCube } from "swiper/modules";
import { Swiper, SwiperSlide } from "swiper/react";

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
      <Swiper
        effect={"cube"}
        grabCursor={true}
        cubeEffect={{
          shadow: true,
          slideShadows: true,
          shadowOffset: 20,
          shadowScale: 0.94,
        }}
        modules={[EffectCube]}
        className="select-none"
      >
        <SwiperSlide className="relative bg-[#f2f2f2]">
          <SilderItem
            title={"Hình ảnh bắt đầu"}
            image={data.image_start}
            camera_name={data.camera_name}
            time={data.start_time}
            handleWatchVideo={() => handleWatchVideo(data.event_id)}
          />
        </SwiperSlide>
        <SwiperSlide className="relative bg-[#f2f2f2]">
          <SilderItem
            title={"Hình ảnh kết thúc"}
            image={data.image_end}
            camera_name={data.camera_name}
            time={data.end_time}
            handleWatchVideo={() => handleWatchVideo(data.event_id)}
          />
        </SwiperSlide>
      </Swiper>
    </motion.div>
  );
}

const SilderItem = (data: {
  title: string;
  image?: string;
  camera_name?: string;
  time?: Date | null;
  handleWatchVideo: any;
}) => {
  return (
    <div>
      <PreviewImage
        className="w-full h-[200px] justify-between flex-col flex"
        src={data.image ?? "null"}
        openWithDoubleClick
      >
        <ImageFallback
          src={data.image ?? "null"}
          fallbackSrc={"/images/logo-oryza.png"}
          width={300}
          height={180}
          alt={"Hình ảnh ghi nhận"}
          style={{
            objectFit: "contain",
            background: "#CFD3D8",
            maxHeight: "180px",
            width: "100%",
            padding: "5px 0",
          }}
        />
        <p className="text-center w-full text-[14px] text-[#323232] font-medium h-[20px]">
          {data.title}
        </p>
      </PreviewImage>
      <div className="p-2 flex justify-between">
        <div>
          <p className="table-text-custom">
            <span>Camera:</span>
            {data?.camera_name || "--"}
          </p>
          <p className="table-text-custom">
            {data?.time
              ? moment(data.time).format("HH:mm:ss DD/MM/yyyy")
              : "Thời gian: --"}
          </p>
        </div>
        <div>
          <WatchVideoBtn onClick={data.handleWatchVideo} />
        </div>
      </div>
    </div>
  );
};
