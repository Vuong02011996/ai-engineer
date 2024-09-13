export interface IPerson {
  name: string;
  company_id: string;
  other_info: OtherInfo;
  created: Date;
  modified: Date;
  is_delete: boolean;
  id: string;
  images: IImage[];
  idCameraPerson?: string;
}

export interface IImage {
  id: string;
  url: string;
  name: string;
}

export interface OtherInfo {
  gender: string;
  address: string;
}

export interface PersonCompanyCamera {
  id: string;
  name: string;
  created: Date;
  images: IImage[];
  is_supervision: boolean;
  other_info: OtherInfo;
  id_person_camera: string;
}
