import { CopyBtn } from "@/components/common/button/copy-btn";
import ImageFallback from "@/components/common/image-fallback";
// import ImageMagnifyComponent from "@/components/common/image-with-hover-effect/zoom";
import { PreviewImage } from "@/components/common/preview-img";
import { EventData } from "@/interfaces/manage/event";
// import { Stack } from "@mui/material";
import moment from "moment";
import ViolationDetailsModal from "@/components/common/modal/violation-details-modal";
import { useState } from "react"; 
import React, { ReactNode } from 'react';
// import { vendored } from "next/dist/server/future/route-modules/app-page/module.compiled";

export interface IListItemTableProps {
  data: EventData;
  index: number;
}

export function ListItemTable(props: IListItemTableProps) {
  const { data, index } = props;
  const [modalOpen, setModalOpen] = useState(false);

  const _renderText = (text?: ReactNode) => <p className="font-medium text-grayOz text-sm">{text || "--"}</p>;

  const handleOpenModal = () => {
    setModalOpen(true);
  };
  
  const handleCloseModal = () => {
    setModalOpen(false);
  };
  const custom_traffic_data = {
    plate: data.license_plate,
    vehicle_type: data.vehicle_type,
    brand_name: data.brand_name,
    vehicle_color: data.vehicle_color,
    violation: data.violation,
    violation_code: data.violation_code,
    ...(Array.isArray(data.traffic_code) && data.traffic_code.length > 0 && { traffic_code: data.traffic_code }),
    ...(Array.isArray(data.safe_belt) && data.safe_belt.length > 0 && { safe_belt: data.safe_belt }),
    ...(Array.isArray(data.calling) && data.calling.length > 0 && { calling: data.calling }),
    ...(Array.isArray(data.smoking) && data.smoking.length > 0 && { smoking: data.smoking }),
    ...((data.lane != "") && { lane: data.lane }),
    ...(data.plate_color != "" && { plate_color: data.plate_color }),
    ...(data.speed != "" && { speed: data.speed }),
    ...(data.vehicle_color != "" && { vehicle_color: data.vehicle_color }),

  };
  const _renderViolationContent = () => {
    return (
      <div>
        {
          data.violation == "ANPR" && data.violation_code == "" && data.violation_code == ""
            ? _renderText("Không vi phạm")
            : _renderText(data.violation)
        }
        {_renderText(
          <>
            <div className="flex flex-col">
              <a href="#" onClick={handleOpenModal} className="text-blue-500 mt-2">
                Chi tiết
              </a>
            </div>
          </>
        )}
        <ViolationDetailsModal
          open={modalOpen}
          onClose={handleCloseModal}
          data_item={custom_traffic_data}
        />
      </div>
    );
  };

  return (
    <div className="w-full flex flex-row min-w-[1200px] table-row-custom items-center border-b-2 border-[#F8F8F8]">
      <div className="w-[60px] py-6 flex justify-center">
        {_renderText(index.toString())}
      </div>

      <div className="w-[10%] py-6 pr-3 flex justify-start break-all">
        <div style={{ marginRight: '10px' }}>{_renderText(data.license_plate)}</div>
        <CopyBtn text={data.license_plate} title="Biển số"/>
      </div>

      <div className="w-[8%] py-6 pr-3 flex justify-start">
        {_renderText(data?.vehicle_type)}
      </div>
      <div className="w-[8%] py-6 pr-3 flex justify-start break-all">
        {_renderText(data?.brand_name)}
      </div>
      <div className="w-[8%] py-6 pr-3 flex justify-start break-all">
        {_renderText(data?.vehicle_color)}
      </div>

      <div className="w-[15%] py-6 pr-3 flex flex-col justify-start break-all">
        <div className="mb-2">{_renderText(data?.camera_name)}</div>
        <div>{_renderText(data?.camera_ip)}</div>
      </div>

      <div className="w-[11%] py-6 pr-3 flex flex-col justify-start">
        {
          <>
            <div className="mb-2">{_renderText(formatDateTime(data.timestamp, "DD/MM/yyyy"))}</div>
            <div>{_renderText(formatDateTime(data.timestamp, "HH:mm:ss"))}</div>
          </>
        }
      </div>
      <div className="w-[14%] py-3 pr-3 flex justify-start">
        <PreviewImage
            className="w-full h-[90px] relative  justify-start flex "
            src={data.crop_plate || "null"}
          >
          <ImageFallback
            src={data.crop_plate || "null"}
            fallbackSrc={"/images/logo-oryza.png"}
            width={160}
            height={90}
            alt={"Hình ảnh biển số"}
            style={{
              objectFit: "contain",
              background: "#CFD3D8",
              maxWidth: "160px", // Set a maximum width
              maxHeight: "90px", // Set a maximum height
            }}
          />
        </PreviewImage>
      </div>
      <div className="w-[14%] py-3 pr-3 flex justify-start">
        {/* <Stack
          sx={{
            "& .magnify-handler ": {
              "& .magnify-box ": {
                position: "absolute !important",
                left: "auto !important",
                top: index <= 2 ? "0 !important" : "auto !important",
                bottom: index <= 2 ? "auto !important" : "0 !important",
                right: "calc(100% + 16px) !important",
                "& .magnify-image": {
                  maxWidth: "unset",
                },
                zIndex: 999999999,
                maxWidth: "unset !important",
                // transform:
                //   index <= 2
                //     ? "translate(-100% , 100%) scale(2.0) !important"
                //     : "translate(-100% , -100%) scale(2.0) !important",
              },
            },
          }}
        >
          {data?.full_img ? (
            <div className="max-w-[150px]">
              <ImageMagnifyComponent
                src={data?.full_img as string}
                alt={"full image"}
              />
            </div>
          ) : (
            <ImageFallback
              src={"null"}
              fallbackSrc={"/images/logo-oryza.png"}
              width={160}
              height={90}
              alt={"Hình ảnh ghi nhận"}
              style={{
                objectFit: "contain",
                background: "#CFD3D8",
              }}
            />
          )}
        </Stack> */}
        <PreviewImage
          className="w-full h-[90px] relative  justify-start flex "
          src={data.full_img || "null"}
        >
          <ImageFallback
            src={data.full_img || "null"}
            fallbackSrc={"/images/logo-oryza.png"}
            width={160}
            height={90}
            alt={"Hình ảnh ghi nhận"}
            style={{
              objectFit: "contain",
              background: "#CFD3D8",
            }}
          />
        </PreviewImage>
      </div>
      <div className="w-[12%] py-6 pr-3 flex justify-start">
        {_renderViolationContent()}
      </div>
    </div>
  );
}

function formatDateTime(date: any, format: string) {
  const momentDate = moment(date);
  if (momentDate.isValid()) {
    return momentDate.format(format);
  } else {
    return "--";
  }
}