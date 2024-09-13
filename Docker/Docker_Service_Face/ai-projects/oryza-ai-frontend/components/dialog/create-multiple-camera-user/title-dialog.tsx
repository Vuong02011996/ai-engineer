import CloseRoundedIcon from "@mui/icons-material/CloseRounded";
import { IconButton } from "@mui/material";
import { Processbar } from "./process-bar";
export interface ITitleDialogProps {
  onClose: () => void;
  percent: number;
}

export function TitleDialog(props: ITitleDialogProps) {
  return (
    <div className="px-8 pt-4 bg-grayOz justify-between">
      <div className="flex flex-row justify-between">
        <div>
          <h3 className="text-white font-medium text-lg">
            Thêm camera giám sát cho đối tượng
          </h3>
          <p className="text-white text-xs font-normal">
            Tổng số camera: tất cả
          </p>
        </div>
        <IconButton
          onClick={props.onClose}
          aria-label="delete"
          size="small"
          title="Đóng"
          className="w-[24px] h-[24px] flex"
        >
          <CloseRoundedIcon
            fontSize="inherit"
            sx={{ color: "white", fontSize: 25 }}
          />
        </IconButton>
      </div>
      <div className="mt-4">
        <Processbar percent={props.percent} />
      </div>
    </div>
  );
}
