interface Company {
    id: string;
    name: string;
  }
export interface UserRes {
    id: string;
    username: string;
    email: string;
    company: Company;
    email_validated: boolean;
    is_active: boolean;
    is_superuser: boolean;
    is_admin: boolean;
    created: string;
    modified: string;
    hash_password: string;
    avatar: string;
}

export interface UpdateUserForm {
  new_password: string;
  role: string;
}