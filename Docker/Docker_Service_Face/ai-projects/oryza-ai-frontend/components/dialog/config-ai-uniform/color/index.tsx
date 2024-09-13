import { rgbToHex } from "@/utils/global-func";
import { Typography } from "@mui/material";
import clsx from "clsx";
import ntc from "ntcjs";
import { useEffect, useState } from "react";
import { RgbColor, RgbColorPicker } from "react-colorful";
import { getColorName } from "./function";
import { useDebouncedValue } from "@mantine/hooks";

export interface IColorPickerProps {
  color: string;
  onChange: (value: string) => void;
}

export function ColorPicker(props: IColorPickerProps) {
  const [color, setColor] = useState<RgbColor>({
    r: 255,
    b: 255,
    g: 255,
  });
  const [colorName, setColorName] = useState("Trắng");
  const [debouncValue] = useDebouncedValue(props.color, 100);
  useEffect(() => {
    if (props.color) {
      const oldColor = JSON.parse(props.color);
      const rbgColor = {
        r: oldColor[0],
        g: oldColor[1],
        b: oldColor[2],
      };
      setColor(rbgColor);
      handleUpdateName(rbgColor);
    }
  }, [debouncValue]);

  const handleUpdateName = (newColor: RgbColor) => {
    const { r, g, b } = newColor;
    const hexColor = rgbToHex(r, g, b);
    const n_match = ntc.name(hexColor);
    const name = getColorName(n_match);
    setColorName(name);
  };

  return (
    <>
      <label className="text-[14px] font-medium text-grayOz mb-[6px] ">
        Màu sắc đồng phục
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
      </label>
      <div className="color-picker-wrapper">
        <RgbColorPicker
          color={color}
          onChange={(newColor: RgbColor) => {
            // setColor(newColor);
            const { r, g, b } = newColor;

            props.onChange(JSON.stringify([r, g, b]));
            // handleUpdateName(newColor);
          }}
        />
      </div>
      <div className="pt-4">
        <div className="flex gap-2">
          <div className="flex gap-2 flex-1 ">
            <p className="text-[#AFAFAF] text-[16px]">
              RGB: <span className="text-grayOz">{colorName}</span>{" "}
            </p>
            <div
              className={clsx(
                "w-[22px] h-[22px] rounded-[2px] shadow-shadown1"
              )}
              style={{
                backgroundColor: rgbToHex(color.r, color.g, color.b),
              }}
            />
          </div>
          <div className="flex w-[150px]  justify-between h-[32px]">
            <input
              type="number"
              className="text-center w-full items-center border-t border-b border-l border-[#dddddd] rounded-tl-[8px] rounded-bl-[8px] outline-none"
              placeholder="-"
              value={color.r}
              onChange={(e) => {
                let value = Number(e.target.value);

                const newColor = {
                  ...color,
                  r: value < 0 ? 0 : value > 255 ? 255 : value,
                };
                // setColor(newColor);
                const { r, g, b } = newColor;
                props.onChange(JSON.stringify([r, g, b]));

                // handleUpdateName({
                //   ...color,
                //   r: value < 0 ? 0 : value > 255 ? 255 : value,
                // });
              }}
            />
            <input
              type="number"
              className="text-center w-full items-center border border-[#dddddd] outline-none"
              placeholder="-"
              value={color.g}
              onChange={(e) => {
                let value = Number(e.target.value);

                const newColor = {
                  ...color,
                  g: value < 0 ? 0 : value > 255 ? 255 : value,
                };
                // setColor(newColor);
                const { r, g, b } = newColor;

                props.onChange(JSON.stringify([r, g, b]));
                // handleUpdateName({
                //   ...color,
                //   g: value < 0 ? 0 : value > 255 ? 255 : value,
                // });
              }}
            />
            <input
              type="number"
              className="text-center w-full items-center border-t border-b border-r border-[#dddddd] rounded-tr-[8px] rounded-br-[8px] outline-none"
              placeholder="-"
              value={color.b}
              onChange={(e) => {
                let value = Number(e.target.value);
                const newColor = {
                  ...color,
                  b: value < 0 ? 0 : value > 255 ? 255 : value,
                };
                // setColor(newColor);
                const { r, g, b } = newColor;
                props.onChange(JSON.stringify([r, g, b]));

                // handleUpdateName({
                //   ...color,
                //   b: value < 0 ? 0 : value > 255 ? 255 : value,
                // });
              }}
            />
          </div>
        </div>
      </div>
    </>
  );
}
