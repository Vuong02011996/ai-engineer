import { cameraApi } from "@/api-client/camera";
import { geoApi } from "@/api-client/geo-unit";
import TextFieldFormV3 from "@/components/common/text-field/text-field-form-v3";
import { ChooseCameraBrand } from "@/components/input-field/choose-camera-brand";
import { CameraRes } from "@/interfaces/camera";
import { formatCameraData } from "@/libs/camera";
import { Validator } from "@/utils";
import CloseRoundedIcon from "@mui/icons-material/CloseRounded";
import { Grid, IconButton, Button, Typography } from "@mui/material";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogTitle from "@mui/material/DialogTitle";
import Slide from "@mui/material/Slide";
import { TransitionProps } from "@mui/material/transitions";
import * as React from "react";
import { useEffect, useState } from "react";
import { ConfirmCloseDialog } from "../confirm-dialog/confirm-close-dialog";
import { ChooseTypeCamera } from "../create-service/choose-type";
import { ChooseTypeServiceMultiple } from "./choose-type-serivce";
import { ResultEnum } from "@/constants/enum";
import { LoadingPopup } from "@/components/common/loading/loading-popup";
import { enqueueSnackbar } from "notistack";
import { ChooseGeoUnit } from "@/components/input-field/choose-camera-address";
import { ChooseCameraType } from "@/components/input-field/choose-camera-type";

const Transition = React.forwardRef(function Transition(
  props: TransitionProps & {
    children: React.ReactElement<any, any>;
  },
  ref: React.Ref<unknown>
) {
  return <Slide direction="up" ref={ref} {...props} />;
});

const formInit = {
  name: "",
  ip_address: "",
  port: "",
  username: "",
  password: "",
  rtsp: "",
  company_id: "",
  is_ai: "",
  brand_camera_id: "",
  type_service_ids: [],
  ward_id: "",
  address: "",
  coordinate: "",
  coordinate_left: "",
  coordinate_right: "",
  camera_type: "",
};

export interface ICreateCameraDialogProps {
  open: boolean;
  handleClose: () => void;
  submit: (formData: any) => Promise<ResultEnum>;
  camera?: CameraRes;
}

