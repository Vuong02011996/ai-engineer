import { serviceApi } from "@/api-client/service";
import { SelectCustom } from "@/components/common/select/select";
import { SelectModel } from "@/models/select";
import * as React from "react";
import { useEffect, useState } from "react";

export interface IChooseServiceProps {
  name: string;
  label: string;
  defaultValue?: string;
  textError?: string;
  onChange?: (value: any) => void;
  value?: string;
}

export function ChooseService(props: IChooseServiceProps) {
  const [options, setOptions] = useState<SelectModel[]>([]);

  const getService = async () => {
    serviceApi
      .getAll({ page_break: false })
      .then((res: any) => {
        setOptions(
          res.data.data.map((item: any) => {
            return {
              id: item?.id ?? "",
              name: item?.name ?? "",
              type: item?.type,
            };
          })
        );
      })
      .catch((error) => {
        console.log("Error: ", error);
      });
  };

  const onChange = (value: any) => {
    if (props.onChange) props.onChange(options.find((i) => i?.id === value));
  };

  useEffect(() => {
    getService();
  }, []);
  return (
    <SelectCustom
      title={props.label}
      required
      name={props.name}
      defaultValue={props.defaultValue}
      listSelect={options}
      textError={props.textError}
      setValue={onChange}
      value={props.value}
    />
  );
}
