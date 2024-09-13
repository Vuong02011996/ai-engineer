import { cameraApi } from "@/api-client/camera";
import { personApi } from "@/api-client/identification-profile/person";
import { personCameraApi } from "@/api-client/identification-profile/person-camera";
import { MainHead } from "@/components";
import {
  EmptyData,
  Loading,
  OpactityAnimation,
  SeoPage,
} from "@/components/common";
import Scrollbar from "@/components/common/scrollbar";
import { IdentificationUserDialog } from "@/components/dialog/create-identification-user";
import { CreateMultipleCameraPerson } from "@/components/dialog/create-multiple-camera-user";
import { HeadContent } from "@/components/head/content-head";
import { FilterSmallIcon } from "@/components/popup/filter/filter-small-icon";
import { TableHead } from "@/components/table";
import { ResultEnum } from "@/constants/enum";
import { CameraBtn } from "@/containers/identification-profile/ui/camera-btn";
import { UserSlugTableItem } from "@/containers/identification-profile/user/table-slug-item";
import { headSlugData } from "@/data/identification-profile";
import { filterCameraByPerson } from "@/data/identification-profile/filter-option";
import useHandleError from "@/hooks/useHandleError";
import { ICameraAI } from "@/interfaces/identification-profile/camera-ai";
import { IPerson } from "@/interfaces/identification-profile/person";
import HomeLayout from "@/layouts/home";
import { formatCameraAi, formatPerson } from "@/libs/format-data";
import { Stack } from "@mui/material";
import { useRouter } from "next/router";
import { useCallback, useEffect, useState } from "react";

export interface IUserIdentificationProfileSlugProps {}

