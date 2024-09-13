import { useAppDispatch } from "@/hooks/useReudx";
import { addData } from "@/store/camra-person";
import { memo, useEffect } from "react";

export interface ISocketProps {
  id: string;
}

type EventType = "success" | "error";
export interface CameraPersonEvent {
  id_camera: string;
  percent: string;
  type: EventType;
}

const SocketCameraPerson = ({ id }: ISocketProps) => {
  const SOCKET_DOMAIN = process.env.NEXT_PUBLIC_SOCKET_DOMAIN + "/add_user/";

  const dispatch = useAppDispatch();

  useEffect(() => {
    if (!id) return;
    const socket = new WebSocket(SOCKET_DOMAIN + id);

    socket.onmessage = function name(event: any) {
      const eventData: CameraPersonEvent = JSON.parse(event.data);
      const action = addData({ data: eventData });
      dispatch(action);
    };
    return () => {
      socket.close();
    };
  }, [SOCKET_DOMAIN, id]);

  return <></>;
};
export default memo(SocketCameraPerson);
