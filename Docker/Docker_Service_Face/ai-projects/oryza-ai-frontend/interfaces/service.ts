export interface ServiceRes {
  id: string;
  name: string;
  port: string;
  is_alive: boolean;
  max_process: number;
  type_service: any;
  server: string;
  type: string;
  created: Date;
  modified: Date;
  count_process: number;
}
