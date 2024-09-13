import { useAuth } from "@/hooks/auth-hook";
import { useAppDispatch } from "@/hooks/useReudx";
import { formatInfoServer } from "@/libs/format-data";
import { setInfoServer, setServer } from "@/store/server";
import { memo, useEffect } from "react";

export interface ISocketProps {}

const SocketServer = (props: ISocketProps) => {
  const { profile, firstLoading } = useAuth();
  const dispatch = useAppDispatch();

  const SOCKET_DOMAIN = process.env.NEXT_PUBLIC_SOCKET_DOMAIN + "/super_admin";

  useEffect(() => {
    if (firstLoading) return;

    if (profile?.is_superuser === true) {
      const socket = new WebSocket(SOCKET_DOMAIN);
      socket.onmessage = function name(event: any) {
        let obj = JSON.parse(event.data);
        if (obj?.type === "ALIVE_SERVER") {
          const action = setServer({ data: obj.data });
          dispatch(action);
        }
        if (obj?.type === "INFO_SERVER") {
          let newItem = formatInfoServer(obj.data);
          const action = setInfoServer({ data: newItem });
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
export default memo(SocketServer);