export function CreateCameraDialog(props: ICreateCameraDialogProps) {
  const { open, handleClose, submit, camera } = props;
  const [loading, setLoading] = useState(false);
  const [formErr, setFormErr] = useState<any>({});
  const [formData, setFormData] = useState<any>(formInit);

  const handleChange = (name: string, value: string | string[]) => {
    setFormData({ ...formData, [name]: value });
  };

  const [provinceId, setProvinceId] = useState('');
  const [districtId, setDistrictId] = useState('');
  const [wardId, setWardId] = useState('');
  
  const handleProvinceChange = (value: string) => {
    setProvinceId(value);
    setDistrictId(''); // Reset district
    // setWardId(''); // Reset ward
    setFormData({ ...formData, ward_id: '' });
  };

  const handleDistrictChange = (value: string) => {
    setDistrictId(value);
    setWardId(''); // Reset ward
  };

  const handleWardChange = (value: string) => {
    // console.log('Ward:', value);
    setWardId(value);
  };

  const getForm = React.useCallback(async () => {
    if (camera) {
      let response: CameraRes[] = formatCameraData([camera]);
      let type_service_ids = response[0].is_ai
        ? await getCameraTypeMapping(camera.id)
        : [];
      let form = {
        ...response[0],
        is_ai: response[0].is_ai ? "AI_CAMERA" : "AI_SERVICE",
        brand_camera_id: response[0]?.brand_camera,
        type_service_ids: type_service_ids,
        address: response[0]?.other_info?.address ?? "",
        coordinate: response[0]?.other_info?.coordinate ?? "",
        coordinate_left: response[0]?.other_info?.coordinate_left ?? "",
        coordinate_right: response[0]?.other_info?.coordinate_right ?? "",
        ward_id: response[0]?.ward_id ?? "",
        camera_type: response[0]?.other_info?.camera_type ?? "",
      };
      setFormData(form);
      try {
        const rs = await geoApi.getById(form.ward_id);
        if (rs.status == 200) {
          const data = rs.data;
          setProvinceId(data?.province_id);
          setDistrictId(data?.district_id);
        } else {
          console.error('Error fetching ward:', rs);
        }
      } catch (error) {
        console.error('Error fetching ward:', error);
      }
    }
  }, [camera]);

  useEffect(() => {
    getForm();
  }, [getForm]);

  async function getCameraTypeMapping(cameraId: string) {
    try {
      let { data } = await cameraApi.cameraTypeMapping(cameraId);

      return data;
    } catch (error) {
      return [];
    }
  }

  const handleGenerateRTSP = async () => {
    if (!checkValidateGenerateRTSP()) return;
    let payload = {
      address: formData.ip_address,
      port: formData.port,
      username: formData.username,
      password: formData.password,
    };
    setLoading(true);
    try {
      if (formData.rtsp !== "") {
        enqueueSnackbar("Camera đã có RTSP. Vui lòng xóa đi nếu muốn tạo RTSP mới", { variant: "error" });
        return;
      }
      let response = await cameraApi.generateRtsp(payload);
      if (response.status === 201) {
        setFormData({ ...formData, rtsp: response.data.data });
      } else {
        // Handle non-success status codes
        enqueueSnackbar("Tạo RTSP không thành công", { variant: "error" });
      }
    } catch (error) {
      // Handle errors
      console.error('Error generating RTSP:', error);
      enqueueSnackbar("Tạo RTSP không thành công", { variant: "error" });
    } finally {
      setLoading(false);
    }
  }

  const handleSubmit = async (event: any) => {
    event.stopPropagation();
    if (!checkValidate()) return;
    let payload = {
      ...formData,
      is_ai: formData["is_ai"] === "AI_CAMERA",
      ward_id: wardId,  
      other_info: {
        ...formData.other_info, 
        address: formData.address,
        coordinate: formData.coordinate,
        coordinate_left: formData.coordinate_left,
        coordinate_right: formData.coordinate_right,
        camera_type: formData.camera_type,
      },
    };
    setLoading(true);
    console.log('Payload:', payload);
    let result = await submit(payload);
    if (result === ResultEnum.success) {
      setFormData(formInit);
      setProvinceId('');
      setDistrictId('');
      props.handleClose();
    }
    setLoading(false);
  };

  const checkValidateGenerateRTSP = () => {
    let { ip_address, username, password, port } = formData;
    const error = {
      ...formErr,
      ip_address: Validator.checkNotEmpty(ip_address ?? ""),
      username: Validator.checkNotEmpty(username ?? ""),
      password: Validator.checkNotEmpty(password ?? ""),
      port: Validator.checkNumberString(port.toString()),
    };
  
    const hasError = Object.values(error).some((err) => err !== null);
    setFormErr(error);
    return !hasError;
  };
  
  const checkValidate = () => {
    const { 
      name, ip_address, username, password, rtsp, port, brand_camera_id, 
      coordinate, coordinate_left, coordinate_right
    } = formData;
    console.log('Form data:', formData);
    const MIN = 2, MAX = 150;
    const error = {
      ...formErr,
      name: Validator.checkNotEmpty(name ?? "", MIN, MAX),
      ip_address: Validator.checkNotEmpty(ip_address ?? ""),
      username: Validator.checkNotEmpty(username ?? ""),
      password: Validator.checkNotEmpty(password ?? ""),
      rtsp: Validator.validateRTSPUrl(rtsp ?? ""),
      port: Validator.checkNumberString(port.toString()),
      brand_camera_id: Validator.checkNotEmpty(brand_camera_id ?? ""),
      coordinate: Validator.checkCoordinate(coordinate ?? ""),
      coordinate_left: Validator.checkCoordinate(coordinate_left ?? ""),
      coordinate_right: Validator.checkCoordinate(coordinate_right ?? "") || Validator.checkDifferent(coordinate_left, coordinate_right, "Hai tọa độ"),
    };
    console.log('Error:', error);
    const hasError = Object.values(error).some((err) => err !== null);
    setFormErr(error);
    return !hasError;
  };

  const onClose = () => {
    handleClose();
    setFormErr({});
    setFormData(formInit);
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
      fullWidth
      maxWidth="xs"
      PaperProps={{
        sx: {
          borderRadius: "11px",
          boxShadow: "0px 1px 10px 0px rgba(34, 34, 34, 0.10)",
          padding: "16px",
          position: "relative",
          overflow: "unset",
        },
      }}
    >
      <LoadingPopup open={loading} />
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

      {/* close btn */}
      <IconButton
        onClick={(event: any) => {
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

      {/*  */}
      {formData["is_ai"] === "AI_CAMERA" && (
        <ChooseTypeServiceMultiple
          onChange={function (value: string[]): void {
            handleChange("type_service_ids", value);
          }}
          value={formData["type_service_ids"] ?? []}
        />
      )}

      <DialogTitle className="text-center text-[#1C2A53] text-xl font-medium">
        {camera ? "Chỉnh sửa camera" : "Tạo mới camera"}
      </DialogTitle>
      <DialogContent sx={{ overflow: "unset", maxHeight: '500px', overflowY: 'auto' }}>
        <Grid container spacing={2}>
          <Grid item xs={12}>
            <Typography className="text-left text-[#1C2A53] text-xl font-medium">Thông tin Camera</Typography>
          </Grid>
          <Grid item xs={12}>
            <ChooseTypeCamera
              defaultValue={formData.is_ai}
              value={formData.is_ai || "AI_SERVICE"}
              onChange={(e) => {
                handleChange("is_ai", e);
              }}
            />
          </Grid>
          <Grid item xs={12} sx={{ marginBottom: '12px' }}>
            <TextFieldFormV3
              label="Tên camera"
              required
              placeholder="Nhập tên ..."
              name="name"
              onChange={(event: any) => {
                const { name, value } = event.target;
                handleChange(name, value);
              }}
              value={formData["name"]}
              textError={formErr.name}
            />
          </Grid>
          <Grid item xs={12} sx={{ marginBottom: '12px' }}>
            <ChooseCameraBrand
              label={"Chọn hãng camera"}
              name={"brand_camera_id"}
              onChange={(value) => {
                handleChange("brand_camera_id", value);
              }}
              value={formData["brand_camera_id"]}
              textError={formErr.brand_camera_id}
            />
          </Grid>
          <Grid item xs={7} sx={{ marginBottom: '12px' }}>
            <TextFieldFormV3
              label="Địa chỉ IP"
              required
              placeholder="--"
              name="ip_address"
              onChange={(event: any) => {
                const { name, value } = event.target;
                handleChange(name, value);
              }}
              value={formData["ip_address"]}
              textError={formErr.ip_address}
            />
          </Grid>
          <Grid item xs={5} sx={{ marginBottom: '12px' }}>
            <TextFieldFormV3
              label="Port"
              type="number"
              name="port"
              placeholder="80"
              onChange={(event: any) => {
                const { name, value } = event.target;
                handleChange(name, value);
              }}
              value={formData["port"]}
              textError={formErr.port}
              defaultValue={80}
            />
          </Grid>
          <Grid item xs={7} sx={{ marginBottom: '12px' }}>
            <TextFieldFormV3
              label="Tên đăng nhập"
              required
              placeholder="--"
              name="username"
              onChange={(event: any) => {
                const { name, value } = event.target;
                handleChange(name, value);
              }}
              value={formData["username"]}
              textError={formErr.username}
            />
          </Grid>
          <Grid item xs={5} sx={{ marginBottom: '12px' }}>
            <TextFieldFormV3
              label="Mật khẩu"
              required
              placeholder="--"
              name="password"
              onChange={(event: any) => {
                const { name, value } = event.target;
                handleChange(name, value);
              }}
              value={formData["password"]}
              textError={formErr.password}
              type="password"
              endAdornment={<>icon</>}
            />
          </Grid>
          <Grid container item xs={12} alignItems="center" spacing={2}>
            <Grid item xs={8} sx={{ marginBottom: '12px' }}>
              <TextFieldFormV3
                label="Luồng RTSP"
                required
                name="rtsp"
                placeholder="rtsp://..."
                onChange={(event: any) => {
                  const { name, value } = event.target;
                  handleChange(name, value);
                }}
                value={formData["rtsp"]}
                textError={formErr.rtsp}
              />
            </Grid>
            <Grid item xs={4} sx={{ marginBottom: '12px' }}>
              <Button
                variant="outlined"
                fullWidth
                style={{ textTransform: 'none', height: '46px', marginTop: '27px', fontSize: '14px', lineHeight: '1.4' }}
                onClick={handleGenerateRTSP}
              >
                Tạo RTSP tự động
              </Button>
            </Grid>
            <Grid item xs={12} sx={{ marginBottom: '12px' }}>
              <ChooseCameraType
                label="Loại camera"
                name="camera_type"
                value={formData.camera_type}
                onChange={(value) => {
                  handleChange("camera_type", value);
                }}
                required={false}
              />
            </Grid> 
              {/* Camera Address Section */}
            <Grid item xs={12}>
              <Typography className="text-left text-[#1C2A53] text-xl font-medium">Địa chỉ Camera</Typography>
            </Grid>
            <Grid item xs={12}>
              <ChooseGeoUnit
                  name="province_id"
                  label="1. Chọn tỉnh/thành phố"
                  value={provinceId}
                  onChange={handleProvinceChange}
                  parentId={null}
                  type="province"
                  required={false}
                />
            </Grid>
            <Grid item xs={12}>
              <ChooseGeoUnit
                name="district_id"
                label="2. Chọn quận/huyện"
                value={districtId}
                onChange={handleDistrictChange}
                parentId={provinceId}
                type="district"
                required={false}
                />
            </Grid>
            <Grid item xs={12}>
              <ChooseGeoUnit
                name="ward_id"
                label="3. Chọn phường/xã"
                value={formData.ward_id}
                onChange={handleWardChange}
                parentId={districtId} // Use districtId as parentId
                type="ward"
                required={false}
              />
            </Grid>
            <Grid item xs={12}>
              <TextFieldFormV3
                label="Địa chỉ chi tiết"
                placeholder="--"
                name="address"
                onChange={(event: any) => {
                  const { name, value } = event.target;
                  handleChange(name, value);
                }}
                value={formData["address"]}
                textError={formErr.address}
                required={false}
              />
            </Grid>
            <Grid item xs={12} sx={{ marginBottom: '12px' }}>
              <TextFieldFormV3
                label="Tọa độ camera"
                placeholder="kinh độ, vĩ độ. VD: '10.80349,106.72092'"
                name="coordinate"
                onChange={(event: any) => {
                  const { name, value } = event.target;
                  handleChange(name, value);
                }}
                value={formData["coordinate"]}
                textError={formErr.coordinate}
                required={false}
              />
            </Grid>
            <Grid item xs={6} sx={{ marginBottom: '12px' }}>
              <TextFieldFormV3
                label="Tọa độ nhìn trái"
                placeholder="kinh độ, vĩ độ"
                name="coordinate_left"
                onChange={(event: any) => {
                  const { name, value } = event.target;
                  handleChange(name, value);
                }}
                value={formData["coordinate_left"]}
                textError={formErr.coordinate_left}
                required={false}
              />
            </Grid>
            <Grid item xs={6} sx={{ marginBottom: '12px' }}>
              <TextFieldFormV3
                label="Tọa độ nhìn phải"
                placeholder="kinh độ, vĩ độ"
                name="coordinate_right"
                onChange={(event: any) => {
                  const { name, value } = event.target;
                  handleChange(name, value);
                }}
                value={formData["coordinate_right"]}
                textError={formErr.coordinate_right}
                required={false}
              />
            </Grid>
          </Grid>
        </Grid>
      </DialogContent>
      <DialogActions sx={{ justifyContent: "center", gap: "16px" }}>
        <button
          onClick={(event) => {
            event.stopPropagation();
            setConfirmDialog(true);
          }}
          className="min-w-[100px] shadow-shadown1 bg-white rounded-lg px-[14px] py-2 capitalize text-grayOz font-semibold text-sm hover:bg-white hover:shadow-shadown1"
        >
          Hủy bỏ
        </button>
        <button
          onClick={handleSubmit}
          className="min-w-[100px] shadow-shadown1 bg-primary rounded-lg px-[14px] py-2 capitalize text-white font-semibold text-sm hover:bg-primaryDark"
        >
          {camera ? "Xác nhận" : "Tạo mới"}
        </button>
      </DialogActions>
    </Dialog>
  );
}
