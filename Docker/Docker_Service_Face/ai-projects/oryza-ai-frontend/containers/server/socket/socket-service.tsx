import { useService } from "@/context/service-context";
import { useAuth } from "@/hooks/auth-hook";
import { useAppDispatch } from "@/hooks/useReudx";
import { setService } from "@/store/server";
import { memo, useEffect } from "react";

export interface ISocketProps {}

const SocketService = (props: ISocketProps) => {
  const { profile, firstLoading } = useAuth();

  const SOCKET_DOMAIN = process.env.NEXT_PUBLIC_SOCKET_DOMAIN + "/super_admin";

  const dispatch = useAppDispatch();

  useEffect(() => {
    if (firstLoading) return;

    if (profile?.is_superuser === true) {
      const socket = new WebSocket(SOCKET_DOMAIN);
      socket.onmessage = function name(event: any) {
        let obj = JSON.parse(event.data);
        if (obj?.type === "ALIVE_SERVICE") {
          const action = setService({ data: obj.data });
          dispatch(action);
        }
      };
      return () => {
        socket.close();
      };
    }
  }, [firstLoading, profile]);

  return <></>;
};
export default memo(SocketService);
