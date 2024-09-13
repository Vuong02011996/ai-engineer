import { useAuth } from "@/hooks/auth-hook";
import * as React from "react";
import clsx from "clsx";

export interface IDebugFlagProps {
  show?: boolean;
}

export function DebugFlag(props: IDebugFlagProps) {
  const { profile } = useAuth();
  return (
    <div
      className={clsx(
        "absolute top-0 left-0 w-fit h-fit bg-warning px-[30px] -rotate-45 text-center -translate-x-[25px] translate-y-[10px] z-1",
        profile?.is_superuser === true && props.show ? "flex" : "hidden"
      )}
    >
      <p className="text-xs text-blackOz font-medium">Debug</p>
    </div>
  );
}
