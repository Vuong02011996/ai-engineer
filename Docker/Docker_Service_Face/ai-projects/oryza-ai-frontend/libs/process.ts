import { processApi } from "@/api-client/process";
import { enqueueSnackbar } from "notistack";

// * * * * * * * RUN PROCESS * * * * * * * * * * *
export const handleRunProcess = async (data: {
  id: string;
  reload?: () => void;
  setLoading: any;
  // isDebug: boolean;
}) => {
  const { id, reload, setLoading } = data;

  if (!data.id) return;
  setLoading(true);

  try {
    await processApi.run({ process_id: id, is_debug: false });
    if (reload) reload();
    enqueueSnackbar("Đã bật AI", { variant: "success" });
  } catch (error: any) {
    console.log("Run process Error", error);
    let reason = "";
    if (error.response?.data?.detail == "Setting not found") {
      reason = "chưa cấu hình";
    }
    console.log("reason", reason);
    let errorMsg = `Bật AI không thành công`
    if (reason) errorMsg += `: ${reason}`;
    enqueueSnackbar(errorMsg, { variant: "error" });
  } finally {
    setLoading(false);
  }
};

// * * * * * * * KILL PROCESS * * * * * * * * * *
export const handleKillProcess = async (data: {
  id: string;
  reload?: () => void;
  setLoading: any;
}) => {
  const { id, reload, setLoading } = data;

  if (!id) return;
  setLoading(true);
  try {
    await processApi.kill({ process_id: id });
    if (reload) reload();
    enqueueSnackbar("Đã tắt AI", { variant: "success" });
  } catch (error: any) {
    console.log("Kill process Error", error);
    const errorMsg = "Tắt AI không thành công";
    enqueueSnackbar(errorMsg, { variant: "error" });
  } finally {
    setLoading(false);
  }
};

// * * * * * * * DELETE PROCESS * * * * * * * * * * *
export const handleDeleteProcess = async (data: {
  id: string;
  reload?: () => void;
  setLoading: any;
}) => {
  const { id, reload, setLoading } = data;
  if (!id) return;
  setLoading(true);
  try {
    await processApi.delete(id);
    if (reload) reload();
    enqueueSnackbar("Xóa process thành công", { variant: "success" });
  } catch (error) {
    enqueueSnackbar("Xóa process không thành công", { variant: "error" });
  } finally {
    setLoading(false);
  }
};
