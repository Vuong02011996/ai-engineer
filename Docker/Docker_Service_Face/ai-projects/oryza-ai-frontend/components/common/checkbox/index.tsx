import * as React from "react";
import { styled } from "@mui/material/styles";
import Checkbox, { CheckboxProps } from "@mui/material/Checkbox";
import { FormControlLabel, FormGroup, FormGroupProps } from "@mui/material";

const BpIcon = styled("span")(({ theme }) => ({
  borderRadius: 3,
  width: 20,
  height: 20,
  boxShadow:
    theme.palette.mode === "dark"
      ? "0 0 0 1px rgb(16 22 26 / 40%)"
      : "inset 0 0 0 1px rgba(16,22,26,.2), inset 0 -1px 0 rgba(16,22,26,.1)",
  backgroundColor: theme.palette.mode === "dark" ? "#394b59" : "#f5f8fa",
  backgroundImage:
    theme.palette.mode === "dark"
      ? "linear-gradient(180deg,hsla(0,0%,100%,.05),hsla(0,0%,100%,0))"
      : "linear-gradient(180deg,hsla(0,0%,100%,.8),hsla(0,0%,100%,0))",
  ".Mui-focusVisible &": {
    outline: "2px auto rgba(19,124,189,.6)",
    outlineOffset: 2,
  },
  "input:hover ~ &": {
    backgroundColor: theme.palette.mode === "dark" ? "#30404d" : "#ebf1f5",
  },
  "input:disabled ~ &": {
    boxShadow: "none",
    background:
      theme.palette.mode === "dark"
        ? "rgba(57,75,89,.5)"
        : "rgba(206,217,224,.5)",
  },
}));

// Inspired by blueprintjs
export interface ICheckboxCustomProps {
  label: string;
  onChange?: (e: any) => void;
  defaultChecked?: boolean;
}
export default function CheckboxCustom(props: ICheckboxCustomProps) {
  return (
    <FormGroup sx={{ width: "100%" }}>
      <FormControlLabel
        control={
          <Checkbox
            defaultChecked={props.defaultChecked}
            onChange={(e) => {
              if (props.onChange) props.onChange(e.target.checked);
            }}
            sx={{
              "&:hover": { bgcolor: "transparent" },
              color: "#CDD2D1",
            }}
            disableRipple
            color="primary"
            inputProps={{ "aria-label": "Checkbox demo" }}
          />
        }
        label={<p>{props.label}</p>}
        sx={{
          "& .MuiFormControlLabel-label > p": {
            color: "#55595d",
            fontSize: 14,
            fontWeight: 500,
            transition: "all .3s ease-in-out",
          },
          "& .Mui-checked": {
            "& + .MuiFormControlLabel-label > p": {
              color: "#000000",
            },
          },
        }}
      />
    </FormGroup>
  );
}
