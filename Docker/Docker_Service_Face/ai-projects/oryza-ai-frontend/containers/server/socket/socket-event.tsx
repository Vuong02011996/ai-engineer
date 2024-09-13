import { useAuth } from "@/hooks/auth-hook";
import { useAppDispatch } from "@/hooks/useReudx";
import { EventData } from "@/interfaces/manage/event";
import { formatEventData } from "@/libs/format-data";
import { setDataEvent } from "@/store";
import { memo, useEffect } from "react";

export interface ISocketProps {}

const SocketEvent = (props: ISocketProps) => {
  const { profile, firstLoading } = useAuth();

  const SOCKET_DOMAIN =
    process.env.NEXT_PUBLIC_SOCKET_DOMAIN + "/" + profile?.company?.id;

  const dispatch = useAppDispatch();

  useEffect(() => {
    if (firstLoading) {
      return;
    }

    if (profile?.company?.id) {
      const socket = new WebSocket(SOCKET_DOMAIN);

      socket.onmessage = function name(event: any) {
        let obj = JSON.parse(event.data);

        let response: EventData = formatEventData([obj?.data], false)[0];
        obj.data = response;
        console.log("objobj: ", obj);

        const action = setDataEvent({ data: obj });
        dispatch(action);
      };
      return () => {
        socket.close();
      };
    }
  }, [firstLoading, profile?.company?.id, SOCKET_DOMAIN]);

  return <></>;
};
export default memo(SocketEvent);
