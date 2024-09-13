export interface CameraCrowd {
  name: string;
  ip_address: string;
  port: number;
  username: string;
  password: string;
  rtsp: string;
  id: string;
  crowdData: CrowdAI | null;
  process_id?: string;
}

export interface CrowdAI {
  boundary: string;
  min_human_count: number;
  min_neighbours: number;
  waiting_time_to_start_alarm: number;
  waiting_time_for_next_alarm: number;
  distance_threshold: number;
  camera_id: string;
  image_url: string;
  id_company: string;
  created: Date;
  modified: Date;
  id: string;
}

export interface BrandCamera {
  id: string;
  key: string;
}

export interface OtherInfo {}
