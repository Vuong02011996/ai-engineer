import { Loading } from "@/components/common";
import * as React from "react";
import Image from "next/image";
import { VisuallyHiddenInput } from "./visually-hidden-input";

export interface IUploadimageProps {
  handleUploadImage: (e: React.ChangeEvent<HTMLInputElement>) => void;
  loading: boolean;
}

export function UploadImage(props: IUploadimageProps) {
  const { handleUploadImage, loading } = props;
  return (
    <label htmlFor="pick-image" className="cursor-pointer">
      {loading ? (
        <div className="h-[150px] bg-[#F8F8F8] flex flex-col items-center justify-center gap-[6px]">
          <Loading />
        </div>
      ) : (
        <div className="h-[150px] bg-[#F8F8F8] flex flex-col items-center justify-center gap-[6px]">
          <Image src="/icons/upload.svg" alt="avatar" width={32} height={32} />
          <p className="text-[#64686D] text-[14px]">Tải hình ảnh lên</p>
        </div>
      )}

      <VisuallyHiddenInput
        disabled={loading}
        id="pick-image"
        type="file"
        accept="image/*"
        onChange={handleUploadImage}
      />
    </label>
  );
}
