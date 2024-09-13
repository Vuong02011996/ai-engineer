import { processApi } from "@/api-client/process";
import { EmptyData, Loading } from "@/components/common";
import { DrawLineComponenent } from "@/components/common/paint/draw-line";
import { LoadingPopup } from "@/components/common/loading/loading-popup";
import { CancelBtn, SubmitBtn, Transition } from "@/components/ui";
import { ResultEnum } from "@/constants/enum";
import { Validator } from "@/utils/validate";
import CloseRoundedIcon from "@mui/icons-material/CloseRounded";
import {
  FormControl,
  FormControlLabel,
  FormLabel,
  Grid,
  IconButton,
  Radio,
  RadioGroup,
  Stack,
} from "@mui/material";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogTitle from "@mui/material/DialogTitle";
import { enqueueSnackbar } from "notistack";
import { useEffect, useState } from "react";
import { ConfirmCloseDialog } from "../confirm-dialog/confirm-close-dialog";
import { TypeServiceKey } from "@/constants/type-service";

export interface IConfigAIPlateNumberDialogProps {
  open: boolean;
  handleClose: () => void;
  submit: (data: any) => Promise<ResultEnum>;
  data: any;
}

const formInit = {
  boundary: "",
  object_detect: "plate", // vehicle
  image_url: "",
};

export function ConfigAIPlateNumberDialog(
  props: IConfigAIPlateNumberDialogProps
) {
  // ************** --init state-- *****************
  const { open, handleClose, submit, data } = props;
  const [formErr, setFormErr] = useState<any>({});
  const [form, setForm] = useState<any>(formInit);
  const [image, setimage] = useState<any>("");
  const [loadingImg, setLoadingImg] = useState(true);
  const [confirmDialog, setConfirmDialog] = useState(false);
  const [loading, setLoading] = useState(false);

  // * * * * * * * * ON CLOSE * * * * * * * * *
  const onClose = () => {
    handleClose();
    setFormErr({});
    setimage("");
    setForm(formInit);
  };

  // * * * * * * * * VALIDATE FUNCTION * * * * * * * * *
  const checkValidate = (form: any) => {
    let hasError = false;

    let error = {
      ...formErr,
      boundary: Validator.checkBoundary(form["boundary"] ?? ""),
    };

    if (error.boundary !== null) {
      hasError = true;
    }

    if (error.boundary) {
      enqueueSnackbar(error.boundary, { variant: "error" });
    }

    setFormErr(error);

    return !hasError;
  };

  // * * * * * * * * GET IMAGE * * * * * * * * *
  // const getImage = async (id: string) => {
  //   if (!id) return;
  //   setimage("");
  //   setLoadingImg(true);

  //   try {
  //     let { data } = await plateNumberApi.getImageByIdCamera(id);
  //     setimage(data);
  //     setForm({ ...form, image_url: data });
  //   } catch (error) {
  //   } finally {
  //     setLoadingImg(false);
  //   }
  // };
  const getImage = async (process_id: any) => {
    if (!process_id) return;
    setimage("");
    setLoadingImg(true);
    try {
      let { data } = await processApi.getPreviewImage(process_id);
      setimage(data);
      setForm({ ...form, image_url: data });
    } catch (error) {
      enqueueSnackbar("Không tải được hình ảnh", {
        variant: "error",
      });
    } finally {
      setLoadingImg(false);
    }
  }

  // * * * * * * * * INIT FORM * * * * * * * * *
  useEffect(() => {
    if (!open) return;

    if (props?.data?.setting) {
      setLoadingImg(false);
      const crowdData = props?.data?.setting;

      setimage(crowdData?.image_url);
      setForm({
        boundary: crowdData?.line,
        object_detect: crowdData?.object_detect,
        image_url: crowdData?.image_url,
      });
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
        Cấu hình AI nhận diện biển số
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
                <DrawLineComponenent
                  image={image}
                  lines={data.setting?.line}
                  onReloadImage={() => {
                    getImage(props.data?.process_id);
                  }}
                  onSubmit={(boundary: any) => {
                    setForm({ ...form, boundary: boundary });
                  }}
                  type={TypeServiceKey.plate_number}
                />
              )}
            </Grid>
            <Grid item xs={5}>
              <Stack spacing={2}>
                <FormControl
                  className="w-full"
                  sx={{
                    "& .Mui-focused": {
                      color: "#55595d",
                    },
                    userSelect: "none",
                  }}
                >
                  <FormLabel
                    id="services-type"
                    sx={{
                      color: "#55595d !important",
                      fontSize: "14px",
                      fontWeight: 400,
                      ":focus": {},
                    }}
                  >
                    Chọn loại nhận dạng
                  </FormLabel>
                  <RadioGroup
                    aria-labelledby="services-type"
                    name="type"
                    sx={{
                      display: "flex",
                      flexDirection: "row",
                    }}
                    value={form["object_detect"]}
                    onChange={(e) => {
                      setForm({ ...form, ["object_detect"]: e.target.value });
                    }}
                  >
                    {[
                      {
                        id: "plate",
                        name: "Biển số",
                      },
                      {
                        id: "vehicle",
                        name: "Biển số và loại xe",
                      },
                    ].map((item) => (
                      <FormControlLabel
                        key={item.id}
                        value={item.id}
                        control={
                          <Radio
                            className=""
                            size="small"
                            sx={{
                              color: "#55595d",
                            }}
                          />
                        }
                        label={<p className="text-grayOz">{item.name}</p>}
                        sx={{
                          "& .Mui-checked": {
                            "& + .MuiFormControlLabel-label > p": {
                              color: "#323232",
                            },
                          },
                        }}
                      />
                    ))}
                  </RadioGroup>
                </FormControl>
              </Stack>
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
