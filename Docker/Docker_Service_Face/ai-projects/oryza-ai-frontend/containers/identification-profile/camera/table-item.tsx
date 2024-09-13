import { PaginateKey } from "@/constants/paginate-key";
import { ICameraAI } from "@/interfaces/identification-profile/camera-ai";
import { Stack } from "@mui/material";
import { useRouter } from "next/navigation";

export interface ICameraTableItemProps {
  data: ICameraAI;
  index: number;
  reload: any;
  setTotal: any;
  currentPage: string;
}

export function CameraTableItem(props: ICameraTableItemProps) {
  const { data } = props;

  const router = useRouter();

  const handleClick = () => {
    localStorage.setItem(PaginateKey.identification_camera, props.currentPage);
    router.push(
      `/identification-profile/camera/user/${
        data.id
      }?type_camera=${data.type_camera?.replaceAll(" ", "")}`,
      {}
    );
  };

  return (
    <Stack
      className=" table-row-custom"
      sx={{
        minWidth: "1200px",
        alignItems: "center",
        display: "flex",
        flexDirection: "row",
      }}
    >
      <div onClick={handleClick} className="w-[60px] py-6 flex justify-center">
        {_renderText(props.index.toString())}
      </div>

      <div onClick={handleClick} className="w-[40%] py-6 flex justify-start">
        {_renderText(data?.name)}
      </div>
      <div onClick={handleClick} className="w-[30%] py-6 flex justify-start">
        {_renderText("Camera AI")}
      </div>
      <div onClick={handleClick} className="w-[30%] py-6 flex justify-start">
        {_renderText(data.ip_address)}
      </div>
      {/* <div onClick={handleClick} className="w-[25%] py-6 flex justify-start">
        {_renderText("--")}
      </div> */}
    </Stack>
  );
}

function _renderText(text: string) {
  return <p className="font-medium text-grayOz text-sm">{text}</p>;
}
