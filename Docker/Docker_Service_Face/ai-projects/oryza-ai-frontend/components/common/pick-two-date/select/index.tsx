import { Stack, Typography } from "@mui/material";
import { useEffect, useState } from "react";
import { HourMinute } from "./hour-minute";
import { areDatesEqual } from "@/utils/global-func";

export interface ISelectHourAndMinuteProps {
  value: Date | null;
  setValue: (v: Date) => void;
  maxTime?: Date | null;
  minTime?: Date | null;
}

export function SelectHourAndMinute(props: ISelectHourAndMinuteProps) {
  const { value, setValue, maxTime, minTime } = props;

  const [maxHour, setmaxHour] = useState<number | null>(null);
  const [maxMinute, setMaxMinute] = useState<number | null>(null);

  const [minHour, setminHour] = useState<number | null>(null);
  const [minMinute, setMinMinute] = useState<number | null>(null);

  const initValue = () => {
    if (value) {
      let newValue = new Date();
      newValue.setHours(
        value.getHours(),
        value.getMinutes(),
        value.getSeconds(),
        value.getMilliseconds()
      );

      if (maxTime) {
        let newMaxTime = new Date();
        newMaxTime.setHours(
          maxTime.getHours(),
          maxTime.getMinutes(),
          maxTime.getSeconds(),
          maxTime.getMilliseconds()
        );
        if (areDatesEqual(newValue, newMaxTime)) {
          setmaxHour(newMaxTime.getHours());
          if (newValue.getHours() == newMaxTime.getHours()) {
            setMaxMinute(newMaxTime.getMinutes());
          }
        } else {
          setmaxHour(null);
          setMaxMinute(null);
        }
      }

      if (minTime) {
        let newMinTime = new Date();
        newMinTime.setHours(
          minTime.getHours(),
          minTime.getMinutes(),
          minTime.getSeconds(),
          minTime.getMilliseconds()
        );
        if (areDatesEqual(newValue, newMinTime)) {
          setminHour(newMinTime.getHours());
          if (newValue.getHours() == newMinTime.getHours()) {
            setMinMinute(newMinTime.getMinutes());
          }
        } else {
          setminHour(null);
          setMinMinute(null);
        }
      }
    }
  };
  useEffect(() => {
    initValue();
  }, [value, maxTime, minTime]);
  return (
    <Stack direction="row" spacing={"5px"}>
      <HourMinute
        type={"HOUR"}
        onChange={function (v: string): void {
          let event = value ? new Date(value) : new Date();
          event.setHours(parseInt(v));
          setValue(event);
        }}
        value={value ? value.getHours().toString() : "0"}
        max={maxHour}
        min={minHour}
      />
      <Typography
        sx={{ pt: "23px", color: "#222", fontSize: 18, fontWeight: 500 }}
      >
        :
      </Typography>
      <HourMinute
        type={"MINUTE"}
        onChange={function (v: string): void {
          let event = value ? new Date(value) : new Date();
          event.setMinutes(parseInt(v));
          setValue(event);
        }}
        value={value ? value.getMinutes().toString() : "0"}
        max={maxMinute}
        min={minMinute}
      />
    </Stack>
  );
}
