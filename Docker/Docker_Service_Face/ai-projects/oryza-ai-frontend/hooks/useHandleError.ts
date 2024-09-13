import { enqueueSnackbar } from "notistack";

const useHandleError = () => {
  const handleError = (
    error: any,
    defaultMessage: string = "không thành công"
  ) => {
    const errorMsg = error?.response?.data?.detail ?? defaultMessage;
    enqueueSnackbar(errorMsg, {
      variant: "error",
    });
  };

  return handleError;
};

export default useHandleError;
