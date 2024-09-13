import { SelectModel } from "@/models/select";
import CloseRoundedIcon from "@mui/icons-material/CloseRounded";
import {
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Stack,
  Typography,
} from "@mui/material";
import styles from "./style.module.css";
import CloseIcon from "@mui/icons-material/Close";
import { SxProps } from '@mui/system';

export interface ISelectCustomProps {
  setValue?: (value: any) => void;
  value?: any;
  listSelect: SelectModel[];
  title: string;
  required?: boolean | undefined;
  textError?: string;
  name?: string;
  defaultValue?: string;
  onLoadMore?: () => void;
  disabled?: boolean;
  sx?: SxProps; 
}

export function SelectCustom(props: ISelectCustomProps) {
  const { setValue, value, listSelect, title, textError, disabled } = props;

  return (
    <Stack gap={0.8}>
      {title && (
        <InputLabel sx={{ fontSize: 14, fontWeight: 400, color: "#55595D" }}>
          {props.title}{" "}
          <Typography
            component={"span"}
            sx={{
              color: "#E42727",
              fontSize: 13,
              display: props.required ? "inline-block" : "none",
            }}
          >
            (✶)
          </Typography>
        </InputLabel>
      )}
      <FormControl fullWidth>
        <Select
          onChange={(event: any) => {
            if (setValue) setValue(event.target.value);
          }}
          value={value}
          fullWidth
          name={props.name}
          defaultValue={props.defaultValue}
          size="small"
          placeholder="hehehe"
          disabled={disabled}
          sx={{
            borderRadius: "6px",
            height: "46px",
            "& > fieldset": {
              borderColor: "#E3E5E5",
              borderRadius: "6px",
              "::-webkit-scrollbar-thumb": {
                background: "#78C6E7",
                ":hover": {
                  background: "#78C6E7",
                },
              },
              " ::-webkit-scrollbar": {
                height: "8px",
              },
            },
            ".MuiOutlinedInput-notchedOutline": {
              borderColor: "#E3E5E5",
            },
            "&.Mui-focused .MuiOutlinedInput-notchedOutline": {
              borderColor: "#78C6E7",
              borderWidth: "2px",
              transition: "all .2s ease-in-out",
            },
            "&:hover .MuiOutlinedInput-notchedOutline": {
              borderColor: "#E3E5E5",
            },
            fontSize: "16px",
            fontWeight: 400,
            color: "#323232",
            lineHeight: "20px",
            ":focus": {
              outlineColor: "#E3E5E5",
            },
          }}
          MenuProps={{
            style: {
              width: "100%",
            },
            PaperProps: {
              sx: { maxHeight: 300 },
              onScroll: (e: any) => {
                if (
                  e.currentTarget.scrollHeight - e.currentTarget.scrollTop ===
                  e.currentTarget.clientHeight
                ) {
                  if (props.onLoadMore) props.onLoadMore();
                }
              },
            },
          }}
        >
          {listSelect.map((item: any, index) => (
            <MenuItem value={item?.id} key={index}>
              {item?.name ?? ""}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
      {textError && (
        <Stack
          direction={"row"}
          spacing={"5px"}
          sx={{ alignItems: "center", mt: "4px" }}
        >
          <Stack
            sx={{
              width: "13px",
              height: "13px",
              alignItems: "center",
              justifyContent: "center",
              background: "#E42727",
              borderRadius: "50%",
            }}
          >
            <CloseIcon sx={{ color: "#fff", fontSize: 10, fontWeight: 600 }} />
          </Stack>

          <Typography
            sx={{
              fontSize: 12,
              fontWeight: 400,
              color: "#E42727",
            }}
          >
            {textError}
          </Typography>
        </Stack>
      )}
    </Stack>
  );
}
