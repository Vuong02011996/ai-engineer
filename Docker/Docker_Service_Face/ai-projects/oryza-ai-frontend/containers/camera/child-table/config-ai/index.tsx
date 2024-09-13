import { TypeServiceKey } from "@/constants/type-service";
import { useEffect, useState } from "react";
import {
  getCameraTraffictSettings,
  getCrowdSettings,
  getForgottenSettings,
  getLoiteringSettings,
  getIllegalParkingSettings,
  getPlateNumberSettings,
  getTamperingSettings,
  getUniformSettings,
  getTripwireSettings,
  getLaneViolationSettings, 
  getLeavingSettings,
  getObjAttrSettings
} from "./lib";
import { ConfigAICrowdDialog } from "@/components/dialog/config-ai-crowd";
import { useAuth } from "@/hooks/auth-hook";
import { enqueueSnackbar } from "notistack";
import { ResultEnum } from "@/constants/enum";
import useHandleError from "@/hooks/useHandleError";
import { ConfigAIPlateNumberDialog } from "@/components/dialog/config-ai-plate-number";
import { ConfigAILoiteringDialog } from "@/components/dialog/config-ai-loitering";
import { ConfigAIIllegalParkingDialog } from "@/components/dialog/config-ai-illegal-parking";
import { uniformApi } from "@/api-client/identification-profile/uniform";
import { CongigUniformDialog } from "@/components/dialog/config-ai-uniform";
import { ConfigItemsForgottenDialog } from "@/components/dialog/config-ai-items-forgotten";
import { itemsForgottenApi } from "@/api-client/identification-profile/items-forgotten";
import { ConfigAITamperingDialog } from "@/components/dialog/config-ai-tampering";
import { tamperingApi } from "@/api-client/identification-profile/tampering";
import { ConfigCameraTraffictDialog } from "@/components/dialog/config-ai-camera-traffict";
import { cameraTraffictApi } from "@/api-client/identification-profile/camera-traffict";
import { ConfigAILaneViolationDialog } from "@/components/dialog/config-ai-lane-violation";
import { ConfigAITripwireDialog } from "@/components/dialog/config-ai-tripwire";
import { ConfigAILeavingDialog } from "@/components/dialog/config-ai-leaving"; 
import { ConfigAIObjAttrDialog } from "@/components/dialog/config-ai-obj-attr";

import { 
  tripwireApi, 
  loiteringApi, 
  laneViolationApi,
  plateNumberApi,
  crowdApi,
  illegalParkingApi,
  leavingApi,
  objAttrApi
} from "@/api-client/setting_ai_process";
import { get } from "http";

export interface IConfigAiProps {
  processId: string;
  cameraId: string;
  keyAI: TypeServiceKey;
  open: boolean;
  handleClose: () => void;
}

