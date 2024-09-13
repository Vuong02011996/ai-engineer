import CheckIcon from "@mui/icons-material/Check";
import CloseIcon from "@mui/icons-material/Close";
import {
  InputLabel,
  Stack,
  SxProps,
  TextField,
  TextFieldProps,
  TextFieldVariants,
  Theme,
  Typography,
  alpha,
  darken,
  useTheme,
} from "@mui/material";
import * as React from "react";
import { useState } from "react";
import Icon from "../../icon";

export interface ITextFieldFormV3Props {
  value?: unknown;
  onChange?:
    | React.ChangeEventHandler<HTMLInputElement | HTMLTextAreaElement>
    | undefined;
  label?: string;
  type?: React.HTMLInputTypeAttribute | undefined;
  fullWidth?: boolean | undefined;
  size?: "small" | "medium" | undefined;
  variant?: "outlined" | "standard" | undefined;
  placeholder?: string;
  tabIndex?: number;
  textError?: string | null;
  color?: string;
  required?: boolean;
  row?: number;
  multiline?: boolean;
  name?: string;
  autoComplete?: string;
  disabled?: boolean;
  onBlur?:
    | React.FocusEventHandler<HTMLInputElement | HTMLTextAreaElement>
    | undefined;
  height?: string;
  helpText?: string;
  endAdornment?: React.JSX.Element;
  startAdornment?: React.JSX.Element;
  borderColor?: string;
  clearIcon?: boolean;
  backgroundColor?: string;
  disableIconError?: boolean;
  sx?: SxProps<Theme>;
  defaultValue?: any;
  autofocus?: boolean;
}

export default function TextFieldFormV3(props: ITextFieldFormV3Props) {
  const {
    value,
    onChange,
    label: lable,
    textError,
    required,
    name,
    disabled,
    helpText,
    backgroundColor,
    disableIconError,
    sx,
  } = props;
  const type = props.type ?? "text";
  const fullWidth = props.fullWidth ?? true;
  const size = props.size ?? "small";
  const variant = props.variant ?? "outlined";
  const color = props.color ? props.color : textError ? "#E42727" : "#E3E5E5";
  const borderColor = props.textError
    ? "#E42727"
    : props.borderColor
    ? props.borderColor
    : "#78C6E7";
  const theme = useTheme();

  const isPassword = type === "password";
  const [showPw, setShowPw] = useState(false);
  const togglePassword = () => {
    setShowPw(!showPw);
  };

  function endAdornment() {
    if (props.clearIcon && value != "") {
      return (
        <Stack
          onClick={() => {
            let event: any = { target: { value: "", name: name } };
            onChange && onChange(event);
          }}
          sx={{
            width: "20px",
            height: "20px",
            borderRadius: "50%",
            background: "#AFAFAF",
            cursor: "pointer",
            ":hover": {
              background: alpha("#AFAFAF", 0.8),
            },
            ":active": {
              background: darken("#AFAFAF", 0.2),
            },
          }}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 20 20"
            fill="none"
          >
            <path
              d="M6.24996 5.00004C5.90479 4.65486 5.34514 4.65486 4.99996 5.00004C4.65478 5.34522 4.65478 5.90486 4.99996 6.25004L8.74996 10L5 13.75C4.65482 14.0952 4.65482 14.6548 5 15C5.34518 15.3452 5.90482 15.3452 6.25 15L9.99996 11.25L13.75 15C14.0951 15.3452 14.6548 15.3452 15 15C15.3451 14.6549 15.3451 14.0952 15 13.75L11.25 10L15 6.25C15.3452 5.90482 15.3452 5.34517 15 5C14.6548 4.65482 14.0952 4.65482 13.75 5L9.99996 8.75004L6.24996 5.00004Z"
              fill="white"
            />
          </svg>
        </Stack>
      );
    }

    if (isPassword) {
      return (
        <div className="cursor-pointer" onClick={togglePassword}>
          <Icon name={!showPw ? "eye-off" : "eye-on"} />
        </div>
      );
    }

    return props.endAdornment;
  }

  return (
    <Stack sx={sx ? { ...sx, position: "relative" } : { position: "relative" }}>
      {lable && (
        <InputLabel
          htmlFor={name}
          sx={{ fontSize: 14, fontWeight: 400, color: "#55595D", mb: "6px" }}
        >
          {lable}{" "}
          <Typography
            component={"span"}
            sx={{
              color: "#E42727",
              fontSize: 13,
              display: required ? "inline-block" : "none",
            }}
          >
            (✶)
          </Typography>
        </InputLabel>
      )}
      <Stack sx={{ position: "relative" }}>
        <TextField
          name={name}
          value={value}
          onChange={onChange}
          margin="dense"
          autoFocus={props.autofocus}
          id={`${name}-id`}
          type={showPw ? "text" : type}
          fullWidth={fullWidth}
          size={size}
          variant={variant}
          autoComplete={props.autoComplete ?? "off"}
          placeholder={props.placeholder}
          rows={props.row ?? 1}
          multiline={props.multiline ?? false}
          disabled={disabled}
          onBlur={props.onBlur}
          aria-required="true"
          defaultValue={props.defaultValue}
          sx={{
            backgroundColor: backgroundColor,
            borderRadius: "6px",
            "& .MuiOutlinedInput-root:hover": {
              "& > fieldset": {
                borderColor: color,
                transition: "all 0.3s",
              },
            },
            "& .MuiOutlinedInput-root": {
              "& > fieldset": {
                borderColor: color,
                transition: "all 0.3s",
                borderRadius: "6px",
              },
              "&.Mui-focused fieldset": {
                borderColor: borderColor,
                borderWidth: "2px",
                transition: "all .2s ease-in-out",
              },
            },
            "& label.Mui-focused": {
              color: color,
            },
            marginTop: "0px",
            transition: "all 0.3s",
            "& input[type=number]": {
              MozAppearance: "textfield",
            },
            "& input[type=number]::-webkit-outer-spin-button": {
              WebkitAppearance: "none",
              margin: 0,
            },
            "& input[type=number]::-webkit-inner-spin-button": {
              WebkitAppearance: "none",
              margin: 0,
            },
            margin: 0,
            padding: 0,
          }}
          InputProps={{
            endAdornment: endAdornment(),
            startAdornment: props.startAdornment,
          }}
          inputProps={{
            tabIndex: props.tabIndex,
            style: {
              fontSize: "16px",
              fontWeight: 400,
              color: "#323232",
              padding: !props.row ? "13px 16px" : undefined,
              lineHeight: !props.row ? "20px" : undefined,
              height: props.height
                ? props.height
                : !props.row
                ? "20px"
                : undefined,
            },
          }}
        />
        {textError && (
          <Stack
            direction={"row"}
            spacing={"5px"}
            sx={{
              alignItems: "center",
              mt: "4px",
              position: "absolute",
              top: "100%",
              left: 0,
            }}
          >
            {typeof disableIconError === "boolean" && disableIconError ? (
              <></>
            ) : (
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
                <CloseIcon
                  sx={{ color: "#fff", fontSize: 10, fontWeight: 600 }}
                />
              </Stack>
            )}
  
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
      {helpText && (
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
              background: "#55595d",
              borderRadius: "50%",
            }}
          >
            <CheckIcon sx={{ color: "#fff", fontSize: 10, fontWeight: 600 }} />
          </Stack>
          <Typography
            sx={{
              fontSize: 12,
              fontWeight: 400,
              color: "#55595d",
            }}
          >
            {helpText}
          </Typography>
        </Stack>
      )}
    </Stack>
  );
}
