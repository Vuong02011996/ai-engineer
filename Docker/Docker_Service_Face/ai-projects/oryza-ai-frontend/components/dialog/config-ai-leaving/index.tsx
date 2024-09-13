import { processApi } from "@/api-client/process";
import { EmptyData, Loading } from "@/components/common";
import { DrawAreaObjectsConfig} from "@/components/common/paint/draw-area-object";
import { LoadingPopup } from "@/components/common/loading/loading-popup";
import { CancelBtn, FieldNumber, SubmitBtn, Transition } from "@/components/ui";
import { ResultEnum } from "@/constants/enum";
import { Validator } from "@/utils/validate";
import CloseRoundedIcon from "@mui/icons-material/CloseRounded";
import { Box, Grid, IconButton, Stack, Typography } from "@mui/material";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogTitle from "@mui/material/DialogTitle";
import { enqueueSnackbar } from "notistack";
import { useEffect, useState } from "react";
import { ConfirmCloseDialog } from "../confirm-dialog/confirm-close-dialog";

export interface IConfigAILeavingDialogProps {
  open: boolean;
  handleClose: () => void;
  submit: (data: any) => Promise<ResultEnum>;
  data: any;
}

const formInit = {
  area_str: "",
  object_str: "",
  alert_interval: 10,
  alert_delay: undefined,
  image_url: "",
};

