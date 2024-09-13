import { serviceTypeApi } from "@/api-client/setting";
import { SelectModel } from "@/models/select";
import CloseIcon from "@mui/icons-material/Close";
import {
  FormControl,
  FormControlLabel,
  FormLabel,
  Grid,
  Radio,
  RadioGroup,
  Stack,
  Typography,
} from "@mui/material";
import { useEffect, useState } from "react";

export interface IChooseServiceTypeProps {
  defaultValue?: string;
  textError?: string;
  name: string;
  value?: string;
  onChange?: (value: string) => void;
}

export function ChooseServiceType(props: IChooseServiceTypeProps) {
  const [options, setOptions] = useState<SelectModel[]>([]);

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
    <FormControl
      className="w-full"
      sx={{
        "& .Mui-focused": {
          color: "#55595d",
        },
        userSelect: "none",
      }}
    >
      <FormLabel
        id={props.name}
        className="font-normal text-[14px] focus:text-red-700 "
        sx={{ color: "#55595d !important" }}
      >
        Chọn loại AI <span className="text-[#E42727] text-[13px]">(✶)</span>
      </FormLabel>
      <RadioGroup
        aria-labelledby={props.name}
        defaultValue={props.defaultValue}
        name={props.name}
        value={props.value}
        onChange={(e) => {
          if (props.onChange) props.onChange(e.target.value);
        }}
        sx={{
          display: "flex",
          flexDirection: "row",
        }}
      >
        <Grid container>
          {options.map((item) => (
            <Grid key={item.id} item xs={4}>
              <FormControlLabel
                value={item.id}
                control={
                  <Radio
                    className=""
                    size="small"
                    sx={{
                      color: "#55595d",
                    }}
                  />
                }
                label={<p className="text-grayOz">{item.name}</p>}
                sx={{
                  "& .Mui-checked": {
                    "& + .MuiFormControlLabel-label > p": {
                      color: "#323232",
                    },
                  },
                }}
              />
            </Grid>
          ))}
        </Grid>
      </RadioGroup>
      {props.textError && (
        <Stack
          direction={"row"}
          spacing={"5px"}
          sx={{ alignItems: "center", mt: "4px" }}
        >
          <Stack
            sx={{
              width: "13px",
              height: "13px",
              alignItems: "center",
              justifyContent: "center",
              background: "#E42727",
              borderRadius: "50%",
            }}
          >
            <CloseIcon sx={{ color: "#fff", fontSize: 10, fontWeight: 600 }} />
          </Stack>

          <Typography
            sx={{
              fontSize: 12,
              fontWeight: 400,
              color: "#E42727",
            }}
          >
            {props.textError}
          </Typography>
        </Stack>
      )}
    </FormControl>
  );
}
