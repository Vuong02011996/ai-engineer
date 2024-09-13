import { SelectModel } from "@/models/select";
import * as React from "react";
import { useState, useEffect } from "react";
import { CameraType } from "@/constants/enum";
import AutoCompleteCustom from "../common/autocomplete";

export interface IChooseCameraTypeProps {
  name: string;
  label: string;
  value: string;
  textError?: string;
  onChange?: (v: any) => void;
  required?: boolean;
}

const cameraTypeNames: { [key in CameraType]: string } = {
  [CameraType.NORMAL_CAMERA]: 'Camera thường',
  [CameraType.PTZ_CAMERA]: 'Camera PTZ',
  [CameraType.AI_CAMERA]: 'Camera AI',
  [CameraType.TRAFFIC_CAMERA]: 'Camera giao thông',
};

export function ChooseCameraType(props: IChooseCameraTypeProps) {
  const [options, setOptions] = useState<SelectModel[]>([]);
  const [value, setValue] = useState<SelectModel | null>(null);
  
  useEffect(() => {
    const cameraTypeOptions = Object.values(CameraType).map((type) => ({
      id: type,
      name: cameraTypeNames[type as CameraType], // Use the mapping for Vietnamese names
    }));
    setOptions(cameraTypeOptions);
  }, []);

  useEffect(() => {
    if (props.value) {
      const findValue = options.find(option => option.id === props.value);
      setValue(findValue || null);
    } else {
      setValue(null);
    }
  }, [props.value, options]);

  return (
    <AutoCompleteCustom
      label={props.label}
      options={options}
      required={props.required}
      value={value}
      name={props.name}
      textError={props.textError}
      onChange={(event, value, reason, details) => {
        console.log({ event, value, reason, details });
        setValue(value);
        if (props.onChange) props.onChange(value?.id);
      }}
    />
  );
}
