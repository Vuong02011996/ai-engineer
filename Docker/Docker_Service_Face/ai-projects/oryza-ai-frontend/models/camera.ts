export interface CreateCamera {
  name: string;
  ip_address: string;
  port?: number;
  username: string;
  password: string;
  rtsp: string;
  // company_id: string;
  is_ai: boolean;
  brand_camera_id: string;
  type_service_ids: string[];
  other_info: any;
  ward_id: string;
}

export interface GenerateRTSP {
  address: string;
  port: number;
  username: string;
  password: string;
}
