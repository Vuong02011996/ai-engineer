import { Status, TableAction } from "@/components";
// import CheckboxCustom from "@/components/common/checkbox";
import { LoadingPopup } from "@/components/common/loading/loading-popup";
import { SwitchBtn } from "@/components/common/switch/switch-btn";
import { DialogConfirm } from "@/components/dialog/confirm-dialog";
// import { DebugFlag } from "@/components/ui/debug-flag";
import { TypeServiceKey } from "@/constants/type-service";
import { ConfigAi } from "@/containers/camera/child-table/config-ai";
// import { useAuth } from "@/hooks/auth-hook";
import { ProcessEvent } from "@/interfaces/process-page";
import {
  handleDeleteProcess,
  handleKillProcess,
  handleRunProcess,
} from "@/libs/process";
import { useRouter } from "next/router";
import { memo, useState } from "react";
import { CopyBtn } from "@/components/common/button/copy-btn";

export interface ITableFaceAiProps {
  data: ProcessEvent;
  index: number;
  reload: any;
}

function TableFaceAi(props: ITableFaceAiProps) {
  // const { profile } = useAuth();
  const { data, index } = props;
  const router = useRouter();
  const [openRemoveDialog, setOpenRemoveDialog] = useState(false);
  const [configAiDialog, setConfigAiDialog] = useState(false);
  const [loading, setLoading] = useState(false);
  const key = props?.data?.service?.type_service?.key ?? "";
  // const [isDebug, setIsDebug] = useState(data?.is_debug === true);
  // console.log("key:", key); // Add this line to log the key
  const onClick = () => {
    router.push(`/camera/${data.camera?.id}`);
  };

  return (
    <div className="w-full flex flex-row min-w-[1200px] table-row-custom items-center border-b-2 border-[#F8F8F8]">
      {/* <DebugFlag show={props.data?.is_debug} /> */}
      <LoadingPopup open={loading} />
      <div onClick={onClick} className="w-[60px] py-6 flex justify-center">
        {_renderText(index.toString())}
      </div>
      <div onClick={onClick} className="w-[20%] py-6 pr-3 flex justify-start">
        {_renderText(data?.camera?.name)}
      </div>
      <div onClick={onClick} className="w-[20%] py-6 pr-3 flex justify-start">
        {_renderText(data?.camera?.ip_address)}
      </div>
      <div onClick={onClick} className="w-[15%] py-3 pr-3 flex justify-start">
        {_renderText(data?.service?.server?.name)}
      </div>
      <div onClick={onClick} className="w-[15%] py-6 pr-3 flex justify-start">
        {_renderText(data?.service?.name)}
      </div>
      <div onClick={onClick} className="w-[15%] py-6 pr-3 flex justify-start">
        <Status status={props.data.status === "START" ? "ONLINE" : "OFFLINE"} />
      </div>

      <div className="w-[8%] py-6 pr-3 flex justify-start">
        <SwitchBtn
          checked={data?.isEnable}
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
      <div className="w-[2%] py-6 pr-3 flex justify-end items-center gap-3">
        <CopyBtn text={data?.id} title="Process ID" />
      </div>
      <div className="w-[5%] py-6 pr-3 flex justify-end items-center gap-3">
        <TableAction
          onRemove={() => setOpenRemoveDialog(true)}
          onAIHandle={
            key === TypeServiceKey.CROWD_DETECTION_EXCHANGES ||
            key === TypeServiceKey.DETECT_ITEMS_FORGOTTEN_EXCHANGES ||
            key === TypeServiceKey.IDENTIFY_UNIFORMS_EXCHANGES ||
            key === TypeServiceKey.plate_number ||
            key === TypeServiceKey.loitering ||
            key === TypeServiceKey.CAMERA_TAMPERING_EXCHANGES || 
            key === TypeServiceKey.illegal_parking ||
            key === TypeServiceKey.tripwire ||
            key === TypeServiceKey.CAMERA_TRAFFIC_SIGNAL_EXCHANGES ||
            key === TypeServiceKey.lane_violation ||
            key === TypeServiceKey.line_violation ||
            key === TypeServiceKey.wrong_way ||
            key === TypeServiceKey.leaving ||
            key === TypeServiceKey.intrusion ||
            key === TypeServiceKey.obj_attr
              ? () => setConfigAiDialog(true)
              : undefined
          }
        />
      </div>
      {configAiDialog && (
        <ConfigAi
          processId={props.data.id ?? ""}
          cameraId={props?.data?.camera?.id ?? ""}
          keyAI={key as TypeServiceKey}
          open={true}
          handleClose={() => setConfigAiDialog(false)}
        />
      )}
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
    </div>
  );
}

function _renderText(text?: string) {
  return <p className="font-medium text-grayOz text-sm">{text || "--"}</p>;
}
export default memo(TableFaceAi);
