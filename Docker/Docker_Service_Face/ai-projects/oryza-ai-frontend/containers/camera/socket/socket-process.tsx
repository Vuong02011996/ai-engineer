import { useAuth } from "@/hooks/auth-hook";
import { useAppDispatch } from "@/hooks/useReudx";
import { setProcess } from "@/store/process";
import { uuidv4 } from "@/utils/global-func";
import { memo, useEffect } from "react";

export interface ISocketProps {}

const SocketProcess = (props: ISocketProps) => {
  const { profile, firstLoading } = useAuth();

  const SOCKET_DOMAIN = process.env.NEXT_PUBLIC_SOCKET_DOMAIN + "/super_admin";

  const dispatch = useAppDispatch();

  useEffect(() => {
    if (firstLoading) return;

    const socket = new WebSocket(SOCKET_DOMAIN);
    socket.onmessage = function name(event: any) {
      let obj = JSON.parse(event.data);
      if (obj?.type === "STATUS_PROCESS") {
        const action = setProcess({
          data: {
            ...obj.data,
            socketId: uuidv4(),
          },
        });
        dispatch(action);
      }
    };
    return () => {
      socket.close();
    };
  }, [firstLoading, profile]);

  return <></>;
};
export default memo(SocketProcess);
