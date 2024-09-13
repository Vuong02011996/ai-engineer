import Image from "next/image";
import React, { useMemo } from "react";
import { motion } from "framer-motion";
import ScrollAnimationWrapper from "./Layout/ScrollAnimationWrapper";
import getScrollAnimation from "@/utils/getScrollAnimation";

const features = [
  "Nhận Diện Khuôn Mặt.",
  "Phát Hiện Đồ Vật Bỏ Rơi.",
  "Nhận Diện Biển Số Xe",
  "Phát Hiện Đồng Phục.",
  "Giám Sát Người Lảng Vảng.",
  "Phát Hiện Đám Đông.",
  "Phát Hiện Đậu đỗ Trái Phép.",
  "Phát Hiện Hành Vi Lấn Làn.",
  "Phát Hiện Hành Vi Lấn Vạch.",
  "Phát Hiện Hành Vi Đi Ngược Chiều.",
];

const Feature = () => {
  const scrollAnimation = useMemo(() => getScrollAnimation(), []);

  return (
    <div
      className="max-w-screen-xl mt-8 mb-6 sm:mt-14 sm:mb-14 px-6 sm:px-8 lg:px-16 mx-auto pt-10"
      id="feature"
    >
      <div className="grid grid-flow-row sm:grid-flow-col grid-cols-1 sm:grid-cols-2 gap-8 p  y-8 my-12">
        <ScrollAnimationWrapper className="flex w-full justify-end">
          <motion.div className="h-full w-full p-4 " variants={scrollAnimation}>
            <Image
              src="/assets/smart-building.png"
              alt="VPN Illustrasi"
              layout="responsive"
              quality={100}
              height={414}
              width={508}
              style={{
                borderRadius: "10px",
              }}
            />
          </motion.div>
        </ScrollAnimationWrapper>
        <ScrollAnimationWrapper>
          <motion.div
            className="flex flex-col items-end justify-center ml-auto w-full lg:w-9/12"
            variants={scrollAnimation}
          >
            <h3 className="text-3xl lg:text-4xl font-medium leading-relaxed text-white">
              Chúng tôi cung cấp nhiều tính năng bạn có thể sử dụng
            </h3>
            <p className="my-2 text-[#dddddd]">
              Bạn có thể khám phá các tính năng mà chúng tôi cung cấp một cách
              thú vị và có các chức năng riêng của từng tính năng.
            </p>
            <ul className="text-black-500 self-start list-inside ml-8">
              {features.map((feature, index) => (
                <motion.li
                  className="relative circle-check custom-list text-white"
                  custom={{ duration: 2 + index }}
                  variants={scrollAnimation}
                  key={feature}
                  whileHover={{
                    scale: 1.1,
                    transition: {
                      duration: 0.2,
                    },
                  }}
                >
                  <h4>{feature}</h4>
                </motion.li>
              ))}
            </ul>
          </motion.div>
        </ScrollAnimationWrapper>
      </div>
    </div>
  );
};

export default Feature;
