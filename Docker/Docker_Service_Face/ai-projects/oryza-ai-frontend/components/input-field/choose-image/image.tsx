import { personApi } from "@/api-client/identification-profile/person";
import { MAX_SIZE_UPLOAD } from "@/constants/config";
import { AnimatePresence, motion } from "framer-motion";
import Image from "next/image";
import { enqueueSnackbar } from "notistack";
import { useEffect, useState } from "react";
import { ImageItem, RemoveBtn, UploadImage } from "./ui";
import { ImageError } from "./ui/image-error";
import { FileInterface } from "./interface";
import { uuidv4 } from "@/utils/global-func";

interface UrlItem {
  url: string;
  name: string;
  id: string;
  isError: boolean;
}

export interface IImageComponentProps {
  setFiles: React.Dispatch<React.SetStateAction<FileInterface[]>>;
  files: FileInterface[];
  defaultImage?: string[];
}

export function ImageComponent(props: IImageComponentProps) {
  // ************** --init state-- *****************
  const { files, setFiles, defaultImage } = props;
  const [loading, setLoading] = useState(false);
  const [url, setUrl] = useState<UrlItem[]>([]);

  async function urlToFile(url: string): Promise<File> {
    const response = await fetch(url);
    const blob = await response.blob();

    // Extract the filename from the URL
    const filename = url.substring(url.lastIndexOf("/") + 1);
    const mimeType = blob.type; // Get the MIME type from the Blob

    return new File([blob], filename, { type: mimeType });
  }

  useEffect(() => {
    if (defaultImage) {
      const processImages = async () => {
        const urlPromises = defaultImage.map(async (url) => {
          const file = await urlToFile(url);
          const check = await checkImage(file);
          const id = uuidv4();

          return {
            id,
            url,
            name: url,
            isError: !check,
            file: check ? file : null,
          };
        });

        const results = await Promise.all(urlPromises);

        const validFiles = results
          // .filter((result) => !result.isError)
          .map((result) => {
            let item: FileInterface = {
              id: result.id,
              file: result.isError ? null : result.file,
            };
            return item;
          });

        const urlResults = results.map(({ id, url, name, isError }) => ({
          id,
          url,
          name,
          isError,
        }));

        setUrl(urlResults);
        setFiles(validFiles);
      };

      processImages();
    }
  }, [defaultImage]);

  // *************** REMOVE IMAGE ***************
  const removeImage = (urlItem: UrlItem) => {
    setUrl(url.filter((item) => item.id !== urlItem.id));
    setFiles(files.filter((item) => item.id !== urlItem.id));
  };

  // *************** CHECK IMAGE ***************
  const checkImage = async (file: File): Promise<boolean> => {
    if (files.length > 0) {
      const isFileExists = files.some(
        (e: FileInterface) => e.file !== null && e.file.name === file.name
      );
      if (isFileExists) {
        enqueueSnackbar("Hình ảnh đã tồn tại", { variant: "error" });
        return false;
      }
    }

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);

    try {
      await personApi.checkImage(formData);
      return true;
    } catch (error) {
      enqueueSnackbar("Hình ảnh không hợp lệ", { variant: "error" });
      return false;
    } finally {
      setLoading(false);
    }
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
    const check = await checkImage(file);
    if (!check) return;

    const id = uuidv4();
    const newUrl: UrlItem = {
      url: URL.createObjectURL(file),
      name: file.name,
      id: id,
      isError: false,
    };
    const newFile: FileInterface = {
      id: id,
      file: file,
    };

    setUrl([newUrl, ...url]);
    setFiles([newFile, ...files]);
  };

  return (
    <div className="grid grid-cols-2 gap-4 max-h-[400px] overflow-auto">
      <UploadImage handleUploadImage={handleUploadImage} loading={loading} />

      <AnimatePresence initial={false}>
        {url.length > 0 &&
          url.map((item: UrlItem) => {
            return (
              <ImageItem
                key={item.name}
                isError={item.isError}
                urlError={item.url}
              >
                {item.isError ? (
                  <>
                    <ImageError />
                    <RemoveBtn onClick={() => removeImage(item)} />
                  </>
                ) : (
                  <>
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
                    <RemoveBtn onClick={() => removeImage(item)} />
                  </>
                )}
              </ImageItem>
            );
          })}
      </AnimatePresence>
    </div>
  );
}
