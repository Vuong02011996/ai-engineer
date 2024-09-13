import { personApi } from "@/api-client/identification-profile/person";
import { MAX_SIZE_UPLOAD } from "@/constants/config";
import { AnimatePresence, motion } from "framer-motion";
import Image from "next/image";
import { enqueueSnackbar } from "notistack";
import { useState } from "react";
import { ImageItem, RemoveBtn, UploadImage } from "./ui";

export interface IImageComponentProps {
  setFiles: any;
  files: any[];
}

export function ImageComponent(props: IImageComponentProps) {
  // ************** --init state-- *****************
  const { files, setFiles } = props;
  const [loading, setLoading] = useState(false);
  const [url, setUrl] = useState<{ url: string; name: string }[]>([]);

  // *************** REMOVE IMAGE ***************
  const removeImage = (imageName: string) => {
    setUrl(url.filter((item) => item.name !== imageName));
    setFiles(files.filter((item) => item.name !== imageName));
  };

  // *************** HANDLE UPLOAD IMAGE ***************
  const handleUploadImage = async (e: any) => {
    if (!e.target.files[0] || loading) return;
    const file = e.target.files[0];

    if (file.size > MAX_SIZE_UPLOAD) {
      const errMsg = `Dung lượng tối đa ${MAX_SIZE_UPLOAD / 1024 / 1024}mb`;
      enqueueSnackbar(errMsg, { variant: "error" });
      return;
    }

    setUrl([{ name: file.name, url: URL.createObjectURL(file) }, ...url]);
    setFiles([file, ...files]);
  };

  return (
    <div className="grid grid-cols-2  overflow-auto">
      <UploadImage handleUploadImage={handleUploadImage} loading={loading} />

      <AnimatePresence initial={false}>
        {url.length > 0 &&
          url.map((item) => {
            return (
              <ImageItem key={item.name}>
                <Image
                  key={item.url}
                  src={item.url}
                  alt="avatar"
                  width={1000}
                  height={1000}
                  style={{
                    width: "100%",
                    height: "100%",
                    objectFit: "contain",
                  }}
                />
                <RemoveBtn onClick={() => removeImage(item.name)} />
              </ImageItem>
            );
          })}
      </AnimatePresence>
    </div>
  );
}
