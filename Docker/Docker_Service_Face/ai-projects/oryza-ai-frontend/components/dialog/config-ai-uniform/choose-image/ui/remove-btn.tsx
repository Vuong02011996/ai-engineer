import CloseRoundedIcon from "@mui/icons-material/CloseRounded";
import { IconButton } from "@mui/material";
export interface IRemoveBtnProps {
  onClick?: () => void;
}

export function RemoveBtn(props: IRemoveBtnProps) {
  const { onClick } = props;
  return (
    <IconButton
      onClick={onClick}
      sx={{
        position: "absolute",
        top: "5px",
        right: "5px",
        cursor: "pointer",
        transition: "all 0.3s ease",
        background: "#ffffff60",
        ":hover": {
          background: "red",
          opacity: 0.5,
          color: "#fff",
        },
        color: "#222",
      }}
      size="small"
    >
      <CloseRoundedIcon sx={{ fontSize: "12px" }} />
    </IconButton>
  );
}
