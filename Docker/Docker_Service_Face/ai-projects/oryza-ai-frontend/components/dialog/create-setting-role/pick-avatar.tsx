import AddRoundedIcon from "@mui/icons-material/AddRounded";
import { styled } from "@mui/material";
import Image from "next/image";
import { useState } from "react";
import { useEffect } from 'react';

const VisuallyHiddenInput = styled("input")({
  clip: "rect(0 0 0 0)",
  clipPath: "inset(50%)",
  height: 1,
  overflow: "hidden",
  position: "absolute",
  bottom: 0,
  left: 0,
  whiteSpace: "nowrap",
  width: 1,
});

export interface IPickAvatarProps {
  onAvatarChange: (avatarBase64: string) => void;
  currentAvatar?: string; // Add a new prop for the current avatar
}

export function PickAvatar(props: IPickAvatarProps) {
  const [url, setUrl] = useState<string>(props.currentAvatar || ""); // Use the current avatar as the initial state
  const [avatar, setAvatar] = useState();

  useEffect(() => {
    // Cleanup URL.createObjectURL
    return () => {
      if (url) URL.revokeObjectURL(url);
    };
  }, [url]);

  useEffect(() => {
    setUrl(props.currentAvatar || "");
    if (!props.currentAvatar) {
      setAvatar(undefined);
    }
  }, [props.currentAvatar]);

  const handleUploadImage = (e: any) => {
    if (!e.target.files[0]) return;
    const file = e.target.files[0];
    setAvatar(file);
    setUrl(URL.createObjectURL(file));

    const reader = new FileReader();
    reader.onloadend = () => {
      props.onAvatarChange(reader.result as string);
    };
    reader.readAsDataURL(file);
  };
  return (
    <label className="flex flex-row items-center space-x-3 cursor-pointer ">
      {url ? (
        <div className="w-[60px] h-[60px] bg-[#CDD2D1] rounded-full flex items-center justify-center  overflow-hidden relative border border-[#F2F2F2]">
          <Image src={url} alt="avatar" fill className="object-cover" />
        </div>
      ) : (
        <div className="w-[60px] h-[60px] bg-[#CDD2D1] rounded-full flex items-center justify-center border border-[#F2F2F2]">
          <AddRoundedIcon className="text-white" />
        </div>
      )}

      <div>
        <VisuallyHiddenInput
          type="file"
          accept="image/*"
          onChange={handleUploadImage}
        />
        <p className="text-primary text-[14px] font-normal ">
          {url ? "Đổi ảnh đại diện" : "Chọn ảnh đại diện"}
        </p>
      </div>
    
      {/* {url && (
        <button
          onClick={() => {
            setUrl("");
            setAvatar(undefined);
            props.onAvatarChange("");
          }}
          className="text-primary text-[14px] font-normal"
        >
          Xóa ảnh đại diện
        </button>
      )} */}
    </label>
  );
}