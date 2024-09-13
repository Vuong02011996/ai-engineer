import React, { useMemo } from "react";
import Image from "next/image";
import ButtonPrimary from "./misc/button-primary";
import { motion } from "framer-motion";
import ScrollAnimationWrapper from "./Layout/ScrollAnimationWrapper";
import getScrollAnimation from "@/utils/getScrollAnimation";

const Hero = ({
  listUser = [
    {
      name: "Người sử dụng",
      number: "500",
      icon: "/assets/Icon/heroicons_sm-user.svg",
    },
    {
      name: "Dự án triển khai",
      number: "100",
      icon: "/assets/Icon/gridicons_location.svg",
    },
    {
      name: "Năm kinh nghiệp thực chiến",
      number: "6",
      icon: "/assets/Icon/bx_bxs-server.svg",
    },
  ],
}) => {
  const scrollAnimation = useMemo(() => getScrollAnimation(), []);

  return (
    <div className="max-w-screen-xl pt-24 px-8 xl:px-16 mx-auto" id="about">
      <ScrollAnimationWrapper>
        <motion.div
          className="grid grid-flow-row sm:grid-flow-col grid-rows-2 md:grid-rows-1 sm:grid-cols-2 gap-8 py-6 sm:py-16"
          variants={scrollAnimation}
        >
          <div className=" flex flex-col justify-center items-start row-start-2 sm:row-start-1">
            <h1 className="text-3xl lg:text-4xl xl:text-5xl font-medium text-[#323232] leading-normal">
              Mọi việc trở nên dễ dàng với <strong>Oryza AI</strong>.
            </h1>
            <p className="text-[#55595d] mt-4 mb-6">
              Cung cấp mạng lưới đáp ứng mọi nhu cầu của bạn một cách dễ dàng và
              thú vị bằng cách sử dụng Oryza AI để khám phá các tính năng thú vị
              từ chúng tôi.
            </p>
            <a href="https://product.oryzacloud.vn/" target="_blank">
              <ButtonPrimary>Xem chi tiết</ButtonPrimary>
            </a>
          </div>
          <div className="flex w-full">
            <motion.div className="h-full w-full" variants={scrollAnimation}>
              <Image
                src="/assets/camera-ai.png"
                alt="VPN Illustrasi"
                quality={100}
                width={612}
                height={383}
                layout="responsive"
                style={{
                  borderRadius: "10px",
                }}
              />
            </motion.div>
          </div>
        </motion.div>
      </ScrollAnimationWrapper>
      <div className="relative w-full flex ">
        <ScrollAnimationWrapper className="rounded-lg w-full grid grid-flow-row sm:grid-flow-row grid-cols-1 sm:grid-cols-3 py-9 divide-y-2 sm:divide-y-0 sm:divide-x-2 divide-gray-100  z-10 ">
          {listUser.map((listUsers, index) => (
            <motion.div
              className="flex items-center justify-start sm:justify-center py-4 sm:py-6 w-8/12 px-4 sm:w-auto mx-auto sm:mx-0"
              key={index}
              custom={{ duration: 2 + index }}
              variants={scrollAnimation}
            >
              <div className="flex mx-auto w-40 sm:w-auto">
                <div className="flex items-center justify-center bg-orange-100 w-12 h-12 mr-6 rounded-full">
                  <img src={listUsers.icon} className="h-6 w-6" alt="image" />
                </div>
                <div className="flex flex-col">
                  <p className="text-xl text-black-600 font-bold">
                    {listUsers.number}+
                  </p>
                  <p className="text-lg text-black-500">{listUsers.name}</p>
                </div>
              </div>
            </motion.div>
          ))}
        </ScrollAnimationWrapper>
        <div
          className="absolute bg-black-600 opacity-5 w-11/12 roudned-lg h-64 sm:h-48 top-0 mt-8 mx-auto left-0 right-0"
          style={{ filter: "blur(114px)" }}
        ></div>
      </div>
    </div>
  );
};

export default Hero;
