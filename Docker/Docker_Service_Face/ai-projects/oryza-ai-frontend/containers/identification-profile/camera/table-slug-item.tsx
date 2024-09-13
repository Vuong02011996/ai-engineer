import { personCameraApi } from "@/api-client/identification-profile/person-camera";
import CheckboxCustom2 from "@/components/common/checkbox/checbox-2";
import { CameraRes } from "@/interfaces/camera";
import { PersonCompanyCamera } from "@/interfaces/identification-profile/person";
import { Stack, styled } from "@mui/material";
import { enqueueSnackbar } from "notistack";
import { useState } from "react";
import { ImageStack } from "../ui/image-stack";
import { QuichAction, QuickActionType } from "./quick-action";

const ItemRow = styled(Stack)(({ theme }) => ({
  minWidth: "1200px",
  ":hover": {
    ".img-item:nth-of-type(2)": {
      left: "50px",
    },
    ".img-item:nth-of-type(3)": {
      left: "100px",
    },
    ".img-item:nth-of-type(4)": {
      left: "150px",
    },
    ".image-number": {
      opacity: 0,
    },
  },
  ".img-item:nth-of-type(2)": {
    opacity: 0.8,
  },
  ".img-item:nth-of-type(3)": {
    opacity: 0.5,
  },
  ".img-item:nth-of-type(4)": {
    opacity: 0.2,
  },
  alignItems: "center",
  display: "flex",
  flexDirection: "row",
}));

export interface ICameraSlugTableItemProps {
  data: PersonCompanyCamera;
  index: number;
  updateState: (idCameraPerson: boolean) => void;
  setTotal: any;
  isOn: boolean;
  camera: CameraRes | null;
  handleCheck: (value: string, checked: boolean) => void;
  checkedIds: string[];
  loading: boolean;
  action: null | "create" | "delete";
}

export function CameraSlugTableItem(props: ICameraSlugTableItemProps) {
  const { data, camera, handleCheck, checkedIds } = props;
  const [loading, setloading] = useState(false);

  // * * * * * * * * ADD PERSON TO CAMERA * * * * * * * * *
  const hanldeAddPersonToCamera = async () => {
    if (loading || !camera) return;

    setloading(true);
    try {
      const payload = {
        person_id: data.id,
        id_camera: camera.id,
        key_camera: camera.brand_camera?.key,
      };

      await personCameraApi.create(payload);
      props.updateState(true);
    } catch (error) {
      enqueueSnackbar("Bật giám sát không thành công", {
        variant: "error",
      });
    } finally {
      setloading(false);
    }
  };

  // * * * * * * * * REMOVE PERSON TO CAMERA * * * * * * * * *
  const hanldeRemovePersonToCamera = async () => {
    if (!data.id || loading || !camera) return;
    setloading(true);

    try {
      const payload = {
        key_camera: camera?.brand_camera?.key,
        id_camera: camera?.id,
      };
      await personCameraApi.remove(payload, data.id_person_camera);
      props.updateState(false);
    } catch (error) {
      console.log("hanldeRemovePersonToCamera error: ", error);
    } finally {
      setloading(false);
    }
  };

  function checkLoading() {
    if (props.action === "delete" && props.loading && props.isOn) {
      return true;
    }
    if (props.action === "create" && props.loading && !props.isOn) {
      return true;
    }
    return false;
  }

  return (
    <ItemRow className=" table-row-custom">
      {/* <div className="w-[60px] py-6 flex justify-center">
        {_renderCheckbox(data.id, handleCheck, checkedIds)}
      </div> */}
      <div className="w-[60px] py-6 flex justify-center">
        {_renderText(props.index.toString())}
      </div>
      <div className="w-[20%] py-6 flex justify-start">
        {_renderText(data.name)}
      </div>
      <div className="w-[10%] py-6 flex justify-start">
        {_renderText(
          data?.other_info?.gender === "male"
            ? "Nam"
            : data?.other_info?.gender === "female"
            ? "Nữ"
            : ""
        )}
      </div>
      <div className="w-[20%] py-6 flex justify-start">
        {_renderText(data?.other_info?.address)}
      </div>

      <div className="w-[30%] py-6 flex justify-start">
        <ImageStack images={data.images} />
      </div>
      <div className="w-[20%] py-6 pr-10 flex justify-end">
        <QuichAction
          type={
            checkLoading() || loading ? "LOADING" : props.isOn ? "ON" : "OFF"
          }
          onClick={(type: QuickActionType) => {
            switch (type) {
              case "ON":
                hanldeRemovePersonToCamera();
                break;
              case "OFF":
                hanldeAddPersonToCamera();
                break;
              default:
                break;
            }
          }}
        />
      </div>
    </ItemRow>
  );
}

function _renderText(text?: string) {
  return <p className="font-medium text-grayOz text-sm">{text || "--"}</p>;
}
function _renderCheckbox(value: any, handleCheck: any, checkedIds: string[]) {
  return (
    <div>
      <CheckboxCustom2
        checked={checkedIds.includes(value)}
        onChange={(checked) => {
          handleCheck(value, checked);
        }}
      />
    </div>
  );
}
