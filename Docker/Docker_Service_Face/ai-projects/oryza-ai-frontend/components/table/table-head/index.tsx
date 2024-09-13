import CheckboxCustom2 from "@/components/common/checkbox/checbox-2";
import clsx from "clsx";

export interface ITableHeadProps {
  dataHead: {
    id: number;
    name?: string;
    width: string;
    key: string;
    isCenter?: boolean;
  }[];
  hanleCheckAll?: (checked: boolean) => void;
}

export function TableHead(props: ITableHeadProps) {
  const { dataHead } = props;
  return (
    <div className="w-full h-[32px] flex flex-row bg-[#F1F1F1] min-w-[1200px] sticky top-0 z-999">
      {dataHead.map((menuHead) => {
        return (
          <div
            key={menuHead.id}
            className={clsx(
              "py-2 flex",
              menuHead.key === "INDEX" ||
                menuHead.key === "ACTION" ||
                menuHead.key === "CHECKBOX" ||
                menuHead.key === "TOTAL" ||
                menuHead.key === "MEMBER_OF_CROWD" ||
                menuHead.key === "crowd_alert_threshold" ||
                menuHead?.isCenter === true
                ? "justify-center"
                : menuHead.key === "END"
                ? "justify-end"
                : "justify-start"
            )}
            style={{ width: menuHead.width }}
          >
            {menuHead.key === "CHECKBOX" ? (
              <CheckboxCustom2
                onChange={(checked) => {
                  if (props.hanleCheckAll) props.hanleCheckAll(checked);
                }}
              />
            ) : (
              <p
                className={clsx(
                  "text-[#8E95A9] font-semibold text-sm",
                  menuHead.key === "END" && "pr-10"
                )}
              >
                {menuHead.name}
              </p>
            )}
          </div>
        );
      })}
    </div>
  );
}
