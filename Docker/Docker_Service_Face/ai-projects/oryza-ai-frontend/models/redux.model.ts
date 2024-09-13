import { TypeServiceKey } from "@/constants/type-service";
import { EventData } from "@/interfaces/manage/event";

export interface EventSliceInterface {
  data: SocketEventData | null;
}
export interface ProcessSliceInterface {
  data: SocketProcessData | null;
}
export interface ServeSliceInterface {
  server: SocketServerData | null;
  service: SocketServerData | null;
  info_server: InfoServer | null;
}
export interface SocketEventData {
  type_service: TypeServiceKey;
  data: EventData;
  type?: string;
}
export interface SocketServerData {
  id: string;
  is_alive: true;
}
export interface InfoServer {
  id: string;
  ip: string;
  cpu_percent: number;
  ram_total: number;
  ram_used: number;
  ram_percent: number;
  disk_total: number;
  disk_used: number;
  disk_percent: number;
  current_freq_mhz: number;
  list_gpu: ListGPU[];
}

export interface ListGPU {
  gpu_id: number;
  gpu_name: string;
  gpu_load: number;
  gpu_memory_total: number;
  gpu_memory_used: number;
  gpu_memory_free: number;
  gpu_memory_utilization: number;
}

export interface SocketProcessData {
  id: string;
  status: string;
  socketId: string;
}
