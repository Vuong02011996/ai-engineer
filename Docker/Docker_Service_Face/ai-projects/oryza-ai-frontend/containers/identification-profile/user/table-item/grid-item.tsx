import { TableAction } from "@/components";
import ImageFallback from "@/components/common/image-fallback";
import { IPerson } from "@/interfaces/identification-profile/person";
import { Stack } from "@mui/material";
import { motion } from "framer-motion";
import { EffectCards } from "swiper/modules";
import { Swiper, SwiperSlide } from "swiper/react";

export interface IGridItemTableProps {
  data: IPerson;
  index: number;
  reload: any;
  setTotal: any;
  handleClick: any;
  setOpenEditDialog: any;
  setOpenRemoveDialog: any;
}

export function GridItemTable(props: IGridItemTableProps) {
  const { data, handleClick, setOpenEditDialog, setOpenRemoveDialog } = props;

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
      className="relative h-[300px] "
    >
      <Swiper
        effect={"cards"}
        grabCursor={true}
        modules={[EffectCards]}
        className="h-full"
      >
        {data.images.map((image, index) => {
          return (
            <SwiperSlide
              key={image.id}
              className="rounded-xl shadow-shadown2 relative cursor-pointer"
            >
              <Stack
                onClick={handleClick}
                sx={{
                  ":hover": {
                    "#action-btn": {
                      background: "#ddd",
                    },
                  },
                }}
                className="w-full h-full rounded-[8px] overflow-hidden "
              >
                <ImageFallback
                  fallbackSrc={"/images/logo-oryza.png"}
                  src={image.url}
                  width={200}
                  height={200}
                  quality={100}
                  style={{
                    height: "100%",
                    width: "100%",
                    objectFit: "cover",
                    borderRadius: "8px",
                  }}
                  alt="photo"
                />

                <div className="absolute bottom-0 left-0 right-0 text-white px-5 pb-2 pt-6 bg-gradient-to-t from-[#00000080] via-[#00000080] to-transparent">
                  <p className="font-semibold truncate text-[16px] pb-1">
                    {data.name}
                  </p>
                  <p className="font-medium truncate text-[12px]">
                    {data.other_info.address || "Không có địa chỉ"}
                  </p>
                </div>
                <div
                  id="action-btn"
                  className="absolute top-0 right-0  rounded-bl-[10px] overflow-hidden bg-transparent hover:bg-gray-100 transition-all duration-200 cursor-pointer"
                >
                  <TableAction
                    onEdit={() => setOpenEditDialog(true)}
                    onRemove={() => setOpenRemoveDialog(true)}
                  />
                </div>
              </Stack>
            </SwiperSlide>
          );
        })}
      </Swiper>
    </motion.div>
  );
}