export function ConfigAILeavingDialog(
  props: IConfigAILeavingDialogProps
) {
  // ************** --init state-- *****************
  const { open, handleClose, submit, data } = props;
  const [formErr, setFormErr] = useState<any>({});
  const [form, setForm] = useState<any>(formInit);
  const [confirmDialog, setConfirmDialog] = useState(false);
  const [image, setImage] = useState<any>("");
  const [loadingImg, setLoadingImg] = useState(true);
  const [loading, setLoading] = useState(false);

  // * * * * * * * * HANDLE INPUT CHANGE * * * * * * * * *
  const handleInputChange = (key: string, value: any) => {
    setForm({ ...form, [key]: value });
    setFormErr({ ...formErr, [key]: null });
  };

  // * * * * * * * * ON CLOSE * * * * * * * * *
  const onClose = () => {
    handleClose();
    setFormErr({});
    setImage("");
    setForm(formInit);
  };

  // * * * * * * * * VALIDATE FUNCTION * * * * * * * * *
  const checkValidate = (form: any) => {
    let hasError = false;
    console.log('form', form);
    let error = {
      ...formErr,
      alert_interval: Validator.checkContainsOnlyNumbers(
        form["alert_interval"] ?? ""
      ),
      alert_delay: Validator.checkContainsOnlyNumbers(
        form["alert_delay"] ?? ""
      ),
      object: Validator.checkLeavingObjects(form["area_str"], form["object_str"] ?? ""),
    };

    if (
      error.alert_interval !== null || error.alert_delay !== null
      || error.object !== null
    ) {
      hasError = true;
    }
    if (error.object) {
      enqueueSnackbar(error.object, { variant: "error" });
    }

    setFormErr(error);

    return !hasError;
  };

  const getImage = async (process_id: string) => {
    // display image and set image_url to form
    if (!process_id) return;
    setImage("");
    setLoadingImg(true);
    try {
      let { data } = await processApi.getPreviewImage(process_id);
      setImage(data);
      setForm((prevForm: any) => {
        const updatedForm = { ...prevForm, image_url: data };
        return updatedForm;
      });
    } catch (error) {
      enqueueSnackbar("Không tải được hình ảnh", {
        variant: "error",
      });
    } finally {
      setLoadingImg(false);
    }
  };

  // * * * * * * * * INIT FORM * * * * * * * * *
  useEffect(() => {
    if (!open) return;
    if (props?.data?.setting) {
      setLoadingImg(false);
      const leavingData = props?.data?.setting;
      console.log('leavingData', leavingData);
      setImage(leavingData.image_url);
      setForm({
        area_str: leavingData.area_str,
        object_str: leavingData.object_str,
        alert_interval: leavingData.alert_interval,
        alert_delay: leavingData.alert_delay,
      });
      getImage(props.data?.process_id);
    } else {
      getImage(props.data?.process_id);
    }

    return () => {};
  }, [props.data, open]);

  return (
    <Dialog
      open={open}
      TransitionComponent={Transition}
      onClose={() => setConfirmDialog(true)}
      aria-describedby="alert-dialog-slide-description"
      fullWidth
      maxWidth="lg"
      PaperProps={{
        sx: {
          borderRadius: "11px",
          boxShadow: "0px 1px 10px 0px rgba(34, 34, 34, 0.10)",
          padding: "16px",
          position: "relative",
          width: "1200px", // Fixed width
          minWidth: "1200px", 
          overflowX: "auto",
        },
        component: "form",
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
        onClick={() => setConfirmDialog(true)}
        aria-label="delete"
        size="small"
        title="Đóng"
        className="w-[32px] h-[32px] flex top-[16px] right-[16px]"
        sx={{
          position: "absolute",
        }}
      >
        <CloseRoundedIcon fontSize="inherit" sx={{ fontSize: 24 }} />
      </IconButton>

      <DialogTitle className="text-start text-[#1C2A53] text-xl font-medium p-0 ">
        Cấu hình AI phát hiện rời vị trí
      </DialogTitle>
      <DialogContent
        sx={{
          marginTop: "20px",
          padding: "0px 40px",
          height: "100%",
          overflow: "hidden",
        }}
      >
        <Stack
          sx={{
            minHeight: 400,
          }}
        >
          <Grid container columnSpacing={10}>
            <Grid item xs={7}>
              {loadingImg ? (
                <Loading />
              ) : !image ? (
                <EmptyData />
              ) : (
                <DrawAreaObjectsConfig
                  image={image}
                  onReloadImage={() => {
                    getImage(props.data?.process_id);
                  }}
                  onSubmit={(area_str: string, object_str: string) => {
                    setForm({ ...form, area_str: area_str, object_str: object_str});
                  }}
                  area_str={form["area_str"]}
                  object_str={form["object_str"]}
                />
              )}
            </Grid>
            <Grid item xs={5}>
              <Stack spacing={2}>
                <FieldNumber
                  text={"Thời gian chờ trước khi bật cảnh báo (giây)"}
                  value={form["alert_delay"]}
                  onChange={function (e: any): void {
                    const key = "alert_delay";
                    handleInputChange(key, e.target.value);
                  }}
                  textError={formErr["alert_delay"]}
                />
                <FieldNumber
                  text={"Khoảng cách giữa các lần cảnh báo (giây)"}
                  value={form["alert_interval"]}
                  onChange={function (e: any): void {
                    const key = "alert_interval";
                    handleInputChange(key, e.target.value);
                  }}
                  textError={formErr["alert_interval"]}
                />
              </Stack>
              <Box
                sx={{
                  border: '1px solid #ccc',
                  borderRadius: '8px',
                  padding: '16px',
                  marginTop: '16px',
                  maxHeight: '280px', 
                  overflowY: 'auto'
                }}
              >
                <Typography variant="h6" gutterBottom>
                  HƯỚNG DẪN SỬ DỤNG
                </Typography>
                <Typography variant="body1" style={{ textAlign: 'justify' }}>
                  <span style={{ fontWeight: 'bold', color: '#1976d2' }}>Thanh công cụ</span> gồm có 6 nút chức năng <span style={{ fontWeight: 'bold', color: 'green' }}>từ trái sang phải</span> như sau: <br />
                  <span style={{ fontWeight: 'bold' }}>1. Nút Di chuyển:</span> <span style={{ fontStyle: 'italic' }}>Dùng để di chuyển khu vực theo dõi hoặc di chuyển đối tượng đã vẽ.</span> <br />
                  <span style={{ color: 'brown' }}>Chú ý:</span> Bạn phải di chuyển đối tượng vào bên trong khu vực theo dõi, thay vì di chuyển khu vực theo dõi tới đối tượng. <br />
                  <span style={{ fontWeight: 'bold' }}>2. Nút Vẽ khu vực theo dõi:</span> Bạn sẽ chọn lần lượt từng điểm, các cạnh của khu vực theo dõi sẽ hiện ra. <br />
                  <span style={{ fontWeight: 'bold' }}>3. Nút Vẽ đối tượng:</span> Bạn chọn 2 điểm trái-trên và phải-dưới của đối tượng, sau đó đối tượng sẽ hiện ra. <br />
                  <span style={{ color: 'purple' }}>Khi muốn di chuyển một điểm đã vẽ:</span> Bạn chọn nút Vẽ khu vực hoặc Vẽ đối tượng tương ứng với điểm đó, rồi di chuyển điểm. <br />
                  <span style={{ fontWeight: 'bold' }}>4. Nút Xóa điểm:</span> Chọn vào một điểm, điểm đó sẽ chuyển màu đỏ. Chọn nút xóa, điểm được chọn sẽ mất đi. <br />
                  <span style={{ fontWeight: 'bold' }}>5. Nút Xóa tất cả:</span> Xóa tất cả điểm đã vẽ. <br />
                  <span style={{ fontWeight: 'bold' }}>6. Nút Tải lại hình ảnh:</span> Tải lại hình ảnh ban đầu. <br />
                </Typography>
              </Box>
            </Grid>
          </Grid>
        </Stack>
      </DialogContent>
      <DialogActions sx={{ justifyContent: "end", gap: "16px" }}>
        <CancelBtn text={"Hủy bỏ"} onClick={() => setConfirmDialog(true)} />
        <SubmitBtn
          disabled={image === ""}
          text={"Cập nhật"}
          onClick={async (e) => {
            e.preventDefault();
            if (!checkValidate(form)) return;
            setLoading(true);
            const result = await submit(form);
            setLoading(false);
            if (result === ResultEnum.success) onClose();
          }}
        />
      </DialogActions>
    </Dialog>
  );
}