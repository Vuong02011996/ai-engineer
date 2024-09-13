// import {LoadingPopup} from "@/components/common/loading/loading-popup";
import TextFieldFormV2 from "@/components/common/text-field/text-field-form-v2";
import {Validator} from "@/utils/validate";
import CloseRoundedIcon from "@mui/icons-material/CloseRounded";
import {Grid, IconButton} from "@mui/material";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogTitle from "@mui/material/DialogTitle";
import Slide from "@mui/material/Slide";
import {TransitionProps} from "@mui/material/transitions";
import * as React from "react";
import {ChooseCompany} from "@/components/input-field/choose-company";
import {ConfirmCloseDialog} from "../confirm-dialog/confirm-close-dialog";
import {ResultEnum} from "@/constants/enum";
import {PickAvatar} from "./pick-avatar";
import {useAuth} from "@/hooks/auth-hook";
import { useEffect, useState } from "react";
import { UserRes } from "@/interfaces/user";
import {formatUser} from "@/libs/format-data";
import { SelectCustom } from "@/components/common/select/select";

const Transition = React.forwardRef(function Transition(
  props: TransitionProps & {
    children: React.ReactElement<any, any>;
  },
  ref: React.Ref<unknown>
) {
  return <Slide direction="up" ref={ref} {...props} />;
});

export interface ISettingRoleDialogProps {
  open: boolean;
  handleClose: () => void;
  submit: (data: any) => Promise<ResultEnum>;
  data?: any;
}

const formInit = {
  username: "",
  email: "",
  password: "",
  company: "",
  is_active: true,
  is_admin: false,
  is_superuser: false,
  avatar: null
};

