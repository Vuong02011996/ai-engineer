import { calculateDaysBetweenDates } from "@/utils/global-func";
import { Divider, Stack } from "@mui/material";
import { LocalizationProvider } from "@mui/x-date-pickers";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { PickerSelectionState } from "@mui/x-date-pickers/internals";
import dayjs, { Dayjs } from "dayjs";
import "dayjs/locale/vi";
import * as React from "react";
import { useState } from "react";
import { ActionComp, CalendaComp, ChooseTime } from "./item";

export interface IPickDateCustomProps {
  onclose: () => void;
  handeSubmit: (startDate: Date | null, endDate: Date | null) => void;
  startDate: Date;
  endDate: Date;
}

export default function PickDateCustom(props: IPickDateCustomProps) {
  const { onclose } = props;

  const now = new Date();
  const today = new Date(
    now.getFullYear(),
    now.getMonth(),
    now.getDate(),
    0,
    0
  );

  const currentDate = new Date();

  const [date1, setDate1] = useState<Date | null>(props.startDate);
  const [date2, setDate2] = useState<Date | null>(props.endDate);

  const handleChangeDate1 = (date: Date | null) => {
    setDate1(date);
  };
  const handleChangeDate2 = (date: Date | null) => {
    setDate2(date);
  };

  const [value, setValue] = React.useState<Dayjs | null>(dayjs(props.endDate));

  const handleSubmit = () => {
    let startDate = date1 ? new Date(date1) : null;
    let endDate = date2 ? new Date(date2) : null;

    if (date1 === null && date2 === null) {
      props.handeSubmit(null, null);

      return;
    }

    // Nếu cả date1 và date2 cùng 1 ngày
    if (
      startDate &&
      endDate &&
      startDate.toDateString() === endDate.toDateString()
    ) {
      startDate.setHours(0, 0, 0, 0);
      endDate.setHours(23, 59, 59, 999);
    } else if (startDate && !endDate) {
      // Nếu chỉ có date1 (date2 là null)
      startDate.setHours(0, 0, 0, 0);
      endDate = new Date(startDate);
      endDate.setHours(23, 59, 59, 999);
    }
    if (startDate && endDate && startDate > endDate) {
      [startDate, endDate] = [endDate, startDate];
    }

    if (startDate) {
      startDate.setHours(
        startTime.getHours(),
        startTime.getMinutes(),
        startTime.getSeconds(),
        startTime.getMilliseconds()
      );
    }
    if (endDate) {
      endDate.setHours(
        endTime.getHours(),
        endTime.getMinutes(),
        endTime.getSeconds(),
        endTime.getMilliseconds()
      );
    }

    props.handeSubmit(startDate, endDate);
  };

  function getBeforeDay(daysToSubtract: number | "ALL") {
    if (daysToSubtract === "ALL") {
      setValue(null);
      handleChangeDate1(null);
      handleChangeDate2(null);
    } else {
      if (daysToSubtract === 1) {
        const yesterday = new Date(
          currentDate.getFullYear(),
          currentDate.getMonth(),
          currentDate.getDate() - 1
        );

        const dateBefore = new Date(yesterday);
        dateBefore.setDate(yesterday.getDate() + 1 - daysToSubtract);

        setValue(dayjs(yesterday));
        handleChangeDate1(dateBefore);
        handleChangeDate2(yesterday);
      } else {
        const yesterday = new Date(
          currentDate.getFullYear(),
          currentDate.getMonth(),
          currentDate.getDate()
        );

        const dateBefore = new Date(yesterday);
        dateBefore.setDate(yesterday.getDate() + 1 - daysToSubtract);

        setValue(dayjs(yesterday));
        handleChangeDate1(dateBefore);
        handleChangeDate2(yesterday);
      }
      setStartTime(new Date(2000, 1, 1, 0, 0, 0));
      setendTime(new Date(2000, 1, 1, 23, 59, 59));
    }
  }

  const highlightedDay = () => {
    let date = [];
    if (date1 != null) date.push(date1);
    if (date2 != null) date.push(date2);
    return date;
  };

  const [startTime, setStartTime] = useState<Date>(
    props.startDate ?? new Date(2000, 1, 1, 0, 0, 0)
  );
  const [endTime, setendTime] = useState<Date>(
    props.endDate ?? new Date(2000, 1, 1, 23, 59, 59)
  );

  const handleDateChange = (
    value: dayjs.Dayjs | null,
    selectionState?: PickerSelectionState | undefined
  ) => {
    if (selectionState === "finish") {
      if (date1 === null && date2 === null) {
        setDate1(value!.toDate());
      } else if (date1 !== null && date2 === null) {
        setDate2(value!.toDate());
      } else if (date1 !== null && date2 !== null) {
        setDate1(value!.toDate());
        setDate2(null);
      }
      setStartTime(new Date(2000, 1, 1, 0, 0, 0));
      setendTime(new Date(2000, 1, 1, 23, 59, 59));
    }
    setValue(value);
  };

  const maxTime = () => {
    if (date1 != null && date2 != null) {
      return date1?.getDate() === date2?.getDate() ? endTime : null;
    } else {
      return endTime;
    }
  };

  const minTime = () => {
    if (date1 != null && date2 != null) {
      return date1?.getDate() === date2?.getDate() ? startTime : null;
    } else {
      return startTime;
    }
  };
  const handleClose = () => {
    if (props.startDate) setDate1(new Date(props.startDate));
    if (props.endDate) setDate2(new Date(props.endDate));
    if (props.endDate) setValue(dayjs(props.endDate));

    onclose();
  };

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs} adapterLocale="vi">
      <Stack
        sx={{
          height: "100%",
          padding: "24px",
          background: "white",
        }}
      >
        <Stack
          flex={1}
          sx={{
            overflow: "auto",
            "&::-webkit-scrollbar": {
              width: "2px",
              height: "2px",
            },
            "&::-webkit-scrollbar-thumb": {
              backgroundColor: "transparent",
              borderRadius: "4px",
            },
          }}
        >
          <Stack direction={{ xs: "column-reverse", sm: "row" }} sx={{}}>
            <Stack
              sx={{
                width: "100%",
              }}
            >
              <CalendaComp
                value={value}
                handleDateChange={handleDateChange}
                highlightedDay={highlightedDay}
              />
            </Stack>
          </Stack>
          <Divider />

          <ChooseTime
            setStartTime={setStartTime}
            startTime={startTime}
            setendTime={setendTime}
            endTime={endTime}
            maxTime={maxTime}
            minTime={minTime}
          />
        </Stack>

        <Divider />

        <ActionComp
          handleClose={handleClose}
          handleSubmit={handleSubmit}
          dateNumber={calculateDaysBetweenDates(date1, date2)}
        />
      </Stack>
    </LocalizationProvider>
  );
}
