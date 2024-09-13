import { Modal, Box, Typography } from '@mui/material';
import React, { ReactNode } from 'react';

type TrafficViolationKeys =
  | 'TRAFFIC_NOSEATBELT'
  | 'TRAFFIC_SMOKING'
  | 'TRAFFIC_NOHELMET'
  | 'TRAFFIC_CALLING'
  | 'TRAFFIC_OVERLINE'
  | 'TRAFFIC_RETROGRADE'
  | 'TRAFFIC_OVERYELLOWLINE'
  | 'TRAFFIC_WRONGROUTE'
  | 'TRAFFIC_TURNRIGHT'
  | 'TRAFFIC_DRIVINGONSHOULDER'
  | 'TRAFFIC_CROSSLANE'
  | 'TRAFFIC_RUNREDLIGHT'
  | 'TRAFFIC_TURNLEFT'
  | 'TRAFFIC_UTURN'
  | 'TRAFFIC_PEDESTRAINPRIORITY';

const errorName: Record<TrafficViolationKeys, string> = {
  'TRAFFIC_NOSEATBELT': 'Không đội mũ bảo hiểm',
  'TRAFFIC_SMOKING': 'Hút thuốc lá khi lái xe',
  'TRAFFIC_NOHELMET': 'Không đội mũ bảo hiểm',
  'TRAFFIC_CALLING': 'Sử dụng điện thoại khi lái xe',
  'TRAFFIC_OVERLINE': 'Lấn làn',
  'TRAFFIC_RETROGRADE': 'Đi ngược chiều',
  'TRAFFIC_OVERYELLOWLINE': 'Đè vạch vàng',
  'TRAFFIC_WRONGROUTE': 'Sai làn đường',
  'TRAFFIC_TURNRIGHT': 'Rẽ phải từ làn đường trái',
  'TRAFFIC_DRIVINGONSHOULDER': 'Lái xe trên lề đường',
  'TRAFFIC_CROSSLANE': 'Chuyển làn đường không đúng quy định',
  'TRAFFIC_RUNREDLIGHT': 'Vượt đèn đỏ',
  'TRAFFIC_TURNLEFT': 'Rẽ trái từ làn đường phải',
  'TRAFFIC_UTURN': 'Quay đầu xe trái chiều',
  'TRAFFIC_PEDESTRAINPRIORITY': 'Không nhường đường cho người đi bộ',
};

interface CustomEventData {
  violation?: string;
  violation_code?: string;
  traffic_code?: TrafficViolationKeys[];
  safe_belt?: string;
  calling?: string;
  smoking?: string;
  speed?: string;
  lane?: string;
  vehicle_color?: string;
  plate_color?: string;
  [key: string]: any;
}

interface ViolationDetailsModalProps {
  open: boolean;
  onClose: () => void;
  data_item: CustomEventData;
}

const ViolationDetailsModal: React.FC<ViolationDetailsModalProps> = ({ open, onClose, data_item }) => {
  const traffic_code = Array.isArray(data_item.traffic_code) ? data_item.traffic_code : [];
  const trafficViolations = traffic_code ? traffic_code.map(code => errorName[code]) : [];
  const _renderText = (text?: ReactNode) => <p className="font-medium text-grayOz text-sm" style={{ color: 'blue' }}>{text || ""}</p>;

  return (
    <Modal open={open} onClose={onClose}>
      <Box sx={{ width: 600, bgcolor: 'background.paper', p: 4, margin: 'auto', mt: '10%', borderRadius: 2 }}>
        <Typography variant="h6" component="h2">
          Thông tin chi tiết
        </Typography>
        {data_item.violation && (
          <>
            <Typography sx={{ mt: 2 }}>
              <strong>Vi phạm giao thông</strong>
            </Typography>
            <div style={{ marginLeft: '20px' }}>
              <Typography sx={{ mt: 2, display: 'flex', alignItems: 'center' }}>
                Tên sự kiện vi phạm: &nbsp; {data_item.violation !== "ANPR" ? _renderText(data_item.violation) : ""}
              </Typography>
              <Typography sx={{ mt: 2, display: 'flex', alignItems: 'center' }}>
                Mã vi phạm: &nbsp; {_renderText(data_item.violation_code)}
              </Typography>
              <Typography sx={{ mt: 2, display: 'flex', alignItems: 'center' }}>
                Các vi phạm khác: &nbsp;
                {trafficViolations.length > 0 ? (
                  <ul>
                    {trafficViolations.map((violation, index) => (
                      <li key={index} style={{ marginLeft: '20px' }}>{violation}</li>
                    ))}
                  </ul>
                ) : (
                  _renderText("Không có")
                )}
              </Typography>
            </div>
          </>
        )}
        <Typography sx={{ mt: 2, display: 'flex', alignItems: 'center' }}>
          <strong>Biển số:</strong>&nbsp;{_renderText(data_item.plate)}
        </Typography>
        <Typography sx={{ mt: 2, display: 'flex', alignItems: 'center' }}>
          <strong>Loại xe:</strong>&nbsp;{_renderText(data_item.vehicle_type)}
        </Typography>
        <Typography sx={{ mt: 2, display: 'flex', alignItems: 'center' }}>
          <strong>Hãng xe:</strong>&nbsp;{_renderText(data_item.brand_name)}
        </Typography>
        <Typography sx={{ mt: 2, display: 'flex', alignItems: 'center' }}>
          <strong>Màu xe:</strong>&nbsp;{_renderText(data_item.vehicle_color)}
        </Typography>
        <Typography sx={{ mt: 2, display: 'flex', alignItems: 'center' }}>
          <strong>Tốc độ:</strong>&nbsp;{_renderText(data_item.speed && data_item.speed !== "0" ? data_item.speed : "Không rõ")}
        </Typography>
        <Typography sx={{ mt: 2, display: 'flex', alignItems: 'center' }}>
          <strong>Làn đường:</strong>&nbsp;{_renderText(data_item.lane)}
        </Typography>
        <Typography sx={{ mt: 2, display: 'flex', alignItems: 'center' }}>
          <strong>Màu xe:</strong>&nbsp;{_renderText(data_item.vehicle_color)}
        </Typography>
        <Typography sx={{ mt: 2, display: 'flex', alignItems: 'center' }}>
          <strong>Màu biển số:</strong>&nbsp;{_renderText(data_item.plate_color)}
        </Typography>
      </Box>
    </Modal>
  );
};


export default ViolationDetailsModal;