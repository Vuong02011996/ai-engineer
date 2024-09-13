export interface CameraTraffictDetection {
  id: string;
  name: string;
  rtsp: string;
  ip_address: string;
  port: number;
  username: string;
  password: string;
  setting: Setting;
  process_id?: string;
}

export interface Setting {
  created: Date;
  id_company: string;
  image_url: string;
  light_boundary: string;
  modified: Date;
  id: string;
}
