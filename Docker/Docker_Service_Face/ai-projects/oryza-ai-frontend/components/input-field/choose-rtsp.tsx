import { cameraApi } from "@/api-client/camera";
import { SelectCustom } from "@/components/common/select/select";
import * as React from "react";
import { useEffect, useState } from "react";

export interface IChooseRtspProps {
  name: string;
  label: string;
  value?: string;
  onChange?: (value: string) => void;
  camera: any;
  textError?: string;
}

type Option = {
  id: any;
  name: string;
  value: any;
};

export function ChooseRtsp(props: IChooseRtspProps) {
  const [options, setOptions] = useState<Option[]>([]);

  const getRtspOptions = async (camera: any) => {
    try {
      const res = await cameraApi.getListRtsp(camera.id);
      const options = res.data.data.map((item: string, index: number) => {
        return {
            id: item,
            value: item,
            name: item,
          };
        }
      );
      setOptions(options);
      } catch (error) {
        console.log("Error: ", error);
      }
    };

  const onChange = (value: any) => {
    if (props.onChange) props.onChange(value);
  };

  const resetForm = () => {
    setOptions([]);
  };

  useEffect(() => {
    // Reset the form and fetch new options when the camera prop changes
    resetForm();
    getRtspOptions(props.camera);
  }, [props.camera]);

  return (
    <SelectCustom
      title={props.label}
      required
      name={props.name}
      listSelect={options}
      textError={props.textError}
      setValue={onChange}
      value={props.value}
    />
  );
}