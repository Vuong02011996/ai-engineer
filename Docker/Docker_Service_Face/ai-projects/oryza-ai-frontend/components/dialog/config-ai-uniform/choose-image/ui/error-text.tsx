import { IPerson } from "@/interfaces/identification-profile/person";
import CloseIcon from "@mui/icons-material/Close";
import { InputLabel, Stack, Typography } from "@mui/material";

export interface ErrortextProps {
  error: string;
}

export function Errortext({ error }: ErrortextProps) {
  return (
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
        {error}
      </Typography>
    </Stack>
  );
}
