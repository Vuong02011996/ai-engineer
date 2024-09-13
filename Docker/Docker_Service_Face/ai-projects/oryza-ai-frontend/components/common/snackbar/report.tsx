import { CustomContentProps, SnackbarContent } from "notistack";
import React from "react";
import { Snackbar } from "./snackbar";

interface ReportCompProps extends CustomContentProps {
  allowDownload: boolean;
}

export const ReportComp = React.forwardRef<HTMLDivElement, ReportCompProps>(
  (props, ref) => {
    const { id, message, allowDownload, variant, ...other } = props;

    return (
      <SnackbarContent ref={ref} role="alert" {...other}>
        <Snackbar message={message} id={id} variant={variant} />
      </SnackbarContent>
    );
  }
);
ReportComp.displayName = "ReportComp";
