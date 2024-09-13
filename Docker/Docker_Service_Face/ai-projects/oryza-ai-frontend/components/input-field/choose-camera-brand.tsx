import { cameraBrandApi } from "@/api-client/setting/camera-brand";
import { SelectModel } from "@/models/select";
import * as React from "react";
import { useEffect, useState } from "react";
import AutoCompleteCustom from "../common/autocomplete";

export interface IChooseCameraBrandProps {
  name: string;
  label: string;
  value?: any;
  defaultValue?: string;
  textError?: string;
  onChange?: (v: any) => void;
}

export function ChooseCameraBrand(props: IChooseCameraBrandProps) {
  const [options, setOptions] = useState<SelectModel[]>([]);
  const [value, setValue] = useState<SelectModel | null>(null);

  const getData = React.useCallback(async () => {
    try {
      let { data } = await cameraBrandApi.getAll({
        page: 0,
        page_break: false,
        data_search: "",
      });
      let option = data.data.map((item: any) => {
        return {
          id: item?.id ?? "",
          name: item?.name ?? "",
        };
      });

      if (props?.value) {
        let findValue = option.find(
          (item: any) => item?.id === props?.value?.id
        );

        if (findValue) {
          setValue(findValue);
        }
      }

      setOptions(option);
    } catch (error) {}
  }, [props.value]);

  useEffect(() => {
    getData();
  }, [getData]);

  // useEffect(() => {
  //   if (props.value) {
  //     handleGetBrandByid(props.value?.id).then((data) => {
  //       let newOptionsItem = {
  //         id: data?.id ?? "",
  //         name: data?.name ?? "",
  //       };

  //       setOptions((prev) => {
  //         let item = prev.find((o) => o?.id === newOptionsItem?.id);

  //         return item ? prev : [newOptionsItem, ...prev];
  //       });
  //     });
  //   }
  // }, [props.value]);

  // // get brand by id
  // const handleGetBrandByid = async (brand_id: string) => {
  //   try {
  //     let { data } = await cameraBrandApi.getById(brand_id);
  //     return data;
  //   } catch (error) {
  //     return null;
  //   }
  // };

  // const value = React.useCallback(() => {
  //   let item = options.find((o) => o.id === props.value?.id);
  //   if (item) {
  //     return item;
  //   }
  //   return null;
  // }, [props.value, options]);

  return (
    <AutoCompleteCustom
      label={props.label}
      options={options}
      required
      value={value}
      name={props.name}
      textError={props.textError}
      onChange={(event, value, reason, details) => {
        console.log({ event, value, reason, details });
        setValue(value);
        if (props.onChange) props.onChange(value?.id);
      }}
    />
    // <SelectCustom
    //   title={props.label}
    //   required
    //   name={props.name}
    //   value={props.value}
    //   listSelect={options}
    //   textError={props.textError}
    //   setValue={(e) => {
    //     if (props.onChange) props.onChange(e);
    //   }}
    //   onLoadMore={() => {
    //     if (total <= options.length) return;
    //     cameraBrandApi
    //       .getAll({
    //         page: Math.ceil(options.length / LIMIT_ITEM),
    //         page_break: true,
    //       })
    //       .then((res: any) => {
    //         let newItem = res.data.data.map((item: any) => {
    //           return {
    //             id: item?.id ?? "",
    //             name: item?.name ?? "",
    //           };
    //         });
    //         setOptions([...options, ...newItem]);
    //       })
    //       .catch((error) => {
    //         console.log("Error: ", error);
    //       });
    //   }}
    // />
  );
}
