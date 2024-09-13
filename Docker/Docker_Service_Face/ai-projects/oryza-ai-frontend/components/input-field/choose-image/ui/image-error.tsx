import * as React from "react";
import Image from "next/image";

export interface IImageErrorProps {}

export function ImageError(props: IImageErrorProps) {
  return (
    <div className="flex w-full h-full items-center justify-center flex-col space-y-[6px]">
      <Image
        src="/icons/upload-error.svg"
        alt="avatar"
        width={32}
        height={32}
      />
      <p className="text-error text-[14px]">Hình ảnh không hợp lệ</p>
    </div>
  );
}
