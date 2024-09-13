import { Button, Stack, Typography } from "@mui/material";

export interface IActionCompProps {
  handleClose: any;
  handleSubmit: any;
  dateNumber: number | string;
}

export function ActionComp(props: IActionCompProps) {
  const { handleClose, handleSubmit } = props;
  return (
    <Stack
      direction={"row"}
      justifyContent="space-between"
      mt="auto"
      pt={"12px"}
    >
      <Stack
        sx={{
          justifyContent: { xs: "center", sm: "flex-end" },
        }}
        direction={{ xs: "column", md: "column" }}
        spacing={"5px"}
        alignItems="center"
      >
        <Typography
          sx={{
            color: "#55595D",
            fontSize: 12,
            fontWeight: 400,
          }}
        >
          Đã chọn:
        </Typography>
        {typeof props.dateNumber === "string" ? (
          <Typography
            sx={{
              color: "#55595d",
              fontSize: 14,
              fontWeight: 500,
            }}
          >
            <Typography
              component="span"
              sx={{
                color: "#007dc0",
                mr: "5px",
                fontWeight: 500,
                fontSize: 14,
              }}
            >
              {props.dateNumber}
            </Typography>
          </Typography>
        ) : (
          <Typography
            sx={{
              color: "#55595d",
              fontSize: 14,
              fontWeight: 500,
            }}
          >
            <Typography
              component="span"
              sx={{
                color: "#007dc0",
                mr: "5px",
                fontWeight: 600,
                fontSize: 14,
              }}
            >
              {props.dateNumber}
            </Typography>
            ngày
          </Typography>
        )}
      </Stack>
      <Stack
        sx={{
          justifyContent: { xs: "center", sm: "flex-end" },
        }}
        direction="row"
        spacing={{ xs: 0.5, sm: 1 }}
        alignItems="center"
      >
        <button
          onClick={handleClose}
          className="shadow-shadown1 p-2 rounded-lg min-w-24 bg-white "
        >
          <p className="text-grayOz text-center font-semibold text-[14px]">
            Hủy bỏ
          </p>
        </button>
        <button
          onClick={handleSubmit}
          className="shadow-shadown1 p-2 rounded-lg min-w-24 bg-primary hover:bg-primaryDark transition-all duration-200"
        >
          <p className="text-white text-center font-semibold text-[14px]">
            Áp dụng
          </p>
        </button>
      </Stack>
    </Stack>
  );
}
