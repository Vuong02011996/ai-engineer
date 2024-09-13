import gridIcon from "@/assets/svgs/grid.svg";
import listIcon from "@/assets/svgs/list.svg";
import { MainHead } from "@/components";
import { BigBtn, OpactityAnimation, SeoPage } from "@/components/common";
import { ActionItem } from "@/components/file-action/item";
import { HeadContent } from "@/components/head/content-head";
import { FilterComponents } from "@/components/popup/filter";
import { TypeServiceKey } from "@/constants/type-service";
import { PickTimeFaceAi } from "@/containers/manage/face-ai/pick-time";
import { ManageProvider, useManagement } from "@/context/manage-context";
import { optionFilterFaceAi } from "@/data/manage";
import { useRouter } from "next/router";
import * as React from "react";
import addBlueIcon from "@/assets/svgs/add-blue.svg";
import { IdentificationUserDialog } from "@/components/dialog/create-identification-user";
import { IdentificationUserUpdateDialog } from "@/components/dialog/update-identification-user";
import { useState } from "react";
import { personApi } from "@/api-client/identification-profile/person";
import { enqueueSnackbar } from "notistack";
import { ResultEnum } from "@/constants/enum";
import useHandleError from "@/hooks/useHandleError";
import { eventApi } from "@/api-client/event";
import { TabHeaderManage } from "@/containers/manage/tab-header";

export interface IManageLayoutProps {
  children: React.ReactNode;
  tabIndex: string;
  handleChangeTab: (tab: any) => void;
}

const ManageLayoutComp = (props: IManageLayoutProps) => {
  const { tabData, textSearch, setTextSearch, imagesList, eventIds } =
    useManagement();

  const router = useRouter();
  const handleError = useHandleError();
  const [openCreate, setOpenCreate] = useState(false);
  const [openUpdate, setOpenUpdate] = useState(false);

  const handleCreate = async (formData: any) => {
    try {
      const personId = await personApi.create(formData).then(async (res) => {
        const payload = {
          user_id: res.data.id,
          name: res.data.name,
          list_id_event: eventIds,
        };
        await eventApi.updateFaceRecognition(payload);
        return res.data.id;
      });
      enqueueSnackbar("Thêm mới hồ sơ nhận diện đối tượng thành công ", {
        variant: "success",
      });

      // router.reload();
      return personId;
    } catch (error) {
      handleError(error, "Thêm mới hồ sơ nhận diện đối tượng không thành công");
      return ResultEnum.error;
    }
  };

  return (
    <section className="p-[24px] h-full">
      <SeoPage title="Quản lý dữ liệu" />

      <MainHead searchValue={textSearch} onChange={setTextSearch} />

      <div className="h-calc50 shadow-shadown1 rounded-[16px] relative">
        <HeadContent
          key="manage"
          title={"Danh sách dữ liệu AI"}
          tabData={tabData}
          tabIndex={props.tabIndex}
          handleChangeTab={(v) => {
            props.handleChangeTab(v);
            setTextSearch("");
          }}
          hiddenCreateBtn
          hiddenUpdateBtn
          tabChildren={<TabHeaderManage setOpenCreate={setOpenCreate} setOpenUpdate={setOpenUpdate}/>}
        />

        <OpactityAnimation className={"h-calc112  "}>
          {props.children}
        </OpactityAnimation>
      </div>
      <IdentificationUserDialog
        open={openCreate}
        handleClose={() => setOpenCreate(false)}
        submit={handleCreate}
        defaultImage={imagesList}
      />
      <IdentificationUserUpdateDialog
        open={openUpdate}
        handleClose={() => setOpenUpdate(false)}
        // submit={handleUpdate}
        defaultImage={imagesList}
      />
    </section>
  );
};
export function ManageLayout(props: IManageLayoutProps) {
  return (
    <ManageProvider>
      <ManageLayoutComp
        children={props.children}
        tabIndex={props.tabIndex}
        handleChangeTab={props.handleChangeTab}
      />
    </ManageProvider>
  );
}