export function ConfigAi(props: IConfigAiProps) {
  const { open, handleClose } = props;
  const [data, setData] = useState<any>(null);
  const { profile } = useAuth();
  const handleError = useHandleError();

  let name_ai_setting = "";
  let api = null;
  switch (props.keyAI) {
    case TypeServiceKey.lane_violation:
      name_ai_setting = "lấn làn ";
      break;
    case TypeServiceKey.line_violation:
      name_ai_setting = "lấn vạch ";
      break;
    case TypeServiceKey.wrong_way:
      name_ai_setting = "đi ngược chiều ";
      break;
    case TypeServiceKey.loitering:
      name_ai_setting = "lảng vảng ";
      break;
    case TypeServiceKey.intrusion:
      name_ai_setting = "xâm nhập ";
      break;
    case TypeServiceKey.leaving:
      name_ai_setting = "rời vị trí ";
      break;
    case TypeServiceKey.obj_attr:
      name_ai_setting = "thuộc tính đối tượng ";
      api = objAttrApi;
      break;
    default:
      break;
  }

  const getData = async () => {
    let dataSetting = {
      id: props.cameraId,
      setting: null,
      crowdData: null,
      process_id: props.processId,
    };

    switch (props.keyAI) {
      case TypeServiceKey.CROWD_DETECTION_EXCHANGES:
        dataSetting.crowdData = await getCrowdSettings(props.cameraId);
        break;
      case TypeServiceKey.DETECT_ITEMS_FORGOTTEN_EXCHANGES:
        dataSetting.setting = await getForgottenSettings(props.cameraId);
        break;
      case TypeServiceKey.IDENTIFY_UNIFORMS_EXCHANGES:
        dataSetting.setting = await getUniformSettings(props.cameraId);
        break;
      case TypeServiceKey.plate_number:
        dataSetting.setting = await getPlateNumberSettings(props.cameraId);
        break;
      case TypeServiceKey.loitering:
      case TypeServiceKey.intrusion:
        dataSetting.setting = await getLoiteringSettings(props.cameraId, props.keyAI);
        break;
      case TypeServiceKey.CAMERA_TAMPERING_EXCHANGES:
        dataSetting.setting = await getTamperingSettings(props.cameraId);
        break;
      case TypeServiceKey.CAMERA_TRAFFIC_SIGNAL_EXCHANGES:
        dataSetting.setting = await getCameraTraffictSettings(props.cameraId);
        break;
      case TypeServiceKey.illegal_parking:
        dataSetting.setting = await getIllegalParkingSettings(props.cameraId);
        break;
      case TypeServiceKey.tripwire:
        dataSetting.setting = await getTripwireSettings(props.cameraId);
        break
      case TypeServiceKey.lane_violation: 
      case TypeServiceKey.line_violation:
      case TypeServiceKey.wrong_way:
        dataSetting.setting = await getLaneViolationSettings(props.cameraId, props.keyAI);
        break;
      case TypeServiceKey.leaving:
        dataSetting.setting = await getLeavingSettings(props.cameraId);
        break
      case TypeServiceKey.obj_attr:
        dataSetting.setting = await getObjAttrSettings(props.cameraId);
        break;
      default:
        break;
    }
    console.log('props', props);
    console.log('dataSetting', dataSetting);
    setData(dataSetting);
  };

  useEffect(() => {
    getData();
  }, [props.cameraId, props.keyAI]);

  // crow
  const handleCreateCrow = async (formData: any) => {
    if (data?.crowdData) {
      return await handleUpdateCrow(formData);
    } else {
      try {
        const payload = {
          ...formData,
          camera_id: data.id,
          company_id: profile?.company?.id,
        };
        await crowdApi.create(payload);
        enqueueSnackbar("Cấu hình AI phát hiện đám đông thành công", {
          variant: "success",
        });

        return ResultEnum.success;
      } catch (error) {
        handleError(error, "Cấu hình AI phát hiện đám đông không thành công");
        return ResultEnum.error;
      }
    }
  };
  const handleUpdateCrow = async (formData: any) => {
    try {
      const payload = {
        ...formData,
        camera_id: data.id,
        company_id: profile?.company?.id,
      };

      await crowdApi.update(payload, data.crowdData?.id ?? "");
      enqueueSnackbar("Cập nhật cấu hình AI phát hiện đám đông thành công", {
        variant: "success",
      });
      return ResultEnum.success;
    } catch (error) {
      handleError(error, "Cập nhật cấu hình AI phát hiện đám đông không thành công");
      return ResultEnum.error;
    }
  };

  // plate number
  const handleCreatePlateNumber = async (formData: any) => {
    if (data?.setting) {
      return await handleUpdatePlateNumber(formData);
    } else {
      try {
        const payload = {
          camera_id: data.id,
          company_id: profile?.company?.id,
          line: formData?.boundary,
          object_detect: formData?.object_detect,
          image_url: formData?.image_url,
        };
        await plateNumberApi.create(payload);
        enqueueSnackbar("Cấu hình AI nhận diện biển số thành công", {
          variant: "success",
        });

        return ResultEnum.success;
      } catch (error) {
        handleError(error, "Cấu hình AI nhận diện biển số không thành công");
        return ResultEnum.error;
      }
    }
  };

  const handleUpdatePlateNumber = async (formData: any) => {
    try {
      const payload = {
        line: formData?.boundary,
        object_detect: formData?.object_detect,
        image_url: formData?.image_url,
      };

      await plateNumberApi.update(payload, data.setting?.id ?? "");
      enqueueSnackbar("Cập nhật cấu hình AI biển số thành công", {
        variant: "success",
      });

      return ResultEnum.success;
    } catch (error) {
      handleError(error, "Cập nhật cấu hình AI biển số không thành công");
      return ResultEnum.error;
    }
  };
  // illegal parking
  const handleCreateIllegalParking = async (formData: any) => {
    if (data?.setting) {
      return await handleUpdateIllegalParking(formData);
    } else {
      try {
        const payload = {
          ...formData,
          camera_id: data.id,
          company_id: profile?.company?.id,
        };
        await illegalParkingApi.create(payload);
        enqueueSnackbar("Cấu hình AI phát hiện vi phạm đậu đỗ trái phép thành công", {
          variant: "success",
        });
        return ResultEnum.success;
      } catch (error) {
        handleError(error, "Cấu hình AI phát hiện vi phạm đậu đỗ trái phép không thành công");
        return ResultEnum.error;
      }
    }
  };

  const handleUpdateIllegalParking = async (formData: any) => {
    try {
      const payload = {
        ...formData,
        camera_id: data.id,
        company_id: profile?.company?.id,
      };

      await illegalParkingApi.update(payload, data.setting?.id ?? "");
      enqueueSnackbar("Cập nhật cấu hình AI phát hiện đậu đỗ trái phép thành công", {
        variant: "success",
      });

      return ResultEnum.success;
    } catch (error) {
      handleError(error, "Cập nhật cấu hình AI phát hiện đậu đỗ trái phép không thành công");
      return ResultEnum.error;
    }
  };

  // loitering
  const handleCreateLoitering = async (formData: any) => {
    if (data?.setting) {
      return await handleUpdateLoitering(formData);
    } else {
      let name_ai_setting = "";
      try {
        const payload = {
          ...formData,
          key_ai: props.keyAI,
          camera_id: data.id,
          company_id: profile?.company?.id,
        };
        console.log('handleCreateLoitering payload:', payload);

        await loiteringApi.create(payload);
        enqueueSnackbar(`Cấu hình AI phát hiện ${name_ai_setting}thành công`, {
          variant: "success",
        });
        return ResultEnum.success;
      } catch (error) {
        handleError(error, `Cấu hình AI phát hiện ${name_ai_setting}không thành công`);
        return ResultEnum.error;
      }
    }
  };

  const handleUpdateLoitering = async (formData: any) => {
    try {
      const payload = {
        ...formData,
        camera_id: data.id,
        company_id: profile?.company?.id,
      };

      await loiteringApi.update(payload, data.setting?.id ?? "");
      enqueueSnackbar(`Cập nhật cấu hình AI phát hiện ${name_ai_setting} thành công`, {
        variant: "success",
      });

      return ResultEnum.success;
    } catch (error) {
      handleError(error, `Cập nhật cấu hình AI phát hiện ${name_ai_setting} không thành công`);
      return ResultEnum.error;
    }
  };

  // uniform
  const handleCreateUniform = async (formData: any) => {
    if (data?.setting) {
      return await handleUpdateUniform(formData);
    } else {
      try {
        const payload = {
          ...formData,
          camera_id: data.id,
          company_id: profile?.company?.id,
        };
        await uniformApi.create(payload);
        enqueueSnackbar("Cấu hình AI nhận diện đồng phục thành công", {
          variant: "success",
        });

        return ResultEnum.success;
      } catch (error) {
        handleError(error, "Cấu hình AI nhận diện đồng phục không thành công");
        return ResultEnum.error;
      }
    }
  };

  const handleUpdateUniform = async (formData: any) => {
    try {
      const payload = {
        ...formData,
        camera_id: data.id,
        company_id: profile?.company?.id,
      };

      await uniformApi.update(payload, data.setting?.id ?? "");
      enqueueSnackbar("Cập nhật cấu hình AI nhận diện đồng phục thành công", {
        variant: "success",
      });

      return ResultEnum.success;
    } catch (error) {
      handleError(error, "Cập nhật cấu hình AI nhận diện đồng phục không thành công");
      return ResultEnum.error;
    }
  };

  // forgotten items
  const handleCreateForgotten = async (formData: any) => {
    if (data?.setting) {
      return await handleUpdateForgotten(formData);
    } else {
      try {
        const payload = {
          ...formData,
          camera_id: data.id,
          company_id: profile?.company?.id,
        };
        await itemsForgottenApi.create(payload);
        enqueueSnackbar("Cấu hình AI phát hiện bỏ rơi thành công", {
          variant: "success",
        });

        return ResultEnum.success;
      } catch (error) {
        handleError(error, "Cấu hình AI phát hiện bỏ rơi không thành công");
        return ResultEnum.error;
      }
    }
  };

  const handleUpdateForgotten = async (formData: any) => {
    try {
      const payload = {
        ...formData,
        camera_id: data.id,
        company_id: profile?.company?.id,
      };

      await itemsForgottenApi.update(payload, data.setting?.id ?? "");
      enqueueSnackbar("Cập nhật cấu hình AI phát hiện bỏ rơi thành công", {
        variant: "success",
      });

      return ResultEnum.success;
    } catch (error) {
      handleError(error, "Cập nhật cấu hình AI phát hiện bỏ rơi không thành công");
      return ResultEnum.error;
    }
  };

  // tampering

  const handleCreateTampering = async (formData: any) => {
    if (data?.setting) {
      return await handleUpdateTampering(formData);
    } else {
      try {
        const payload = {
          ...formData,
          camera_id: data.id,
          company_id: profile?.company?.id,
        };
        await tamperingApi.create(payload);
        enqueueSnackbar("Cấu hình AI phát hiện phá hoại thành công", {
          variant: "success",
        });
        return ResultEnum.success;
      } catch (error) {
        handleError(error, "Cấu hình AI phát hiện phá hoại không thành công");
        return ResultEnum.error;
      }
    }
  };

  const handleUpdateTampering = async (formData: any) => {
    try {
      const payload = {
        ...formData,
        camera_id: data.id,
        company_id: profile?.company?.id,
      };

      await tamperingApi.update(payload, data.setting?.id ?? "");
      enqueueSnackbar("Cập nhật cấu hình AI phát hiện phá hoại thành công", {
        variant: "success",
      });
      return ResultEnum.success;
    } catch (error) {
      handleError(error, "Cập nhật cấu hình AI phát hiện phá hoại không thành công");
      return ResultEnum.error;
    }
  };

  // Camera Traffic
  /**
   * Asynchronous function to create a camera traffic configuration.
   */
  async function createCameraTraffict(formData: any) {
    try {
      const payload = {
        camera_id: data.id,
        company_id: profile?.company?.id,
        light_boundary: formData.boundary,
        image_url: formData.image_url,
      };

      await cameraTraffictApi.create(payload);
      const msg = "Cấu hình AI nhận diện tín hiệu đèn giao thông thành công";
      enqueueSnackbar(msg, { variant: "success" });

      return ResultEnum.success;
    } catch (error) {
      const msg = "Cấu hình AI nhận diện tín hiệu đèn giao thông không thành công";
      handleError(error, msg);
      return ResultEnum.error;
    }
  }

  /**
   * Asynchronous function to update a camera traffic configuration.
   */
  const updateCameraTraffict = async (formData: any) => {
    try {
      const payload = {
        light_boundary: formData.boundary,
        image_url: formData.image_url,
        camera_id: data.id,
        company_id: profile?.company?.id,
      };

      await cameraTraffictApi.update(payload, data.setting?.id ?? "");
      const msg = "Cập nhật cấu hình AI nhận diện tín hiệu đèn giao thông thành công";
      enqueueSnackbar(msg, { variant: "success" });

      return ResultEnum.success;
    } catch (error) {
      const msg =
        "Cập nhật cấu hình AI nhận diện tín hiệu đèn giao thông không thành công";
      handleError(error, msg);
      return ResultEnum.error;
    }
  };

  /**
   * Asynchronous function to submit a camera traffic configuration.
   */
  const submitCameraTraffict = async (formData: any) => {
    if (data?.setting) {
      return await updateCameraTraffict(formData);
    } else {
      return await createCameraTraffict(formData);
    }
  };

  const handleCreateTripwire = async (formData: any) => {
    if (data?.setting) {
      return await handleUpdateTripwire(formData);
    } else {
      try {
        const payload = {
          ...formData,
          camera_id: data.id,
          company_id: profile?.company?.id,
        };
        await tripwireApi.create(payload);
        enqueueSnackbar("Cấu hình AI Hàng rào ảo thành công", {
          variant: "success",
        });
        return ResultEnum.success;
      } catch (error) {
        handleError(error, "Cấu hình AI Hàng rào ảo không thành công");
        return ResultEnum.error;
      }
    }
  }

  const handleUpdateTripwire = async (formData: any) => {
    try {
      const payload = {
        ...formData,
        camera_id: data.id,
        company_id: profile?.company?.id,
      };

      await tripwireApi.update(payload, data.setting?.id ?? "");
      enqueueSnackbar("Cập nhật cấu hình AI Hàng rào ảo thành công", {
        variant: "success",
      });

      return ResultEnum.success;
    } catch (error) {
      handleError(error, "Cập nhật cấu hình AI Hàng rào ảo không thành công");
      return ResultEnum.error;
    }
  } 


  const handleCreateLaneViolation = async (formData: any) => {
    if (data?.setting) {
      return await handleUpdateLaneViolation(formData);
    } else {
      let name_ai_setting = "";
      try {
        const payload = {
          ...formData,
          key_ai: props.keyAI,
          camera_id: data.id,
          company_id: profile?.company?.id,
        };
        console.log('handleCreateLaneViolation payload:', payload);

        await laneViolationApi.create(payload);
        enqueueSnackbar(`Cấu hình AI ${name_ai_setting}thành công`, {
          variant: "success",
        });
        return ResultEnum.success;
      } catch (error) {
        handleError(error, `Cấu hình AI ${name_ai_setting}không thành công`);
        return ResultEnum.error;
      }
    }
  };  

  const handleUpdateLaneViolation = async (formData: any) => {
    try {
      const payload = {
        ...formData,
        camera_id: data.id,
        company_id: profile?.company?.id,
      };
      console.log('handleUpdateLaneViolation payload:', payload);
      await laneViolationApi.update(payload, data.setting?.id ?? "");
      enqueueSnackbar(`Cập nhật cấu hình AI ${name_ai_setting}thành công`, {
        variant: "success",
      });

      return ResultEnum.success;
    } catch (error) {
      handleError(error, `Cập nhật cấu hình AI ${name_ai_setting}thành công`);
      return ResultEnum.error;
    }
  };


  const handleCreateLeaving = async (formData: any) => {
    if (data?.setting) {
      return await handleUpdateLeaving(formData);
    } else {
      try {
        const payload = {
          ...formData,
          key_ai: props.keyAI,
          camera_id: data.id,
          company_id: profile?.company?.id,
        };
        console.log('handleCreateLeaving payload:', payload);

        await leavingApi.create(payload);
        enqueueSnackbar(`Cấu hình AI ${name_ai_setting}thành công`, {
          variant: "success",
        });
        return ResultEnum.success;
      } catch (error) {
        handleError(error, `Cấu hình AI ${name_ai_setting}không thành công`);
        return ResultEnum.error;
      }
    }
  }; 

  const handleUpdateLeaving = async (formData: any) => {
    try {
      const payload = {
        ...formData,
        camera_id: data.id,
        company_id: profile?.company?.id,
      };
      console.log('handleUpdateLeaving payload:', payload);
      await leavingApi.update(payload, data.setting?.id ?? "");
      enqueueSnackbar(`Cập nhật cấu hình AI ${name_ai_setting}thành công`, {
        variant: "success",
      });

      return ResultEnum.success;
    } catch (error) {
      handleError(error, `Cập nhật cấu hình AI ${name_ai_setting}thành công`);
      return ResultEnum.error;
    }
  };

  const handleCreateSetting = async (formData: any) => {
    if (!api) {
      return ResultEnum.error;
    }
    if (data?.setting) {
      return await handleUpdateSetting(formData);
    } else {
      try {
        const payload = {
          ...formData,
          key_ai: props.keyAI,
          camera_id: data.id,
          company_id: profile?.company?.id,
        };
        await api.create(payload);
        enqueueSnackbar(`Cấu hình AI ${name_ai_setting}thành công`, {
          variant: "success",
        });
        return ResultEnum.success;
      } catch (error) {
        handleError(error, `Cấu hình AI ${name_ai_setting}không thành công`);
        return ResultEnum.error;
      }
    }
  }

  const handleUpdateSetting = async (formData: any) => {
    if (!api) {
      return ResultEnum.error;
    }
    try {
      const payload = {
        ...formData,
        camera_id: data.id,
        company_id: profile?.company?.id,
      };
      await api.update(payload, data.setting?.id ?? "");
      enqueueSnackbar(`Cập nhật cấu hình AI ${name_ai_setting}thành công`, {
        variant: "success",
      });
      return ResultEnum.success;
    } catch (error) {
      handleError(error, `Cập nhật cấu hình AI ${name_ai_setting}thành công`);
      return ResultEnum.error;
    }
  }
    
  switch (props.keyAI) {
    case TypeServiceKey.CROWD_DETECTION_EXCHANGES:
      return (
        <ConfigAICrowdDialog
          open={open}
          handleClose={handleClose}
          submit={handleCreateCrow}
          data={data}
        />
      );
    case TypeServiceKey.plate_number:
      return (
        <ConfigAIPlateNumberDialog
          open={open}
          handleClose={handleClose}
          submit={handleCreatePlateNumber}
          data={data}
        />
      );
    case TypeServiceKey.loitering:
    case TypeServiceKey.intrusion: 
    // intrusion is actually loitering with waiting time = 0
      return (
        <ConfigAILoiteringDialog
          open={open}
          handleClose={handleClose}
          submit={handleCreateLoitering}
          data={data}
          keyAI={props.keyAI}
        />
      );
    case TypeServiceKey.IDENTIFY_UNIFORMS_EXCHANGES:
      return (
        <CongigUniformDialog
          open={open}
          handleClose={handleClose}
          submit={handleCreateUniform}
          data={data}
        />
      );
    case TypeServiceKey.DETECT_ITEMS_FORGOTTEN_EXCHANGES:
      return (
        <ConfigItemsForgottenDialog
          open={open}
          handleClose={handleClose}
          submit={handleCreateForgotten}
          data={data}
        />
      );
    case TypeServiceKey.CAMERA_TAMPERING_EXCHANGES:
      return (
        <ConfigAITamperingDialog
          open={open}
          handleClose={handleClose}
          submit={handleCreateTampering}
          data={data}
        />
      );
    case TypeServiceKey.CAMERA_TRAFFIC_SIGNAL_EXCHANGES:
      return (
        <ConfigCameraTraffictDialog
          open={open}
          handleClose={handleClose}
          submit={submitCameraTraffict}
          data={data}
        />
      );
    case TypeServiceKey.illegal_parking:
      return (
        <ConfigAIIllegalParkingDialog
          open={open}
          handleClose={handleClose}
          submit={handleCreateIllegalParking}
          data={data}
        />
      )
    case TypeServiceKey.tripwire:
      return (
        <ConfigAITripwireDialog
          open={open}
          handleClose={handleClose}
          submit={handleCreateTripwire}
          data={data}
        />
      )
    case TypeServiceKey.lane_violation:
    case TypeServiceKey.line_violation:
    case TypeServiceKey.wrong_way:
      return (
        <ConfigAILaneViolationDialog
          open={open}
          handleClose={handleClose}
          submit={handleCreateLaneViolation}
          data={data}
          keyAI={props.keyAI}
        />
      )
    case TypeServiceKey.leaving:
      return (
        <ConfigAILeavingDialog
          open={open}
          handleClose={handleClose}
          submit={handleCreateLeaving}
          data={data}
        />
      )
    case TypeServiceKey.obj_attr:
      return (
        <ConfigAIObjAttrDialog
          open={open}
          handleClose={handleClose}
          submit={handleCreateSetting}
          data={data}
        />
      )
    default:
      return <></>;
  }
}
