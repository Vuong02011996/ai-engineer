import { Status, TableAction } from "@/components";
import { LoadingPopup } from "@/components/common/loading/loading-popup";
import { SwitchBtn } from "@/components/common/switch/switch-btn";
import { DialogConfirm } from "@/components/dialog/confirm-dialog";
import { TypeServiceKey } from "@/constants/type-service";
import { PorcessRes } from "@/interfaces/process";
import {
  handleDeleteProcess,
  handleKillProcess,
  handleRunProcess,
} from "@/libs/process";
import moment from "moment";
import { useState } from "react";
import { ConfigAi } from "./config-ai";

export interface ITableItemCameraProps {
  data: PorcessRes;
  index: number;
  reload?: () => void;
}

export function TableItemCamera(props: ITableItemCameraProps) {
  const [loading, setLoading] = useState(false);
  const [openRemoveDialog, setOpenRemoveDialog] = useState(false);
  const [configAiDialog, setConfigAiDialog] = useState(false);
  const key = props.data.service.type_service.key;

  return (
    <div className="w-full flex flex-row min-w-[1200px] table-row-custom items-center overflow-hidden">
      {/* <DebugFlag show={props.data?.is_debug} /> */}
      <div className="w-[60px] py-6 flex justify-center">
        {_renderText(props.index.toString())}
      </div>
      <div className="w-[20%] py-6 flex justify-start">
        {_renderText(props?.data?.service?.name ?? "")}
      </div>
      <div className="w-[20%] py-6 flex justify-start">
        {_renderText(props?.data?.service?.type_service?.name ?? "")}
      </div>
      <div className="w-[20%] py-6 flex justify-start">
        {_renderText(moment(props.data.created).format("DD/MM/yyyy HH:mm:ss"))}
      </div>

      <div className="w-[20%] py-6 flex justify-start">
        <Status status={props.data.status === "START" ? "ONLINE" : "OFFLINE"} />
      </div>
      <div className="w-[15%] py-6 flex justify-start">
        <SwitchBtn
          checked={props.data.isEnable}
          onChange={(e) => {
            if (e.target.checked) {
              handleRunProcess({
                id: props.data.id ?? "",
                reload: props.reload,
                setLoading: setLoading,
              });
            } else {
              handleKillProcess({
                id: props.data.id ?? "",
                reload: props.reload,
                setLoading: setLoading,
              });
            }
          }}
        />
      </div>
      <div className="w-[5%] py-6 flex justify-center items-center gap-3">
        <TableAction
          onRemove={() => setOpenRemoveDialog(true)}
          onAIHandle={
            key === TypeServiceKey.CROWD_DETECTION_EXCHANGES ||
            key === TypeServiceKey.DETECT_ITEMS_FORGOTTEN_EXCHANGES ||
            key === TypeServiceKey.IDENTIFY_UNIFORMS_EXCHANGES ||
            key === TypeServiceKey.plate_number ||
            key === TypeServiceKey.loitering ||
            key === TypeServiceKey.CAMERA_TAMPERING_EXCHANGES ||
            key === TypeServiceKey.CAMERA_TRAFFIC_SIGNAL_EXCHANGES || 
            key === TypeServiceKey.illegal_parking ||
            key === TypeServiceKey.tripwire ||
            key === TypeServiceKey.lane_violation ||
            key === TypeServiceKey.line_violation ||
            key === TypeServiceKey.wrong_way || 
            key === TypeServiceKey.obj_attr
              ? () => setConfigAiDialog(true)
              : undefined
          }
        />
      </div>

      <LoadingPopup open={loading} />

      {openRemoveDialog && (
        <DialogConfirm
          close={() => setOpenRemoveDialog(false)}
          action={() => {
            handleDeleteProcess({
              id: props.data.id ?? "",
              reload: props.reload,
              setLoading: setLoading,
            });
          }}
          image={"/icons/bin.svg"}
          title={"Bạn chắc chắn xoá không?"}
          description={"Sau khi xoá, dữ liệu sẽ không được phục hồi."}
        />
      )}

      {configAiDialog && (
        <ConfigAi
          processId={props.data.id}
          cameraId={props.data.camera}
          keyAI={props.data.service.type_service.key}
          open={true}
          handleClose={() => setConfigAiDialog(false)}
        />
      )}
    </div>
  );
}

function _renderText(text: string) {
  return <p className="font-medium text-grayOz text-sm">{text}</p>;
}
