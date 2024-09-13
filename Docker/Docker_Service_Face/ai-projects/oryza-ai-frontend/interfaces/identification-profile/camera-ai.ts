export interface ICameraAI {
  brand_camera: BrandCamera;
  created: Date;
  ip_address: string;
  is_ai: boolean;
  modified: Date;
  name: string;
  other_info: any;
  password: string;
  port: number;
  rtsp: string;
  username: string;
  id: string;
  idCameraPerson?: string;
  type_camera?: string;
}

export interface BrandCamera {
  id: string;
  name: string;
  key: string;
}
