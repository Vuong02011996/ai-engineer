import { personApi } from "@/api-client/identification-profile/person";
import { DialogConfirm } from "@/components/dialog/confirm-dialog";
import { MAX_SIZE_UPLOAD } from "@/constants/config";
import { ResultEnum } from "@/constants/enum";
import useHandleError from "@/hooks/useHandleError";
import { IPerson } from "@/interfaces/identification-profile/person";
import { AnimatePresence, motion } from "framer-motion";
import Image from "next/image";
import { enqueueSnackbar } from "notistack";
import { useEffect, useState } from "react";
import { ImageItem, RemoveBtn, UploadImage } from "./ui";
import { uniformApi } from "@/api-client/identification-profile/uniform";

interface UrlInterface {
  url: string;
  name: string;
  id: string;
}

export interface ImageUpdateProps {
  data: any;
}

export function ImageUpdateComponent(props: ImageUpdateProps) {
  const { data } = props;
  const handleError = useHandleError();

  // const [url, setUrl] = useState<string>("");
  const [url, setUrl] = useState<string[]>([]);
  const [imageId, setImageId] = useState("");

  const [loading, setloading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // * * * * * * * * INIT URL * * * * * * * * *
  useEffect(() => {
    if (props.data?.list_image) {
      setUrl(props.data.list_image);
    }
  }, [props.data]);

  const handleUploadImage = async (e: any) => {
    if (!e.target.files[0] || loading) return;
    const file = e.target.files[0];

    if (file.size > MAX_SIZE_UPLOAD) {
      // setError(`Dung lượng tối đa ${MAX_SIZE_UPLOAD / 1024 / 1024}mb`);
      enqueueSnackbar(`Dung lượng tối đa ${MAX_SIZE_UPLOAD / 1024 / 1024}mb`, {
        variant: "error",
      });
      return;
    }

    setError(null);

    await handleUpload(file);
  };

  const handleRemove = async (imageUrl: any) => {
    if (!data) return;
    setloading(true);
    try {
      await uniformApi.deleteSettingCompanyImage(data.id, imageUrl);
      setUrl((prevUrl) => prevUrl.filter((item) => item !== imageUrl));
      setImageId("");
      return ResultEnum.success;
    } catch (error) {
      handleError(error, "Thêm mới hồ sơ nhận diện đối tượng không thành công");
      return ResultEnum.error;
    } finally {
      setloading(false);
    }
  };

  const handleUpload = async (file: any) => {
    if (!data) return;

    setloading(true);
    try {
      let fromData = new FormData();
      fromData.append("file", file);
      let res = await uniformApi.updateSettingCompanyImage(fromData, data.id);
      setUrl([res.data.list_image.at(-1), ...url]);
    } catch (error) {
    } finally {
      setloading(false);
    }
  };

  const [openRemoveDialog, setOpenRemoveDialog] = useState(false);

  return (
    <div className="grid grid-cols-2 gap-4 max-h-[400px] overflow-auto">
      {openRemoveDialog && (
        <DialogConfirm
          close={() => setOpenRemoveDialog(false)}
          action={() => handleRemove(imageId)}
          image={"/icons/bin.svg"}
          title={"Bạn chắc chắn xoá không?"}
          description={"Sau khi xoá, dữ liệu sẽ không được phục hồi."}
        />
      )}
      <UploadImage handleUploadImage={handleUploadImage} loading={loading} />

      <AnimatePresence initial={false}>
        {url.length > 0 &&
          url.map((item) => {
            return (
              <ImageItem key={item}>
                <Image
                  src={item}
                  alt="avatar"
                  width={1000}
                  height={1000}
                  style={{
                    width: "100%",
                    height: "100%",
                    objectFit: "contain",
                  }}
                />
                <RemoveBtn
                  onClick={() => {
                    setImageId(item);
                    setOpenRemoveDialog(true);
                  }}
                />
              </ImageItem>
            );
          })}
      </AnimatePresence>
    </div>
  );
}
