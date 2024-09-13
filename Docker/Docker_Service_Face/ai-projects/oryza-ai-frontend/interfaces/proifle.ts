export interface IProfile {
  full_name: string | null;
  username: string | null;
  email: string | null;
  email_validated: boolean;
  avatar: string;
  is_active: boolean;
  is_superuser: boolean;
  company: {
    id: string;
    name: string;
  };
  id: string | null;
  is_admin: boolean;
  password: boolean;
  created: Date;
  modified: Date;
}
