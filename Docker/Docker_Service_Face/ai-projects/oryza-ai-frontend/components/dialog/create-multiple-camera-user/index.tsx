import { LoadingPopup } from "@/components/common/loading/loading-popup";
import TextFieldFormV2 from "@/components/common/text-field/text-field-form-v2";
import { ChooseGender } from "@/components/input-field/choose-gender";
import { ChooseImage } from "@/components/input-field/choose-image";
import { ResultEnum } from "@/constants/enum";
import { useAuth } from "@/hooks/auth-hook";
import { IPerson } from "@/interfaces/identification-profile/person";
import { Validator } from "@/utils/validate";
import CloseRoundedIcon from "@mui/icons-material/CloseRounded";
import { Grid, IconButton, ListItemText } from "@mui/material";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogTitle from "@mui/material/DialogTitle";
import Slide from "@mui/material/Slide";
import { TransitionProps } from "@mui/material/transitions";
import * as React from "react";
import { useCallback, useEffect, useState } from "react";
import { ConfirmCloseDialog } from "../confirm-dialog/confirm-close-dialog";
import { Processbar } from "./process-bar";
import { TitleDialog } from "./title-dialog";
import Scrollbar from "@/components/common/scrollbar";
import { headSlugData } from "@/data/identification-profile";
import { TableHead } from "@/components/table/table-head";
import { EmptyData, Loading } from "@/components/common";
import { UserSlugTableItem } from "@/containers/identification-profile/user/table-slug-item";
import { ICameraAI } from "@/interfaces/identification-profile/camera-ai";
import { useAppSelector } from "@/hooks/useReudx";

const Transition = React.forwardRef(function Transition(
  props: TransitionProps & {
    children: React.ReactElement<any, any>;
  },
  ref: React.Ref<unknown>
) {
  return <Slide direction="up" ref={ref} {...props} />;
});

export interface ICreateMultipleCameraPersonProps {
  open: boolean;
  handleClose: () => void;
  data?: ICameraAI[];
  listIdCamera: string[];
  setListIdCamera: React.Dispatch<React.SetStateAction<string[]>>;
  reload: any;
  setData: React.Dispatch<React.SetStateAction<ICameraAI[]>>;
  onCreate: () => void;
  loading: number;
  errorCount: number;
}

export function CreateMultipleCameraPerson(
  props: ICreateMultipleCameraPersonProps
) {
  const { data, listIdCamera, errorCount } = props;
  const { open, handleClose } = props;
  const [confirmDialog, setConfirmDialog] = useState(false);

  const onClose = () => {
    handleClose();
  };

  return (
    <Dialog
      open={open}
      TransitionComponent={Transition}
      onClose={() => setConfirmDialog(true)}
      aria-describedby="alert-dialog-slide-description"
      PaperProps={{
        sx: {
          borderRadius: "11px",
          boxShadow: "0px 1px 10px 0px rgba(34, 34, 34, 0.10)",
          position: "relative",
        },
        component: "form",
        onSubmit: async (event: React.FormEvent<HTMLFormElement>) => {
          event.preventDefault();
          let formData = new FormData(event.currentTarget);

          const formJson = Object.fromEntries(formData.entries());
          console.log("lformJson", formJson);
        },
      }}
      fullWidth
      maxWidth="lg"
    >
      <ConfirmCloseDialog
        open={confirmDialog}
        onClose={function (event: any): void {
          setConfirmDialog(false);
        }}
        submit={function (): void {
          setConfirmDialog(false);
          onClose();
        }}
      />

      <TitleDialog
        onClose={() => setConfirmDialog(true)}
        percent={props.loading}
      />
      <div className="h-[300px]">
        <div className="h-full overflow-auto  ">
          <Scrollbar>
            <TableHead dataHead={headSlugData} />

            {false ? (
              <>
                <Loading />
              </>
            ) : !data || data.length === 0 ? (
              <EmptyData />
            ) : (
              data.map((item: any, index) => {
                return (
                  <UserSlugTableItem
                    key={item.id}
                    data={item}
                    index={index + 1}
                    isOn={listIdCamera.includes(item.id)}
                    reload={props.reload}
                    disablePadding
                  />
                );
              })
            )}
          </Scrollbar>
        </div>
      </div>

      {errorCount > 0 ? (
        <div className="flex flex-row justify-between px-8 py-3 border-t-2 border-[#F8F8F8] h-[60px] items-center ">
          <p className="text-xs font-normal text-grayOz ">
            Số camera bị lỗi:{" "}
            <span className="text-[#E42727] font-medium">{errorCount} </span>
          </p>
          <button
            onClick={props.onCreate}
            className="space-x-2 min-w-[100px] shadow-shadown1 bg-primary rounded-lg px-[14px] py-2 capitalize  hover:bg-primaryDark flex flex-row "
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              viewBox="0 0 16 16"
              fill="none"
            >
              <rect width="16" height="16" rx="4" fill="white" />
              <path
                d="M12.8546 7.59048L11.3614 9.27049C11.2378 9.40957 11.0603 9.48133 10.8815 9.48133C10.7402 9.48133 10.598 9.43646 10.4811 9.34455L8.69462 7.94042C8.42976 7.73224 8.3945 7.36157 8.61587 7.1125C8.83724 6.86344 9.23139 6.83027 9.49624 7.03845L10.2288 7.61421C10.0281 6.23866 8.77042 5.1755 7.25345 5.1755C5.59734 5.17551 4.25 6.44257 4.25 8C4.25 9.55743 5.59734 10.8245 7.25345 10.8245C7.59862 10.8245 7.87845 11.0876 7.87845 11.4122C7.87845 11.7368 7.59862 12 7.25345 12C6.11732 12 5.04918 11.5839 4.24582 10.8284C3.44244 10.0729 3 9.06843 3 8C3 6.93157 3.44244 5.92707 4.24582 5.17157C5.04918 4.41608 6.11732 4 7.25345 4C8.38958 4 9.45772 4.41608 10.2611 5.17157C10.8962 5.7688 11.3055 6.52172 11.4492 7.33875L11.8954 6.83661C12.1168 6.58755 12.511 6.55441 12.7758 6.76255C13.0406 6.97075 13.0759 7.34142 12.8546 7.59048Z"
                fill="#007DC0"
              />
            </svg>
            <p className=" text-sm text-white font-medium">Thử lại</p>
          </button>
        </div>
      ) : (
        <div className="h-[60px] border-t-2 border-[#F8F8F8] "></div>
      )}
    </Dialog>
  );
}