export function SettingRoleDialog(props: ISettingRoleDialogProps) {
  const {open, handleClose, submit, data} = props;
  const [formErr, setFormErr] = useState<any>({});
  const [formData, setFormData] = useState<any>(formInit);
  const isUpdate = data != null;
  const [loading, setLoading] = useState(false);
  // console.log('data', data)
  // console.log('isUpdate', isUpdate)
  
  const handleChange = (name: string, value: any) => {
    setFormData({ ...formData, [name]: value });
  }

  useEffect(() => {
    if (data) {
      let response: UserRes[] = formatUser([data]);
      setFormData(response[0]);
    }
  }, [data]);
  

  const handleSubmit = async (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => {
    event.preventDefault();
    console.log('formData', formData)

    if (formData.company === "") {
      formData.company = profile?.company.id;
    }
  
    if (isUpdate) {
      for (let key in formData) {
        if (data[key] === formData[key] || formData[key] === null || formData[key] === "") {
          delete formData[key];
        }
      }
      console.log('formData is updated', formData)
    }

    if (formData === null) {
      console.log('Form is empty');
      return;
    }

    if (formData && (!checkValidate())) {
      console.log('Form is invalid');
      return;
    }
    console.log('Form is valid')

    if (formData) {
      setLoading(true);
      const result = await submit(formData);
      setLoading(false);
      if (result === ResultEnum.success) {
        setFormData(formInit);
        props.handleClose();
      } else {
        console.log("Error when submit form");
      }
    }
  }
  const { profile } = useAuth();

  const checkValidate = () => {
    console.log('check validate', formData)
    let hasError = false;
    let error = { ...formErr };
  
    if (isUpdate) {
      if (formData.hasOwnProperty("email")) {
        const email = Validator.checkValidEmail(formData["email"] ?? "");
        error = { ...error, email: email };
      }
    } else {
      if (formData.hasOwnProperty("username")) {
        const username = Validator.checkNotEmpty(formData["username"] ?? "");
        error = { ...error, username: username };
      }
      if (formData.hasOwnProperty("email")) {
        const email = Validator.checkValidEmail(formData["email"] ?? "");
        error = { ...error, email: email };
      }
      if (formData.hasOwnProperty("password")) {
        const password = Validator.checkNotEmpty(formData["password"] ?? "");
        error = { ...error, password: password };
      }
      if (formData.hasOwnProperty("company")) {
        const company = Validator.checkNotEmpty(formData["company"] ?? "");
        error = { ...error, company: company };
      }
    }
  
    if (
      error.username 
      || error.password 
      || error.company
      || error.is_active 
      || error.email
    ) {
      hasError = true;
    }
  
    setFormErr(error);
    console.log(error);
    return !hasError;
  };

  const onClose = () => {
    setFormErr({});
    handleClose();
    setFormData({ ...formInit, avatar: null });
  };

  const [confirmDialog, setConfirmDialog] = useState(false);
  
  return (
    <Dialog
      open={open}
      TransitionComponent={Transition}
      onClose={(event: any) => {
        event.stopPropagation();
        setConfirmDialog(true);
      }}
      aria-describedby="alert-dialog-slide-description"
      PaperProps={{
        sx: {
          borderRadius: "11px",
          boxShadow: "0px 1px 10px 0px rgba(34, 34, 34, 0.10)",
          padding: "16px",
          position: "relative",
          width: "500px",
          overflow: "unset",
        },
        component: "form",
      }}
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
      {/* <LoadingPopup open={loading} /> */}

      <IconButton
        onClick={(event) => {
          event.stopPropagation();
          setConfirmDialog(true);
        }}
        aria-label="delete"
        size="small"
        title="Đóng"
        className="w-[24px] h-[24px] flex top-[16px] right-[16px]"
        sx={{
          position: "absolute",
        }}
      >
        <CloseRoundedIcon fontSize="inherit" />
      </IconButton>

      <DialogTitle className="text-center text-[#1C2A53] text-xl font-medium">
        {isUpdate? `Chỉnh sửa tài khoản: ${data?.username}` : "Tạo mới tài khoản"}
      </DialogTitle>
      <DialogContent sx={{ overflow: "unset" }}>
        <Grid container spacing={2}>
          <Grid item xs={12}>
            <PickAvatar 
              currentAvatar={isUpdate? data?.avatar : null}
              onAvatarChange={(avatar) => {
                handleChange("avatar", avatar);
                console.log('avatar change')
              }}
            />
          </Grid>
          <Grid item xs={6}>
            <TextFieldFormV2
              label="Tên đăng nhập"
              required={data? false : true}
              placeholder="Nhập tên ..."
              name="username"
              disabled={isUpdate}
              defaultValue={data?.username ?? ""}
              textError={formErr?.username ?? ""}
              onChange={(event: any) => {
                const { name, value } = event.target;
                handleChange(name, value);
              }}
            />
          </Grid>
          <Grid item xs={6}>
            <TextFieldFormV2
              label="Email"
              required={data? false : true}
              placeholder="Nhập email..."
              name="email"
              defaultValue={data?.email ?? ""}
              textError={formErr.email}
              onChange={(event: any) => {
                const { name, value } = event.target;
                handleChange(name, value);
              }}
            />
          </Grid>
          <Grid item xs={6}>
            <TextFieldFormV2
              label="Mật khẩu"
              required={!data}
              placeholder="--"
              name="password"
              textError={formErr.password}
              type="password"
              endAdornment={<>icon</>}
              onChange={(event: any) => {
                const { name, value } = event.target;
                handleChange(name, value);
              }}
            />
          </Grid>
          <Grid item xs={6}>
            <SelectCustom
              title="Loại quyền"
              required={data? false : true}
              name="role"
              defaultValue={data?.is_admin ? "ADMIN" : "USER"}
              listSelect={[
                {
                  id: "ADMIN",
                  name: "Quản trị viên",
                },
                {
                  id: "USER",
                  name: "Người dùng",
                },
              ]}
              textError={formErr.role}
              setValue={(value) => {
                console.log('role event', value)
                if (value === "USER") {
                  handleChange("is_superuser", false);
                  handleChange("is_admin", false);
                }
                else if (value === "ADMIN") {
                  handleChange("is_superuser", false);
                  handleChange("is_admin", true);
                }
              }}
            
            />
          </Grid>
          <Grid item xs={6}>
            <ChooseCompany
              name="company"
              defaultValue={isUpdate? data.company.id : (profile?.is_admin ? profile?.company.id : "" )}
              textError={formErr.company}
              disabled={profile?.is_superuser? false : true}
              // value={formData.company}
              setValue={(value) => {
                console.log('form data', formData)
                console.log('data', data)
                console.log('company event', value)
                handleChange("company", value);
              }}
            />
          </Grid>
          <Grid item xs={6}>
            <SelectCustom
              title="Trạng thái tài khoản"
              required={data? false : true}
              name="is_active"
              defaultValue={data ? (data.is_active ? "ACTIVE": "INACTIVE") : "ACTIVE"}
              listSelect={[
                {
                  id: "ACTIVE",
                  name: "Kích hoạt",
                },
                {
                  id: "INACTIVE",
                  name: "Chưa kích hoạt",
                },
              ]}
              textError={formErr.is_active}
              setValue={(value) => {
                console.log('is_active event', value)
                if (value === "ACTIVE") {
                  handleChange("is_active", true);
                }
                else if (value === "INACTIVE") {
                  handleChange("is_active", false);
                }
              }}
            />
          </Grid>
        </Grid>
      </DialogContent>
      <DialogActions sx={{ justifyContent: "center", gap: "16px" }}>
        <button
          type="button"
          onClick={() => setConfirmDialog(true)}
          className="min-w-[100px] shadow-shadown1 bg-white rounded-lg px-[14px] py-2 capitalize text-grayOz font-semibold text-sm hover:bg-white hover:shadow-shadown1"
        >
          Hủy bỏ
        </button>
        <button
          onClick={handleSubmit}
          disabled={loading}
          className="min-w-[100px] shadow-shadown1 bg-primary rounded-lg px-[14px] py-2 capitalize text-white font-semibold text-sm hover:bg-primaryDark"
        >
          {data ? "Xác nhận" : "Tạo mới"}
        </button>
      </DialogActions>
    </Dialog>
  );
}
