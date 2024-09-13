import { styled } from "@mui/material/styles";
import { DateCalendar } from "@mui/x-date-pickers/DateCalendar";
import { PickersDay, PickersDayProps } from "@mui/x-date-pickers/PickersDay";
import { PickerSelectionState } from "@mui/x-date-pickers/internals";
import dayjs, { Dayjs } from "dayjs";
import "dayjs/locale/vi";
import isBetweenPlugin from "dayjs/plugin/isBetween";
import * as React from "react";
import KeyboardArrowLeftRoundedIcon from "@mui/icons-material/KeyboardArrowLeftRounded";
import { IconButton } from "@mui/material";
dayjs.extend(isBetweenPlugin);

interface CustomPickerDayProps extends PickersDayProps<Dayjs> {
  dayIsBetween: boolean;
  isFirstDay: boolean;
  isLastDay: boolean;
}

const CustomPickersDay = styled(PickersDay, {
  shouldForwardProp: (prop) =>
    prop !== "dayIsBetween" && prop !== "isFirstDay" && prop !== "isLastDay",
})<CustomPickerDayProps>(({ theme, dayIsBetween, isFirstDay, isLastDay }) => ({
  ...(dayIsBetween && {
    background: "#E3E5E5",
    "&:hover, &:focus": {
      background: "#E3E5E5",
    },
  }),
  ...(isFirstDay && {
    background: "#55595D !important",
    color: "#fff !important",
    "&:hover, &:focus": {
      background: "#55595D",
      color: "#fff",
    },
    borderRadius: "5px !important",
    position: "relative",
  }),
  ...(isLastDay && {
    color: "#fff !important",
    background: "#55595D !important",
    "&:hover, &:focus": {
      color: "#fff",
      background: "#55595D",
    },
    borderRadius: "5px !important",
  }),
})) as React.ComponentType<CustomPickerDayProps>;

function Day(
  props: PickersDayProps<Dayjs> & {
    selectedDay?: Dayjs | null;
    highlightedDays?: Date[];
  }
) {
  const { highlightedDays = [], day, selectedDay, ...other } = props;

  if (selectedDay == null) {
    return <PickersDay day={day} {...other} />;
  }
  var arr = [...highlightedDays];

  arr.sort(function (a, b) {
    return a?.getTime() - b?.getTime();
  });

  const start = arr[0];
  const end = arr[arr.length - 1];

  const dayIsBetween = day.isBetween(start, end, null, "[]");
  const isFirstDay = day.isSame(start, "day");
  const isLastDay = day.isSame(end, "day");

  return (
    <CustomPickersDay
      {...other}
      day={day}
      sx={{
        fontSize: 14,
        fontWeight: 500,
        color: "#222",
        borderRadius: "5px",
        fontFamily: "Roboto",
      }}
      dayIsBetween={dayIsBetween}
      isFirstDay={isFirstDay}
      isLastDay={isLastDay}
      showDaysOutsideCurrentMonth
    />
  );
}

export interface ICalendaCompProps {
  value: Dayjs | null;
  handleDateChange: (
    value: dayjs.Dayjs | null,
    selectionState?: PickerSelectionState | undefined
  ) => void;
  highlightedDay: () => void;
}

export function CalendaComp(props: ICalendaCompProps) {
  const { value, handleDateChange, highlightedDay } = props;
  return (
    <DateCalendar
      value={value}
      onChange={handleDateChange}
      views={["year", "month", "day"]}
      slots={{
        day: Day,
        calendarHeader: (time) => {
          let current = time.currentMonth;
          let month = dayjs(current).get("M") + 1;
          let year = dayjs(current).get("year");
          let timeString = `Tháng ${month} năm ${year}`;
          return (
            <div className="flex flex-row justify-center items-center">
              <IconButton
                size="small"
                onClick={() => {
                  const oneMonthAgo = dayjs(current).subtract(1, "month");
                  time.onMonthChange(oneMonthAgo, "left");
                }}
              >
                <KeyboardArrowLeftRoundedIcon />
              </IconButton>
              <p className="text-blackOz text-[16px] font-semibold min-w-40 text-center">
                {timeString}
              </p>
              <IconButton
                size="small"
                onClick={() => {
                  const oneMonthLater = dayjs(current).add(1, "month");
                  time.onMonthChange(oneMonthLater, "left");
                }}
              >
                <KeyboardArrowLeftRoundedIcon className="rotate-180" />
              </IconButton>
            </div>
          );
        },
      }}
      slotProps={{
        day: {
          selectedDay: value,
          highlightedDays: highlightedDay(),
        } as any,
      }}
      dayOfWeekFormatter={(weekday) => `${weekday.format("dd")}`}
      sx={{
        "& .MuiPickersDay-root": {
          "&.Mui-selected": {
            background: "#007DC0",
            color: "#fff",
            "&:hover, &:focus": {
              background: "#007DC0",
              color: "#fff",
            },
          },
          px: 0,
          mx: 0,
          fontSize: 14,
          fontWeight: 500,
          color: "#222",
          width: "100%",
          borderRadius: "0px",
        },
        "& .MuiDayCalendar-header": {
          "& .MuiDayCalendar-weekDayLabel": {
            width: "100%",
            fontSize: "12px",
            fontWeight: 600,
            color: "#AFAFAF",
          },
        },
        "& .MuiPickersDay-dayOutsideMonth": {
          color: "#22222220",
        },
        textTransform: "capitalize",
        width: "350px",
        height: "auto",
      }}
      disableHighlightToday={true}
    />
  );
}
