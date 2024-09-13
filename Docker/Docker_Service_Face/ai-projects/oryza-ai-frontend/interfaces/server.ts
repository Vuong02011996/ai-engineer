import { InfoServer } from "@/models/redux.model";

export interface ServerRes {
  name: string;
  ip_address: string;
  is_alive: boolean;
  id: string;
  created: Date;
  modified: Date;
  count: number;
  serverInfo?: InfoServer;
}
