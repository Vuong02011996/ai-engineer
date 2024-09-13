import { Stack, Typography } from "@mui/material";
import * as React from "react";
import { SelectHourAndMinute } from "../select";

export interface IChooseTimeProps {
  setStartTime: any;
  startTime: any;
  setendTime: any;
  endTime: any;
  maxTime: any;
  minTime: any;
}

export function ChooseTime(props: IChooseTimeProps) {
  const { setStartTime, startTime, setendTime, endTime, maxTime, minTime } =
    props;
  return (
    <Stack
      sx={{
        p: "12px 0",
        justifyContent: "space-between",
      }}
      direction={"row"}
      spacing={1}
    >
      <Stack direction="row" spacing={1}>
        <Typography
          sx={{
            color: "#222",
            textAlign: "right",
            fontFamily: "Roboto",
            fontSize: "14px",
            fontStyle: "normal",
            fontWeight: 500,
            lineHeight: "normal",
            marginTop: "auto",
            pt: "23px",
          }}
        >
          Từ
        </Typography>
        <SelectHourAndMinute
          value={startTime}
          setValue={setStartTime}
          maxTime={maxTime()}
        />
      </Stack>
      <Stack direction="row" spacing={1}>
        <Typography
          sx={{
            color: "#222",
            textAlign: "right",
            fontFamily: "Roboto",
            fontSize: "14px",
            fontStyle: "normal",
            fontWeight: 500,
            lineHeight: "normal",
            marginTop: "auto",
            pt: "23px",
          }}
        >
          Đến
        </Typography>
        <SelectHourAndMinute
          value={endTime}
          setValue={setendTime}
          minTime={minTime()}
        />
      </Stack>
    </Stack>
  );
}
