import { SelectCustom } from "@/components/common/select/select";
import { SelectModel } from "@/models/select";
import * as React from "react";
import { useState } from "react";
import { SxProps } from '@mui/system';

export interface IChooseVMSServerTypeProps {
  name: string;
  label: string;
  defaultValue?: string;
  textError?: string;
  className?: string; 
  sx?: SxProps;
  required?: boolean;
}

export function ChooseVMSServerType(props: IChooseVMSServerTypeProps) {
  const [options, setOptions] = useState<SelectModel[]>([
    {
      id: "nx",
      name: "Server VMS NX",
    },
    {
      id: "oz",
      name: "Server VMS Oryza",
    },
  ]);

  return (
    <div className={props.className} style={{ width: '100%' }}>
      <SelectCustom
        title={props.label}
        name={props.name}
        defaultValue={props.defaultValue}
        listSelect={options}
        textError={props.textError}
        sx={props.sx}
        required={props.required}
      />
    </div>
  );
}
