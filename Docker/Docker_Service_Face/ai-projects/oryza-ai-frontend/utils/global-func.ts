import { URL_PRODUCT } from "@/constants/domain";
import { useRouter } from "next/router";

export function calculateDaysBetweenDates(
  date1: string | number | Date | null,
  date2: string | number | Date | null
) {
  if (date1 === null || date2 === null) return 1;

  // Convert date strings to Date objects
  let firstDate: any = new Date(date1);
  let secondDate: any = new Date(date2);

  firstDate.setHours(0);
  firstDate.setMinutes(0);
  firstDate.setSeconds(0);

  secondDate.setHours(0);
  secondDate.setMinutes(0);
  secondDate.setSeconds(0);

  if (firstDate && secondDate && firstDate > secondDate) {
    [firstDate, secondDate] = [secondDate, firstDate];
  }

  firstDate.setFullYear(
    firstDate.getFullYear(),
    firstDate.getMonth(),
    firstDate.getDate()
  );
  secondDate.setFullYear(
    secondDate.getFullYear(),
    secondDate.getMonth(),
    secondDate.getDate() + 1
  );

  // Calculate the difference in milliseconds
  let timeDifference = Math.abs(secondDate - firstDate);

  // Convert the time difference to days
  let daysDifference = timeDifference / (24 * 60 * 60 * 1000);

  // Round the result to 2 decimal places
  let roundedResult = daysDifference.toFixed(2);

  return parseFloat(roundedResult);
}
export function areDatesEqual(date1: Date, date2: Date) {
  return (
    date1.getFullYear() === date2.getFullYear() &&
    date1.getMonth() === date2.getMonth() &&
    date1.getDate() === date2.getDate()
  );
}
export function convertToDate(dateString: string) {
  let date = new Date(Number(dateString as string) * 1000);

  if (isNaN(date.getTime())) {
    return null;
  }
  if (!dateString) return null;
  return date;
}

export function uuidv4() {
  return "10000000100040008000100000000000".replace(/[018]/g, (c) =>
    (
      +c ^
      (crypto.getRandomValues(new Uint8Array(1))[0] & (15 >> (+c / 4)))
    ).toString(16)
  );
}
export function generateURLWithQueryParams(
  url: string,
  queryParamsObject: { [key: string]: string | undefined }
) {
  const keys = Object.keys(queryParamsObject);
  const query = keys.map((key) => `${key}=${queryParamsObject[key]}`).join("&");

  return `${url}?${query}`;
}

export function formatNumberWithCommas(value: number): string {
  try {
    const number = Number(value);
    return number.toLocaleString("en-US");
  } catch (error) {
    return value.toString();
  }
}
export function renderSchemaProduct(name: string, url?: string) {
  const router = useRouter();
  const schema = {
    "@context": "https://schema.org/",
    "@type": "BreadcrumbList",
    itemListElement: [
      {
        "@type": "ListItem",
        position: 1,
        name: "Trang chủ",
        item: "https://product.oryzacloud.vn/",
      },
      {
        "@type": "ListItem",
        position: 2,
        name: name,
        item: url ?? URL_PRODUCT + router.asPath,
      },
    ],
  };
  return schema;
}
export const rgbToHex = (r: number, g: number, b: number): string => {
  const componentToHex = (c: number): string => {
    const hex = c.toString(16);
    return hex.length === 1 ? "0" + hex : hex;
  };

  return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
};
export const calculateStartTime = (currentTime: Date, hours = 0, days = 0) => {
  return new Date(
    currentTime.getFullYear(),
    currentTime.getMonth(),
    currentTime.getDate() - days,
    currentTime.getHours() - hours,
    currentTime.getMinutes(),
    currentTime.getSeconds()
  );
};
export function addIdToArray(array: any[]) {
  return array.map((item, index) => {
    return {
      ...item,
      id: index,
    };
  });
}
