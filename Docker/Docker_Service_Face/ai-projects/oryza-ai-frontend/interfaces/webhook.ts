export interface WebhookRes {
  id: string;
  company: string;
  type_service: any;
  status: boolean;
  name: string;
  endpoint: string;
  created: Date;
  modified: Date;
  token: string;
  auth_type: string;
}
