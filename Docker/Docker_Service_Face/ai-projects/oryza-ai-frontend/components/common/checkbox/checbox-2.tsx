import Checkbox from "@mui/material/Checkbox";
import { pink } from "@mui/material/colors";

// Inspired by blueprintjs
export interface ICheckboxCustomProps {
  onChange?: (e: any) => void;
  defaultChecked?: boolean;
  checked?: boolean;
}
export default function CheckboxCustom2(props: ICheckboxCustomProps) {
  return (
    <Checkbox
      checked={props.checked}
      defaultChecked={props.defaultChecked}
      onChange={(e) => {
        if (props.onChange) props.onChange(e.target.checked);
      }}
      sx={{
        "&:hover": { bgcolor: "transparent" },
        color: "#CDD2D1",
        "&.Mui-checked": {
          color: "#007dc0",
        },
      }}
      disableRipple
      color="primary"
      inputProps={{ "aria-label": "Checkbox demo" }}
    />
  );
}
