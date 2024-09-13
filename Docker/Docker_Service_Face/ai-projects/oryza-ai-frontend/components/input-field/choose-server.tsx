import { serverApi } from "@/api-client/server";
import { serviceTypeApi } from "@/api-client/setting/service-type";
import { SelectCustom } from "@/components/common/select/select";
import { SelectModel } from "@/models/select";
import * as React from "react";
import { useEffect, useState } from "react";
import AutoCompleteCustom from "../common/autocomplete";

export interface IChooseServerProps {
  defaultValue?: string;
  textError?: string;
  name: string;
}

export function ChooseServer(props: IChooseServerProps) {
  const [options, setOptions] = useState<SelectModel[]>([]);

  const getServer = async () => {
    try {
      let { data } = await serviceTypeApi.getAll({
        page: 0,
        page_break: false,
        data_search: "",
      });

      let option: SelectModel[] = data.data.map((item: any) => {
        return {
          id: item?.id ?? "",
          name: item?.name ?? "",
        };
      });

      setOptions(option);
    } catch (error) {}
  };

  useEffect(() => {
    getServer();
  }, [props?.defaultValue]);

  return (
    <SelectCustom
      title={"Chọn loại service"}
      required
      name={props.name}
      defaultValue={props?.defaultValue ?? ""}
      listSelect={options}
      textError={props?.textError ?? ""}
    />
  );
}
