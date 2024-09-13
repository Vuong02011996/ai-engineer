export interface ProcessEvent {
  camera?: Camera;
  status?: string;
  isEnable?: boolean;
  service?: Service;
  pid?: string;
  id_type_service?: string;
  company?: Company;
  created?: Date;
  modified?: Date;
  id?: string;
  is_debug?: boolean;
}

export interface Camera {
  name?: string;
  ip_address?: string;
  port?: number;
  username?: string;
  password?: string;
  rtsp?: string;
  company?: Company;
  brand_camera?: BrandCamera;
  is_ai?: boolean;
  other_info?: any;
  created?: Date;
  modified?: Date;
  id?: string;
}

export interface BrandCamera {
  name?: string;
  key?: string;
  created?: Date;
  modified?: Date;
  id?: string;
}

export interface Company {
  name?: string;
  domain?: string;
  created?: Date;
  modified?: Date;
  deleted?: null;
  id?: string;
}

export interface Service {
  name?: string;
  port?: string;
  is_alive?: boolean;
  max_process?: number;
  type_service?: BrandCamera;
  server?: Server;
  type?: string;
  created?: Date;
  modified?: Date;
  id?: string;
}

export interface Server {
  name?: string;
  ip_address?: string;
  is_alive?: boolean;
  created?: Date;
  modified?: Date;
  id?: string;
}
