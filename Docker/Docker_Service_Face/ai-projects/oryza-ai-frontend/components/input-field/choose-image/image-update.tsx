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

interface UrlInterface {
  url: string;
  name: string;
  id: string;
}

export interface ImageUpdateProps {
  data: IPerson;
}

export function ImageUpdateComponent(props: ImageUpdateProps) {
  const { data } = props;
  // ************** --init state-- *****************
  const handleError = useHandleError();
  const [imageId, setImageId] = useState("");
  const [openRemoveDialog, setOpenRemoveDialog] = useState(false);
  const [loading, setLoading] = useState(false);
  const [url, setUrl] = useState<UrlInterface[]>([]);

  // * * * * * * * * INIT URL * * * * * * * * *
  useEffect(() => {
    if (props.data?.images) {
      setUrl(props.data.images.map(({ url, name, id }) => ({ url, name, id })));
    }
  }, [props.data]);

  // * * * * * * * * CHECK IMAGE * * * * * * * * *
  const checkImage = async (file: File): Promise<boolean> => {
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

  // * * * * * * * * HANDLE UPLOAD IMAGE * * * * * * * * *
  const handleUploadImage = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || !e.target.files[0] || loading) return;
    const file = e.target.files[0];

    if (file.size > MAX_SIZE_UPLOAD) {
      enqueueSnackbar(`Dung lượng tối đa ${MAX_SIZE_UPLOAD / 1024 / 1024} MB`, {
        variant: "error",
      });
      return;
    }

    const check = await checkImage(file);
    if (!check) return;

    await handleUpload(file);
  };

  // * * * * * * * * HANDLE REMOVE IMAGE * * * * * * * * *
  const handleRemove = async (image_id: string): Promise<ResultEnum> => {
    if (!data) return ResultEnum.error;
    setLoading(true);

    try {
      await personApi.removeImage(data.id, image_id);
      setUrl((prevUrl) => prevUrl.filter((item) => item.id !== image_id));
      return ResultEnum.success;
    } catch (error) {
      handleError(error, "Thêm mới hồ sơ nhận diện đối tượng không thành công");
      return ResultEnum.error;
    } finally {
      setLoading(false);
    }
  };

  // * * * * * * * * HANDLE UPLOAD IMAGE * * * * * * * * *
  const handleUpload = async (file: File) => {
    if (!data) return;

    setLoading(true);

    try {
      const formData = new FormData();
      formData.append("files", file);
      const res = await personApi.addImage(formData, data.id);
      setUrl((prevUrl) => [
        { name: res.data.name, url: res.data.url, id: res.data.id },
        ...prevUrl,
      ]);
    } catch (error) {
      handleError(error, "Không thể tải lên hình ảnh");
    } finally {
      setLoading(false);
    }
  };

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
              <ImageItem key={item.id}>
                <Image
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
                <RemoveBtn
                  onClick={() => {
                    setImageId(item.id);
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
