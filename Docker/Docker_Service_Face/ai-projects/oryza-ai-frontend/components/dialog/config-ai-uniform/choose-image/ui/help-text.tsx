import { Stack } from "@mui/material";

export function Helptext() {
  return (
    <Stack direction="row" spacing="6px" alignItems="center" mt={1}>
      <Stack
        sx={{
          width: "5px",
          height: "5px",
          background: "#E42727",
          borderRadius: "50%",
        }}
      />
      <p className="text-[#808080]  text-xs font-normal ">
        Dung lượng tối đa mỗi hình <span className="font-medium">5MB</span>
      </p>
    </Stack>
  );
}
