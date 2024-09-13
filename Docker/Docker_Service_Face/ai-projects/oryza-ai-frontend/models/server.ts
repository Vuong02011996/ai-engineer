import { StatusState } from "@/components/status/interface";

export interface ServerInterface {
  id: string;
  name: string;
  ip: string;
  status: StatusState;
  aiServiceNumber: number;
  cpu: SystemValue;
  ram: SystemValue;
  gpu: SystemValue;
  driveCapacity: SystemValue;
}

interface SystemValue {
  value: string;
  percent: number;
}

export interface CreateServer {
  name: string;
  ip_address: string;
  is_alive?: boolean;
}
