import KeyboardArrowUpRoundedIcon from "@mui/icons-material/KeyboardArrowUpRounded";
import {
  InputBase,
  List,
  ListItem,
  ListItemButton,
  Popover,
  Stack,
  Typography,
  alpha,
} from "@mui/material";
import * as React from "react";
import { useRef } from "react";

export interface IHourMinuteProps {
  type: "HOUR" | "MINUTE";
  onChange: (v: string) => void;
  value: string;
  max?: number | null;
  min?: number | null;
}

export function HourMinute(props: IHourMinuteProps) {
  const { type, onChange, value, max, min } = props;
  const MAX_NUMBER = type === "HOUR" ? 24 : 60;

  const [anchorEl, setAnchorEl] = React.useState<HTMLButtonElement | null>(
    null
  );

  const boxRef = useRef<any>(null);
  const handleClick = (event: any) => {
    setAnchorEl(boxRef.current);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const open = Boolean(anchorEl);
  const id = open ? "simple-popover" : undefined;

  function disable(value: number) {
    if (max) {
      return value > max;
    }

    if (min) {
      return value < min;
    }
    return false;
  }

  return (
    <Stack>
      <Typography
        sx={{
          fontSize: 12,
          fontWeight: 400,
          color: "#808080",
        }}
      >
        {type === "HOUR" ? "Giờ" : "Phút"}
      </Typography>
      <Stack
        ref={boxRef}
        sx={{
          width: "50px",
          height: "32px",
          border: "1px solid ",
          display: "flex",
          flexDirection: "row",
          borderRadius: "4px",
          borderColor: open ? "#007dc0" : "#E3E5E5",
          transition: "all .2s",
        }}
      >
        <InputBase
          value={value}
          type="number"
          placeholder="00"
          onChange={(e) => {
            const inputValue = e.target.value;
            if (inputValue.length == 0) {
              if (!disable(0)) {
                onChange("0");
              }
            }
            let number = parseInt(inputValue);

            if (number >= 0 && number < MAX_NUMBER) {
              if (!disable(number)) {
                onChange(number.toString());
              }
            } else if (number >= MAX_NUMBER) {
              if (!disable(number)) {
                onChange((MAX_NUMBER - 1).toString());
              }
            }
          }}
          sx={{
            pl: "8px",
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
            textAlign: "center",
            width: "100%",
            fontSize: 14,
            fontWeight: 400,
            color: "#222",
          }}
          endAdornment={
            <KeyboardArrowUpRoundedIcon
              onClick={handleClick}
              sx={{
                width: { xs: "20px", sm: "24px" },
                height: { xs: "20px", sm: "24px" },
                borderRadius: "4px",
                ":active": {
                  background: "#E3E5E5",
                },
                cursor: "pointer",
                transition: "all .2s",
                color: open ? "#007dc0" : "#55595D",
                rotate: open ? "0deg" : "180deg",
                ":hover": {
                  color: "#007dc0",
                },
              }}
            />
          }
          inputProps={{ maxLength: 2 }}
        />
      </Stack>

      <Popover
        id={id}
        open={open}
        anchorEl={anchorEl}
        onClose={handleClose}
        anchorOrigin={{
          vertical: "bottom",
          horizontal: "left",
        }}
        sx={{
          borderRadius: "3px",
        }}
      >
        <List
          sx={{
            maxHeight: 150,
            overflow: "auto",
            "&::-webkit-scrollbar": {
              width: "2px",
            },
            "&::-webkit-scrollbar-thumb": {
              backgroundColor: "#78C6E7",
              borderRadius: "4px",
            },
            width: "50px",
            borderRadius: "3px",
          }}
        >
          {[...Array(MAX_NUMBER)].map((_, index) => {
            let value = index < 10 ? "0" + index : index;
            return (
              <ListItem disablePadding key={index}>
                <ListItemButton
                  disabled={disable(index)}
                  sx={{
                    alignItems: "center",
                    justifyContent: "center",
                    ":hover": {
                      background: alpha("#dedfed", 0.5),
                    },
                  }}
                  onClick={() => {
                    onChange(value.toString());
                    setAnchorEl(null);
                  }}
                >
                  <Typography
                    sx={{
                      fontSize: 14,
                      fontWeight: 400,
                      color: "#222",
                    }}
                  >
                    {value}
                  </Typography>
                </ListItemButton>
              </ListItem>
            );
          })}
        </List>
      </Popover>
    </Stack>
  );
}
