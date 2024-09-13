import { TableAction } from "@/components";
import { IPerson } from "@/interfaces/identification-profile/person";
import { Stack } from "@mui/material";
import moment from "moment";
import { ImageStack } from "../../ui/image-stack";
import useScrollToElement from "@/hooks/use-scroll-to-element";
import { CopyBtn } from "@/components/common/button/copy-btn";

export interface IListItemTableProps {
  data: IPerson;
  index: number;
  reload: any;
  setTotal: any;
  handleClick: any;
  setOpenEditDialog: any;
  setOpenRemoveDialog: any;
}

export function ListItemTable(props: IListItemTableProps) {
  const { data, handleClick, setOpenEditDialog, setOpenRemoveDialog } = props;

  return (
    <Stack
      className=" table-row-custom"
      sx={{
        minWidth: "1200px",
        ":hover": {
          ".img-item:nth-of-type(2)": {
            left: "50px",
          },
          ".img-item:nth-of-type(3)": {
            left: "100px",
          },
          ".img-item:nth-of-type(4)": {
            left: "150px",
          },
          ".image-number": {
            opacity: 0,
          },
        },
        ".img-item:nth-of-type(2)": {
          opacity: 0.8,
        },
        ".img-item:nth-of-type(3)": {
          opacity: 0.5,
        },
        ".img-item:nth-of-type(4)": {
          opacity: 0.2,
        },
        alignItems: "center",
        display: "flex",
        flexDirection: "row",
      }}
    >
      <div onClick={handleClick} className="w-[60px] py-6 flex justify-center">
        {_renderText(props.index.toString())}
      </div>

      <div onClick={handleClick} className="w-[15%] py-6 flex justify-start">
        {_renderText(data?.name ?? "--")}
      </div>
      <div onClick={handleClick} className="w-[10%] py-6 flex justify-start">
        {_renderText(
          data.other_info.gender === "male"
            ? "Nam"
            : data.other_info.gender === "female"
            ? "Nữ"
            : "--"
        )}
      </div>
      <div onClick={handleClick} className="w-[15%] py-6 flex justify-start">
        {_renderText(data?.other_info?.address ?? "--")}
      </div>
      <div onClick={handleClick} className="w-[30%] py-6 flex justify-start">
        <ImageStack images={data?.images} />
      </div>
      <div onClick={handleClick} className="w-[10%] py-6 flex justify-start">
        {_renderText(moment(new Date(data.created)).format("DD/MM/yyyy HH:mm"))}
      </div>
      <div className="w-[15%] py-6 flex justify-start" > 
        <div className="mr-2">{_renderText(data?.id)}</div>
        <CopyBtn text={data?.id} title="ID đối tượng" />
      </div>
      <div className="w-[5%] py-6 flex justify-center">
        <TableAction
          onEdit={() => setOpenEditDialog(true)}
          onRemove={() => setOpenRemoveDialog(true)}
        />
      </div>
    </Stack>
  );
}
function _renderText(text?: string) {
  return <p className="font-medium text-grayOz text-sm">{text || "--"}</p>;
}
