import { CameraRes } from "./camera";
import { ServiceRes } from "./service";

export interface PorcessRes {
  camera: any;
  service: ServiceRes;
  status: string;
  id: string;
  created: Date;
  modified: Date;
  isEnable: boolean;
  is_debug: boolean;
}
