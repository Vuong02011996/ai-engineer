import addBlueIcon from "@/assets/svgs/add-blue.svg";
import gridIcon from "@/assets/svgs/grid.svg";
import listIcon from "@/assets/svgs/list.svg";
import { BigBtn } from "@/components/common";
import EditIcon from "@/assets/svgs/edit-icon.svg";
import { ActionItem } from "@/components/file-action/item";
import { FilterComponents } from "@/components/popup/filter";
import { TypeServiceKey } from "@/constants/type-service";
import { PickTimeFaceAi } from "@/containers/manage/face-ai/pick-time";
import { useManagement } from "@/context/manage-context";
import { optionFilterFaceAi } from "@/data/manage";
import { calculateStartTime } from "@/utils/global-func";
import { resultOptions } from "./config";
import { useRouter } from "next/router";

export interface TabHeaderManageProps {
  setOpenCreate: any;
  setOpenUpdate: any;
}

export function TabHeaderManage(props: TabHeaderManageProps) {
  const { setOpenCreate } = props;
  const { setOpenUpdate } = props;
  const router = useRouter();

  if (router.query.slug) {
    const type: string = router.query.slug as string;

    const {
      setStartTime,
      setEndTime,
      filter,
      setFilter,
      imagesList,
      viewType,
      onChangeViewType,
    } = useManagement();

    switch (type.toUpperCase()) {
      case TypeServiceKey.FACE_RECOGNITION_EXCHANGES:
        return (
          <div className="flex flex-row space-x-3">
            <div className="flex flex-row p-[4px] rounded-[8px] bg-[#F2F2F2]">
              <ActionItem
                active={viewType === "GRID"}
                onClick={() => onChangeViewType("GRID")}
                icon={gridIcon}
              />
              <ActionItem
                active={viewType === "LIST"}
                onClick={() => onChangeViewType("LIST")}
                icon={listIcon}
              />
            </div>
            <FilterComponents
              options={resultOptions}
              value={filter}
              onChange={(value) => {
                const currentTime = new Date();
                setEndTime(currentTime);
                setFilter(value);
              }}
            />
            <PickTimeFaceAi />
            {imagesList.length > 0 && (
              <>
              <BigBtn
                text={"Tạo mới"}
                icon={addBlueIcon}
                className={
                  "bg-primary hover:bg-[#026DA6] text-white h-10 truncate"
                }
                classIcon="bg-white"
                onClick={() => setOpenCreate(true)}
              />
              <BigBtn 
                text={"Cập nhật đối tượng"}
                icon={EditIcon}
                className={
                  "bg-primary hover:bg-[#026DA6] text-white h-10 truncate"
                }
                classIcon="bg-white"
                onClick={() => setOpenUpdate(true)}
              />
            </>
            )}
          </div>
        );
      default: 
        return (
          <div className="flex flex-row space-x-3">
            <div className="flex flex-row p-[4px] rounded-[8px] bg-[#F2F2F2]">
              <ActionItem
                active={viewType === "GRID"}
                onClick={() => {
                  onChangeViewType("GRID");
                }}
                icon={gridIcon}
              />
              <ActionItem
                active={viewType === "LIST"}
                onClick={() => onChangeViewType("LIST")}
                icon={listIcon}
              />
            </div>
            <FilterComponents
              options={optionFilterFaceAi}
              value={filter}
              onChange={(value) => {
                const currentTime = new Date();
                setEndTime(currentTime);
                setFilter(value);
                switch (value) {
                  case "ALL":
                    setStartTime(calculateStartTime(currentTime, 0, 360));
                    break;
                  case "ONE_HOUR":
                    setStartTime(calculateStartTime(currentTime, 1));
                    break;
                  case "FOUR_HOUR":
                    setStartTime(calculateStartTime(currentTime, 4));
                    break;
                  case "EIGHT_HOUR":
                    setStartTime(calculateStartTime(currentTime, 8));
                    break;
                }
              }}
            />
            <PickTimeFaceAi />
          </div>
        );

    }
  } else {
    return <></>;
  }
}
