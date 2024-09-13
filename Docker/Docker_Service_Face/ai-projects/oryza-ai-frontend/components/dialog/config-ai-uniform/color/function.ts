import colors from "./color-2.json";

export function getColorName([hex, name, check]: [string, string, boolean]) {
  let item = colors.find((item) => item.hex === hex.replaceAll("#", ""));
  if (item) {
    return item.vietnam;
  }
  return name;
}
