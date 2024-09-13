import { Stack, Typography, alpha, darken } from "@mui/material";
import Image from "next/image";

interface IDialogConfirmDelete {
  close: () => void;
  action: () => void;
  image: string;
  title: string;
  description: string;
  width?: string;
  height?: string;
}

export const DialogConfirm = (props: IDialogConfirmDelete) => {
  const { action, close, description, image, title, height, width } = props;

  return (
    <Stack
      sx={{
        position: "fixed",
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        zIndex: 2000000000,
      }}
      justifyContent="center"
      alignItems="center"
    >
      <Stack
        sx={{
          position: "absolute",
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: alpha(darken("#070C27", 0.5), 0.4),
          zIndex: 2,
        }}
        onClick={(event) => {
          event.stopPropagation();
          close();
        }}
      />

      <Stack
        sx={{
          backgroundColor: "#FFF",
          borderRadius: "11px",
          padding: "24px",
          zIndex: 3,
          width: { xs: "fit-content", sm: width ? width : "unset" },
          height: { xs: "fit-content", sm: height ? height : "unset" },
          position: "relative",
        }}
        alignItems="center"
      >
        <Stack
          sx={{
            borderRadius: "4px",
            width: "24px",
            height: "24px",
            position: "absolute",
            top: "24px",
            right: "24px",
            cursor: "pointer",
            transition: "all ease .3s",
            "&:hover ": {
              backgroundColor: "#D0D0D0",
            },
          }}
          justifyContent="center"
          alignItems="center"
          onClick={(event) => {
            event.stopPropagation();
            close();
          }}
        >
          <Image src="/icons/x-gray.svg" width={12} height={12} alt="x-gray" />
        </Stack>

        <Image src={image} width={60} height={60} alt="photo" />

        <Stack
          alignItems="center"
          sx={{
            marginBottom: "32px",
            gap: "6px",
            marginTop: "24px",
          }}
        >
          <Typography
            sx={{
              color: "#222",
              fontSize: { xs: "16px", sm: "22px" },
              fontStyle: "normal",
              fontWeight: 600,
              lineHeight: "normal",
            }}
          >
            {title}
          </Typography>
          <Typography
            sx={{
              color: "#55595D",
              fontSize: { xs: "14px", sm: "18px" },
              fontStyle: "normal",
              fontWeight: 400,
              lineHeight: "normal",
            }}
          >
            {description}
          </Typography>
        </Stack>

        <Stack direction="row" sx={{ gap: "16px" }}>
          <button
            onClick={(event) => {
              event.stopPropagation();
              close();
            }}
            className="min-w-[100px] shadow-shadown1 bg-white rounded-lg px-[14px] py-2 capitalize text-grayOz font-semibold text-sm hover:bg-white hover:shadow-shadown1"
          >
            Hủy bỏ
          </button>
          <button
            autoFocus
            onClick={(event) => {
              event.stopPropagation();
              action();
              close();
            }}
            className="min-w-[100px] shadow-shadown1 bg-red rounded-lg px-[14px] py-2 capitalize text-white font-semibold text-sm hover:bg-redDark focus:outline-none "
          >
            Có
          </button>
        </Stack>
      </Stack>
    </Stack>
  );
};
