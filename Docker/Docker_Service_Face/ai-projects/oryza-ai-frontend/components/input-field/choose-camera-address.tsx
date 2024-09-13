import { geoApi } from "@/api-client/geo-unit";
import { SelectModel } from "@/models/select";
import * as React from "react";
import { useEffect, useState } from "react";
import AutoCompleteCustom from "../common/autocomplete";

export interface IChooseGeoUnitProps {
  name: string;
  label: string;
  value?: any;
  defaultValue?: string;
  required?: boolean;
  textError?: string;
  onChange?: (v: any) => void;
  parentId?: string | null; // Add parentId prop
  type: string; // Add type prop
}

export function ChooseGeoUnit(props: IChooseGeoUnitProps) {
  const [options, setOptions] = useState<SelectModel[]>([]);
  const [value, setValue] = useState<SelectModel | null>(null);

  const getData = React.useCallback(async () => {
    try {
      let { data } = await geoApi.getList({
        keyword: "",
        parent_id: props.parentId ?? null, // Use parentId to filter data
        type: props.type, // Use type to filter data
      });
      let option = data.data.map((item: any) => {
        return {
          id: item?.id ?? "",
          name: item?.name ?? "",
        };
      });

      setOptions(option);
    } catch (error) {
      console.error('Error fetching geo units:', error);
    }
  }, [props.parentId, props.type]); // Add parentId and type to dependency array

  useEffect(() => {
    getData();
    setValue(null); // Reset value when parentId changes
  }, [getData]);

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