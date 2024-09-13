import * as React from "react";
import { SelectCustom } from "../common/select/select";
import { useEffect, useState } from "react";
import { webhookApi } from "@/api-client/setting/webhook";
import { SelectModel } from "@/models/select";

export interface IChooseTokenTypeProps {
  defaultValue?: string;
}

export function ChooseTokenType(props: IChooseTokenTypeProps) {
  const [option, setoption] = useState<SelectModel[]>([]);

  const getTokenType = async () => {
    try {
      let { data } = await webhookApi.getTokenType();
      setoption(
        data?.data.map((value: any) => {
          let item: SelectModel = {
            id: value,
            name: value,
          };
          return item;
        })
      );
    } catch (error) {}
  };

  useEffect(() => {
    getTokenType();
  }, []);

  return (
    <SelectCustom
      listSelect={option}
      title={"Loại xác thực"}
      name="auth_type"
      defaultValue={props.defaultValue}
    />
  );
}
