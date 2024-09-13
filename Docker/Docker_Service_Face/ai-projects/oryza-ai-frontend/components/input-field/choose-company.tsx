import { companyApi } from "@/api-client/setting/company";
import { SelectCustom } from "@/components/common/select/select";
import { SelectModel } from "@/models/select";
import * as React from "react";
import { useEffect, useState } from "react";

export interface IChooseCompanyProps {
  defaultValue?: string;
  textError?: string;
  name: string;
  disabled?: boolean;
  value?: string;
  setValue: (value: string) => void;
}

interface Company {
  id: string;
  name: string;
  domain: string;
  created: string;
  modified: string;
}

export function ChooseCompany(props: IChooseCompanyProps) {
  const [options, setOptions] = useState<SelectModel[]>([]);

  const getCompany = async () => {
    try {
      let { data } = await companyApi.getAll({
        page: 0,
        page_break: false,
        data_search: "",
      });
      console.log('data from api', data);
      let option: SelectModel[] = data.data
        // .filter((item: Company) => !item.name.startsWith("_"))
        .map((item: Company) => {
          return {
            id: item?.id ?? "",
            name: item?.name ?? "",
          };
        });
      console.log("option", option);

      setOptions(option);
    } catch (error) {}
  };

  useEffect(() => {
    getCompany();
  }, [props?.defaultValue]);

  return (
    <SelectCustom
      title="Chọn công ty"
      required={props ? false : true}
      name={props.name}
      defaultValue={props?.defaultValue ?? ""}
      listSelect={options}
      textError={props?.textError ?? ""}
      disabled={props.disabled}
      value={props.value}
      setValue={props.setValue}
    />
  );
}
