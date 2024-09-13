export type TimeOption =
  | "ALL"
  | "YESTERDAY"
  | "7-DAY-AGO"
  | "30-DAY-AGO"
  | "90-DAY-AGO"
  | "180-DAY-AGO"
  | "365-DAY-AGO";

export const timeOption: TimeOption[] = [
  "ALL",
  "YESTERDAY",
  "7-DAY-AGO",
  "30-DAY-AGO",
  "90-DAY-AGO",
  "180-DAY-AGO",
  "365-DAY-AGO",
];
export function renderTimeOption(type: TimeOption) {
  switch (type) {
    case "ALL":
      return "Tất cả";
    case "YESTERDAY":
      return "Ngày hôm qua";
    case "7-DAY-AGO":
      return "7 ngày qua";
    case "30-DAY-AGO":
      return "30 ngày qua";
    case "90-DAY-AGO":
      return "90 ngày qua";
    case "180-DAY-AGO":
      return "180 ngày qua";
    case "365-DAY-AGO":
      return "365 ngày qua";

    default:
      return "";
  }
}
