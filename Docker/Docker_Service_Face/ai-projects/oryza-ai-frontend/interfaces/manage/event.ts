export interface EventData {
  event_id: string;
  uuid: string;
  user_id: string;
  timestamp: Date | null;
  image_url: string;
  camera_ip: string;
  name: string;
  camera_name?: string;

  vehicle_bounding_box?: any[];
  vehicle_type?: string;
  vehicle_color?: string;
  brand_name?: string;
  license_plate_bounding_boxes?: any[];
  license_plate?: string;

  total_people_detected?: string;
  crowd_members_count?: string;
  crowd_alert_threshold?: string;
  people_bounding_boxes?: string;

  full_img?: string;
  crop_plate?: string;

  // loitering
  start_time?: Date | null;
  end_time?: Date | null;
  image_start?: string;
  image_end?: string;
  duration_time?: number;
  track_id?: number;

  // uniform
  error_type?: number;

  // light traffict
  signal?: string;

  // illegal parking
  license_plate_url?: string;
  status?: string;
  violation?: string;
  violation_code?: string;
  traffic_code?: string;
  safe_belt?: string;
  calling?: string;
  smoking?: string;
  lane?: string;
  plate_color?: string;
  speed?: string;

  // obj attr
  object_type?: string;
  attributes?: string;
}
