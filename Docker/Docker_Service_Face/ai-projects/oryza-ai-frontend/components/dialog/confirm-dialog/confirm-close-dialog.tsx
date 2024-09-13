import CloseRoundedIcon from "@mui/icons-material/CloseRounded";
import {
  CardMedia,
  Stack,
  Typography,
  darken,
  styled,
  useTheme,
} from "@mui/material";
import Dialog from "@mui/material/Dialog";
const CloseBtn = styled(Stack)(({ theme }) => ({
  position: "absolute",
  top: "16px",
  right: "16px",
  ":hover": {
    color: "#55595d",
  },
  ":active": {
    color: darken("#55595d", 0.9),
  },
  color: "#808080",
  transition: "all .3s ease-in-out",
  cursor: "pointer",
}));

const TitleDialog = styled(Typography)(
  () => `
    color: var(--en, #222);
    text-align: center; 
    font-family: Roboto;
    font-size: 22px;
    font-style: normal;
    font-weight: 600;
    line-height: normal;
    margin-bottom: 6px;
  `
);
const SubtitleDialog = styled(Typography)(
  () => `
    color: var(--Xm_Oryza, #55595D);
    text-align: center; 
    font-family: Roboto;
    font-size: 16px;
    font-style: normal;
    font-weight: 400;
    line-height: 20px; /* 125% */
    margin-bottom: 32px;
  `
);

export interface ConfirmCloseDialogProps {
  open: boolean;
  onClose: any;
  submit: () => void;
}

export function ConfirmCloseDialog(props: ConfirmCloseDialogProps) {
  const { onClose, open } = props;
  const theme = useTheme();

  return (
    <Dialog
      onClose={onClose}
      open={open}
      PaperProps={{
        sx: {
          borderRadius: "10px",
          maxWidth: 350,
        },
      }}
      hideBackdrop
    >
      <Stack
        sx={{
          position: "relative",
          padding: { xs: 3, sm: "24px" },
          alignItems: "center",
        }}
      >
        <CloseBtn onClick={onClose}>
          <CloseRoundedIcon />
        </CloseBtn>

        <CardMedia
          component="img"
          src="/icons/cancel-icon.svg"
          alt=""
          sx={{ width: "60px", height: "60px", mb: "24px" }}
        />
        <TitleDialog>Bạn chắc chắn hủy không?</TitleDialog>
        <SubtitleDialog>Sau khi hủy, dữ liệu sẽ không được lưu.</SubtitleDialog>

        <Stack
          sx={{
            justifyContent: "center",
            width: "100%",
          }}
          direction="row"
          spacing={2}
          alignItems="center"
        >
          <button
            onClick={(event) => {
              event.stopPropagation();
              onClose();
            }}
            className="min-w-[100px] shadow-shadown1 bg-white rounded-lg px-[14px] py-2 capitalize text-grayOz font-semibold text-sm hover:bg-white hover:shadow-shadown1"
          >
            Hủy bỏ
          </button>
          <button
            autoFocus
            onClick={(event) => {
              event.stopPropagation();

              props.submit();
            }}
            className="min-w-[100px] shadow-shadown1 bg-red rounded-lg px-[14px] py-2 capitalize text-white font-semibold text-sm hover:bg-redDark outline-none "
          >
            Có
          </button>
        </Stack>
      </Stack>
    </Dialog>
  );
}
