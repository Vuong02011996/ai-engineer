import { serviceTypeApi } from "@/api-client/setting";
import CheckboxCustom from "@/components/common/checkbox";
import Scrollbar from "@/components/common/scrollbar";
import { SelectModel } from "@/models/select";
import { Stack, Typography } from "@mui/material";
import * as React from "react";
import { useEffect, useState } from "react";

export interface IChooseTypeServiceMultipleProps {
  onChange: (v: string[]) => void;
  value: string[];
}

export function ChooseTypeServiceMultiple(
  props: IChooseTypeServiceMultipleProps
) {
  const [options, setOptions] = useState<SelectModel[]>([]);

  const hanldeChange = (newItem: string, checked: boolean) => {
    if (checked) {
      props.onChange([...props.value, newItem]);
    } else {
      props.onChange(props.value.filter((i) => i != newItem));
    }
  };

  const getServiceType = async () => {
    serviceTypeApi
      .getAll({ page: 0, page_break: true, data_search: "" })
      .then((res: any) => {
        setOptions(
          res.data.data.map((item: any) => {
            return {
              id: item?.id ?? "",
              name: item?.name ?? "",
            };
          })
        );
      })
      .catch((error) => {
        console.log("Error: ", error);
      });
  };

  useEffect(() => {
    getServiceType();
  }, []);
  return (
    <Stack
      sx={{
        position: "fixed",
        top: "calc(50% - 300px)",
        left: "calc(50% + 250px)",
        background: "white",
        width: "250px",
        p: 2,
        borderRadius: "11px",
        boxShadow: "0px 1px 10px 0px rgba(34, 34, 34, 0.10)",
        padding: "16px",
      }}
      spacing={1}
    >
      <Typography sx={{ fontSize: 14, fontWeight: 400, color: "#55595D" }}>
        Các chức năng AI của camera{" "}
        <Typography
          component={"span"}
          sx={{
            color: "#E42727",
            fontSize: 13,
            display: "inline-block",
          }}
        >
          (✶)
        </Typography>
      </Typography>

      <div className="h-[250px]">
        <Scrollbar>
          {options.map((option) => {
            return (
              <div key={option.id} className="flex space-x-2 items-center ">
                <CheckboxCustom
                  label={option.name}
                  onChange={(checked) => {
                    hanldeChange(option.id, checked);
                  }}
                  defaultChecked={
                    props?.value.length > 0
                      ? props?.value?.includes(option.id)
                      : false
                  }
                />
              </div>
            );
          })}
        </Scrollbar>
      </div>
    </Stack>
  );
}
