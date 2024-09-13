import { InputLabel, Typography } from "@mui/material";
import * as React from "react";

export interface ILabelImageProps {}

export function LabelImage(props: ILabelImageProps) {
  return (
    <InputLabel
      sx={{ fontSize: 14, fontWeight: 400, color: "#55595D", mb: "6px" }}
    >
      Hình ảnh dùng để nhận diện{" "}
    </InputLabel>
  );
}
