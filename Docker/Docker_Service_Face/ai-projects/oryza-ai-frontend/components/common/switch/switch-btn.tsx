import * as React from "react";
import { Stack, Switch, SwitchProps, styled } from "@mui/material";

const IOSSwitch = styled((props: SwitchProps) => (
  <Switch focusVisibleClassName=".Mui-focusVisible" disableRipple {...props} />
))(({ theme }) => ({
  width: 50,
  height: 26,
  padding: 0,

  "& .MuiSwitch-switchBase": {
    padding: 0,
    margin: 2,
    transitionDuration: "300ms",
    "&.Mui-checked": {
      transform: "translateX(24px)",
      color: "#fff",
      "& + .MuiSwitch-track": {
        background: "url(/icons/switch-body-active.svg)",
        opacity: 1,
        border: 0,
      },
      "&.Mui-disabled + .MuiSwitch-track": {
        opacity: 0.5,
      },
    },
    "&.Mui-disabled .MuiSwitch-thumb": {
      color:
        theme.palette.mode === "light"
          ? theme.palette.grey[100]
          : theme.palette.grey[600],
    },
    "&.Mui-disabled + .MuiSwitch-track": {
      opacity: theme.palette.mode === "light" ? 0.7 : 0.3,
    },
  },
  "& .MuiSwitch-thumb": {
    boxSizing: "border-box",
    width: 22,
    height: 22,
    background: "  #fff",
    backgroundRepeat: "no-repeat",
    backgroundSize: "65%",
    backgroundPosition: "50% 50%",
    boxShadow: "2px 1px 6px 0px rgba(0, 0, 0, 0.25)",
  },
  "& .MuiSwitch-track": {
    borderRadius: 26 / 2,
    background: "url(/icons/switch-body.svg)",
    opacity: 1,
    transition: "all .3s ease-in-out",
  },
}));

export function SwitchBtn(props: SwitchProps) {
  return <IOSSwitch {...props} />;
}
