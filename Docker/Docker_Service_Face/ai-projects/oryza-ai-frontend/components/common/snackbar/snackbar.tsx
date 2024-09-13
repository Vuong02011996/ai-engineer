import { closeSnackbar } from "notistack";
type Variant = "success" | "default" | "error" | "info" | "warning";
export interface ISnackbarProps {
  message: any;
  id: any;
  variant: Variant;
}

export function Snackbar(props: ISnackbarProps) {
  const variant = props.variant ?? "default";

  function getColorForVariant(variant: Variant) {
    const colorMapping = {
      success: "#22AE68",
      default: "#E42727",
      error: "#E42727",
      info: "#78C6E7",
      warning: "#FF7A00",
    };

    if (colorMapping.hasOwnProperty(variant)) {
      return colorMapping[variant];
    } else {
      return "#999999";
    }
  }
  return (
    <div
      style={{
        background: getColorForVariant(variant),
      }}
      className="flex flex-row p-3 rounded-md space-x-3 items-center"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
      >
        <rect width="24" height="24" rx="6" fill="white" />
        <path
          d="M6 12.8L9.42857 16L18 8"
          stroke={getColorForVariant(variant)}
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
      <p className="text-white">{props.message}</p>
      <div
        onClick={() => closeSnackbar(props.id)}
        style={{
          width: "16px",
          height: "16px",
          alignItems: "center",
          justifyContent: "center",
          cursor: "pointer",
          color: "white",
        }}
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="16"
          height="16"
          viewBox="0 0 16 16"
          fill="none"
        >
          <path
            d="M4.99997 4.00003C4.72383 3.72389 4.27611 3.72389 3.99997 4.00003C3.72383 4.27617 3.72383 4.72389 3.99997 5.00003L6.99997 8.00003L4 11C3.72386 11.2761 3.72386 11.7239 4 12C4.27614 12.2761 4.72386 12.2761 5 12L7.99997 9.00003L11 12C11.2761 12.2762 11.7238 12.2762 12 12C12.2761 11.7239 12.2761 11.2762 12 11L8.99997 8.00003L12 5C12.2761 4.72386 12.2761 4.27614 12 4C11.7239 3.72386 11.2761 3.72386 11 4L7.99997 7.00003L4.99997 4.00003Z"
            fill="#DFF5E8"
          />
        </svg>
      </div>
    </div>
  );
}
