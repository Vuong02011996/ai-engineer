import * as React from "react";
import clsx from "clsx";

export type QuickActionType = "ON" | "LOADING" | "OFF";

export interface IQuichActionProps {
  type: QuickActionType;
  onClick: (type: QuickActionType) => void;
}

export function QuichAction(props: IQuichActionProps) {
  const { type, onClick } = props;

  const typeMap = {
    OFF: "Giám sát",
    ON: "Hủy giám sát",
    LOADING: "Đang giám sát ...",
  };

  return (
    <div
      onClick={() => onClick(type)}
      className={clsx(
        "rounded-lg px-3 py-2 flex flex-row space-x-2 items-center transition-all duration-200",
        type == "OFF" && "bg-aquaTranquil hover:bg-aquaTranquilDark",
        type == "ON" && "bg-grayOz hover:bg-blackOz",
        type == "LOADING" && "bg-white shadow-shadown1 "
      )}
    >
      <div
        className={clsx(
          "  w-4 h-4 rounded-[4px] flex items-center justify-center",
          (type == "ON" || type === "OFF") && "bg-white  ",
          type == "LOADING" && "bg-grayOz"
        )}
      >
        {type === "ON" ? (
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            viewBox="0 0 16 16"
            fill="none"
          >
            <rect width="16" height="16" rx="4" fill="white" />
            <path
              fillRule="evenodd"
              clipRule="evenodd"
              d="M10.9442 11.942C11.0368 11.9804 11.136 12.0001 11.2362 12C11.3872 12.0003 11.5349 11.9558 11.6606 11.872C11.7863 11.7882 11.8842 11.669 11.942 11.5294C11.9998 11.3899 12.0148 11.2363 11.9852 11.0882C11.9556 10.9401 11.8826 10.8041 11.7756 10.6976L9.07876 8.00044L11.7766 5.30231C11.8474 5.23148 11.9036 5.14738 11.9419 5.05485C11.9803 4.96228 12 4.86305 12 4.76287C12 4.66269 11.9803 4.56351 11.9419 4.47094C11.9036 4.37837 11.8474 4.29427 11.7766 4.22343C11.7057 4.1526 11.6216 4.09642 11.5291 4.05804C11.4366 4.01971 11.3373 4 11.2372 4C11.137 4 11.0378 4.01971 10.9453 4.05804C10.8527 4.09642 10.7686 4.1526 10.6978 4.22343L8.00001 6.92156L5.3022 4.22343C5.23137 4.1526 5.14728 4.09642 5.05472 4.05804C4.96216 4.01971 4.86299 4 4.76282 4C4.66266 4 4.56344 4.01971 4.47088 4.05804C4.37837 4.09642 4.29427 4.1526 4.22341 4.22343C4.15258 4.29427 4.09641 4.37837 4.05808 4.47094C4.01975 4.56351 4 4.66269 4 4.76287C4 4.86305 4.01975 4.96228 4.05808 5.05485C4.09641 5.14738 4.15258 5.23148 4.22341 5.30231L6.92124 8.00046L4.22447 10.6976C4.11743 10.8041 4.04444 10.9401 4.0148 11.0882C3.9852 11.2363 4.0002 11.3899 4.05801 11.5294C4.11579 11.669 4.21375 11.7882 4.33941 11.872C4.46507 11.9558 4.61281 12.0003 4.76384 12C4.86405 12.0003 4.96335 11.9807 5.05591 11.9423C5.14851 11.9039 5.23256 11.8476 5.30321 11.7765L8 9.07935L10.6968 11.7765C10.7675 11.8474 10.8516 11.9037 10.9442 11.942Z"
              fill="#55595D"
            />
          </svg>
        ) : (
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="10"
            height="10"
            viewBox="0 0 10 10"
            fill="none"
          >
            <path
              fillRule="evenodd"
              clipRule="evenodd"
              d="M9.5 3.67281C9.5 3.92729 9.30503 4.13362 9.06452 4.13362L0.935506 4.13362C0.759338 4.13362 0.600591 4.02136 0.533178 3.84914C0.465765 3.67696 0.502985 3.47875 0.627533 3.34695L2.71785 1.13497C2.88792 0.955009 3.16367 0.955009 3.33374 1.13497C3.50381 1.31494 3.50381 1.60672 3.33374 1.78668L1.98682 3.21198L9.06452 3.21198C9.30503 3.21198 9.5 3.4183 9.5 3.67281Z"
              fill={type === "OFF" ? "#78C6E7" : "#fff"}
              stroke={type === "OFF" ? "#78C6E7" : "#fff"}
              strokeWidth="0.3"
            />
            <path
              fillRule="evenodd"
              clipRule="evenodd"
              d="M9.46684 6.1507C9.53424 6.32292 9.49699 6.52114 9.37244 6.65294L7.28212 8.86492C7.11205 9.04489 6.83632 9.04489 6.66625 8.86492C6.49618 8.68495 6.49618 8.39315 6.66625 8.21319L8.01316 6.78787L0.935493 6.78787C0.694991 6.78787 0.50001 6.58154 0.50001 6.32704C0.50001 6.07254 0.694991 5.86621 0.935493 5.86621L9.0645 5.86621C9.24064 5.86621 9.39943 5.97853 9.46684 6.1507Z"
              fill={type === "OFF" ? "#78C6E7" : "#fff"}
              stroke={type === "OFF" ? "#78C6E7" : "#fff"}
              strokeWidth="0.3"
            />
          </svg>
        )}
      </div>
      <p
        className={clsx(
          " font-medium text-[14px]",
          type === "LOADING" && "text-grayOz",
          (type === "ON" || type === "OFF") && "text-white"
        )}
      >
        {typeMap[type]}
      </p>
    </div>
  );
}
