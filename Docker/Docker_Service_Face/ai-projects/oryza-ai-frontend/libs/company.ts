import { CompanyRes } from "@/interfaces/company";

export function formatCompanyData(data: any) {
  let array: CompanyRes[] = data.map((camera: any) => {
    let item: CompanyRes = {
      name: camera?.name ?? "",
      domain: camera?.domain ?? "",
      id: camera?.id ?? "",
      created: camera?.created ?? new Date(),
      modified: camera?.modified ?? new Date(),
    };
    return item;
  });
  return array;
}
