import { serviceApi } from "@/api-client/service";
import { SelectCustom } from "@/components/common/select/select";
import { SelectModel } from "@/models/select";
import * as React from "react";
import { useEffect, useState } from "react";

export interface IChooseGenderProps {
  name: string;
  label: string;
  defaultValue?: string;
  textError?: string;
}

export function ChooseGender(props: IChooseGenderProps) {
  const [options, setOptions] = useState<SelectModel[]>([
    {
      id: "male",
      name: "Nam",
    },
    {
      id: "female",
      name: "Nữ",
    },
  ]);

  return (
    <SelectCustom
      title={props.label}
      name={props.name}
      defaultValue={props.defaultValue}
      listSelect={options}
      textError={props.textError}
    />
  );
}
