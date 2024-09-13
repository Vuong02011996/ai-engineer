import { ServerRes } from "@/interfaces/server";

export function formatServerData(data: any) {
  let array: ServerRes[] = data.map((camera: ServerRes) => {
    let item: ServerRes = {
      name: camera?.name ?? "",
      ip_address: camera?.ip_address ?? "",
      is_alive: camera?.is_alive ?? false,
      id: camera?.id ?? "",
      created: camera?.created ?? new Date(),
      modified: camera?.modified ?? new Date(),
      count: camera?.count ? Number(camera?.count) : 0,
    };
    return item;
  });
  return array;
}