export default function UserIdentificationProfileSlug(
  props: IUserIdentificationProfileSlugProps
) {
  const [openCreate, setOpenCreate] = useState(false);
  const handleError = useHandleError();
  const router = useRouter();
  const [person, setPerson] = useState<IPerson | null>(null);
  const [openAddAllDialog, setOpenAddAllDialog] = useState(false);
  const [data, setData] = useState<ICameraAI[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [listIdCamera, setListIdCamera] = useState<string[]>([]);
  const [filter, setFilter] = useState<"ALL" | "ON" | "OFF">("ALL");

  // * * * * * * * * SEARCH * * * * * * * * * *
  const [searchData, setSearchData] = useState<ICameraAI[]>([]);
  const [searchKey, setSearchKey] = useState("");
  // search by name & ip_address
  function handleSearch(searchKey: string) {
    return data.filter((item) => {
      const name = item.name.toLocaleLowerCase();
      const ip_address = item.ip_address.toLocaleLowerCase();
      const search = searchKey.toLocaleLowerCase();

      const searchName = name.includes(search);
      const searchIp = ip_address.includes(search);

      if (searchName || searchIp) return item;
    });
  }

  // * handle create function
  const handleCreate = async (formData: any) => {
    try {
      // call api
      return ResultEnum.success;
    } catch (error) {
      handleError(error, "Thêm mới hồ sơ nhận diện đối tượng không thành công");
      return ResultEnum.error;
    }
  };

  // * fetch data
  const fetchData = useCallback(async () => {
    setIsLoading(true);
    try {
      let { data } = await cameraApi.getCameraAi();
      let cameraPersonList = await getPersonByPersonId();
      const response = formatCameraAi(data, cameraPersonList);
      setData(response);
      return response;
    } catch (error) {
      return null;
    } finally {
      setIsLoading(false);
    }
  }, [router.query]);

  // * get person by id
  const getPersonById = useCallback(async () => {
    if (!router.query.slug) return;
    try {
      let { data } = await personApi.getById(router.query.slug as string);
      let response = formatPerson([data])[0];
      setPerson(response);
    } catch (error) {}
  }, [router.query]);

  //* get person by person id
  const getPersonByPersonId = async () => {
    if (!router?.query?.slug) return;
    try {
      const slug = router?.query?.slug as string;
      let { data } = await personCameraApi.getByPersonId(slug);

      setListIdCamera(data.map((i: any) => i.camera_id));
      return data;
    } catch (error) {
      return [];
    }
  };

  const [progress, setProgress] = useState(0);
  const [errorCount, setErrorCount] = useState(0);

  //* create multiple camera person
  const handleCreateMultipleCameraPerson = async () => {
    setProgress(0);
    setErrorCount(0);

    const presonId = router?.query?.slug;
    if (presonId) {
      personCameraApi
        .createMultipleCameraPerson(presonId as string)
        .then(async (res) => {
          await new Promise((r) => setTimeout(r, 1000));
          fetchData()
            .then((res) => {
              let count = 0;
              if (res) {
                for (const key in res) {
                  if (!listIdCamera.includes(res[key].id)) {
                    count++;
                  }
                }
              }
              setErrorCount(count);
            })
            .finally(() => {
              setProgress(100);
            });
        });
    }

    const interval = setInterval(() => {
      setProgress((prevProgress) => {
        if (prevProgress >= 90) {
          clearInterval(interval);
          return 90;
        } else {
          return prevProgress + 10;
        }
      });
    }, 100);
  };

  // *   useEffect
  useEffect(() => {
    fetchData();
    getPersonById();
  }, [fetchData]);

  //

  return (
    <section className="p-[24px] h-full">
      <SeoPage title="Nhận diện đối tượng" />
      {/* <SocketCameraPerson id={socketId} /> */}
      <MainHead
        searchValue={searchKey}
        onChange={(e) => {
          setSearchKey(e);
          if (data.length <= 0) return;
          const searchData = handleSearch(e.trim());

          setSearchData(searchData);
        }}
      />

      <div className="h-calc50 shadow-shadown1 rounded-[16px] relative">
        {/* table title */}
        <HeadContent
          title={"Camera nhận diện"}
          tabIndex={"1"}
          handleChangeTab={(tab) => {
            if (router.pathname != tab.path) router.push(tab.path);
          }}
          hiddenCreateBtn
          hiddenUpdateBtn
          subTitleApostrophe={person?.name ?? ""}
          rootPage="/identification-profile/user"
        >
          <div className="flex flex-row items-center space-x-4 ">
            <Stack direction="row" alignItems="center" spacing={2}>
              <CameraBtn
                onClick={() => {
                  handleCreateMultipleCameraPerson();
                  setOpenAddAllDialog(true);
                }}
                status={"ON"}
              />
            </Stack>
            <div className="z-10">
              <FilterSmallIcon
                options={filterCameraByPerson}
                onChange={function (value: any): void {
                  setFilter(value);
                }}
              />
            </div>
          </div>
        </HeadContent>

        <OpactityAnimation className={"h-calc92"}>
          <div className="flex-1 h-full pt-2">
            <div className="h-full overflow-auto  ">
              <Scrollbar>
                <TableHead dataHead={headSlugData} />

                {isLoading ? (
                  <Loading />
                ) : (searchKey.length > 0 ? searchData : data)?.length === 0 ? (
                  <EmptyData />
                ) : (
                  (searchKey.length > 0 ? searchData : data).map(
                    (item: ICameraAI, index) => {
                      const isOn = listIdCamera.includes(item.id);
                      const shouldRenderItem =
                        filter === "ALL" ||
                        (filter === "ON" && isOn) ||
                        (filter === "OFF" && !isOn);

                      return shouldRenderItem ? (
                        <UserSlugTableItem
                          key={item.id}
                          data={item}
                          index={index + 1}
                          isOn={isOn}
                          reload={fetchData}
                        />
                      ) : null;
                    }
                  )
                )}
              </Scrollbar>
            </div>
          </div>
        </OpactityAnimation>
      </div>

      {/* create dialog */}
      <IdentificationUserDialog
        open={openCreate}
        handleClose={() => setOpenCreate(false)}
        submit={handleCreate}
      />

      {openAddAllDialog && (
        <CreateMultipleCameraPerson
          open={openAddAllDialog}
          handleClose={async () => {
            setOpenAddAllDialog(false);
            return ResultEnum.success;
          }}
          listIdCamera={listIdCamera}
          data={data}
          setListIdCamera={setListIdCamera}
          reload={fetchData}
          setData={setData}
          onCreate={handleCreateMultipleCameraPerson}
          loading={progress}
          errorCount={errorCount}
        />
      )}
    </section>
  );
}

UserIdentificationProfileSlug.Layout = HomeLayout;
