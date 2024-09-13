import CalendaIcon from "@/assets/svgs/calenda.svg";
import PickDateCustom from "@/components/common/pick-two-date";
import { Popover } from "@mui/material";
import * as React from "react";
export interface IPickTimeProps {}

export function PickTimeHistory(props: IPickTimeProps) {
  const [anchorEl, setAnchorEl] = React.useState<HTMLButtonElement | null>(
    null
  );

  const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const open = Boolean(anchorEl);
  const id = open ? "simple-popover" : undefined;
  return (
    <>
      <button
        aria-describedby={id}
        onClick={handleClick}
        className="bg-white p-2 shadow-shadown1 rounded-lg flex items-center justify-center"
      >
        <CalendaIcon />
      </button>

      <Popover
        id={id}
        open={open}
        anchorEl={anchorEl}
        onClose={handleClose}
        anchorOrigin={{
          vertical: "bottom",
          horizontal: "right",
        }}
        transformOrigin={{
          vertical: "top",
          horizontal: "right",
        }}
        slotProps={{
          paper: {
            sx: {
              borderRadius: "16px",
              boxShadow: "0px 1px 10px 0px rgba(34, 34, 34, 0.10)",
              marginTop: "5px",
            },
          },
        }}
      >
        <PickDateCustom
          onclose={function (): void {}}
          handeSubmit={function (
            startDate: Date | null,
            endDate: Date | null
          ): void {
            console.log("startDate: ", startDate);
            console.log("endDate: ", endDate);
          }}
          startDate={new Date()}
          endDate={new Date()}
        />
      </Popover>
    </>
  );
}
