import { vmsApi } from "@/api-client/setting/vms";
import { LoadingPopup } from "@/components/common/loading/loading-popup";
import TextFieldFormV2 from "@/components/common/text-field/text-field-form-v2";
import useHandleError from "@/hooks/useHandleError";
import { Validator } from "@/utils/validate";
import {
  Dispatch,
  FormEvent,
  SetStateAction,
  useState,
} from "react";
import { SucsessPopup } from "./success-popup";
import { VmsInterface } from "@/interfaces/vms";
import { ChooseVMSServerType } from "@/components/input-field/choose-vms-server-type";

export interface IIntegrationFromProps {
  data: VmsInterface | null;
  setData: Dispatch<SetStateAction<VmsInterface | null>>;
}

export function IntegrationFrom(props: IIntegrationFromProps) {
  const { data, setData } = props;

  const [loading, setLoading] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const handleError = useHandleError();
  const [formErr, setFormErr] = useState<any>({});

  //* validate
  const checkValidate = (formData: any) => {
    let hasError = false;

    let error = {
      ip_address: Validator.checkNotEmpty(formData["ip_address"] ?? ""),
      port: Validator.checkContainsOnlyNumbers(formData["port"] ?? ""),
      username: Validator.checkNotEmpty(formData["username"] ?? ""),
      password: Validator.checkNotEmpty(formData["password"] ?? ""),
      vms_type: Validator.checkNotEmpty(formData["vms_type"] ?? ""),
    };

    if (
      error.ip_address !== null ||
      error.port !== null ||
      error.username !== null ||
      error.password !== null ||
      error.vms_type !== null
    ) {
      hasError = true;
    }

    setFormErr(error);
    return !hasError;
  };

  // * on submit form
  const onSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    let formData = new FormData(event.currentTarget);
    const formJson = Object.fromEntries(formData.entries());

    if (!checkValidate(formJson)) return;

    if (data) {
      updateVms(formJson);
    } else {
      createVms(formJson);
    }
  };

  const createVms = async (formJson: any) => {
    setLoading(true);
    try {
      const payload = {
        ip_address: formJson.ip_address,
        port: formJson.port,
        username: formJson.username,
        password: formJson.password,
        vms_type: formJson.vms_type,
      };

      await vmsApi.create(payload);
      setIsSuccess(true);
    } catch (error) {
      handleError(error, "Kết nối vms không thành công");
      setIsSuccess(false);
    } finally {
      setLoading(false);
    }
  };

  const updateVms = async (formJson: any) => {
    setLoading(true);
    try {
      const payload = {
        ip_address: formJson.ip_address,
        port: formJson.port,
        username: formJson.username,
        password: formJson.password,
        vms_type: formJson.vms_type,
      };

      let { data } = await vmsApi.update(payload);
      setData(data);
      setIsSuccess(true);
    } catch (error) {
      handleError(error, "Cập nhật vms không thành công");
      setIsSuccess(false);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-8">
      <LoadingPopup open={loading} />
      <SucsessPopup
        open={isSuccess}
        handleClose={function (): void {
          setIsSuccess(false);
        }}
      />
      <form className="space-y-8" onSubmit={onSubmit}>
        <fieldset className="flex flex-col ">
          <legend className="text-primary text-[20px] font-medium pb-3">
            Thông tin VMS Server
          </legend>
          <div className="flex flex-row space-x-[24px] ">
            <TextFieldFormV2
              name="ip_address"
              label="Địa chỉ HTTP Server"
              required
              sx={{ width: "60%" }}
              textError={formErr["ip_address"]}
              defaultValue={data?.ip_address}
              key={"RANDOM_KEY" + (10000 + Math.random() * (1000000 - 10000))}
            />
            <TextFieldFormV2
              name="port"
              label="Server Port"
              required
              type="number"
              sx={{ width: "40%" }}
              textError={formErr["port"]}
              defaultValue={data?.port}
              key={"RANDOM_KEY" + (10000 + Math.random() * (1000000 - 10000))}
            />
            <ChooseVMSServerType
              name="vms_type"
              label="Loại VMS Server"
              required
              defaultValue={data?.vms_type}
              textError={formErr["vms_type"]}
            />
          </div>
          
        </fieldset>
        <fieldset className="flex flex-col">
          <legend className="text-primary text-[20px] font-medium pb-3">
            Thông tin tài khoản Oryza VMS Server
          </legend>
          <div className="flex flex-row space-x-[24px] ">
            <TextFieldFormV2
              name="username"
              label="Tên đăng nhập"
              required
              sx={{ width: "100%" }}
              textError={formErr["username"]}
              defaultValue={data?.username}
              key={"RANDOM_KEY" + (10000 + Math.random() * (1000000 - 10000))}
            />
            <TextFieldFormV2
              name="password"
              label="Mật khẩu"
              required
              sx={{ width: "100%" }}
              textError={formErr["password"]}
              defaultValue={data?.password}
              key={"RANDOM_KEY" + (10000 + Math.random() * (1000000 - 10000))}
              type="password"
            />
          </div>
        </fieldset>
        <div className="flex justify-end ">
          <button
            type="submit"
            className="min-w-[100px] shadow-shadown1 bg-primary rounded-lg px-[14px] py-2 capitalize text-white font-semibold text-sm hover:bg-primaryDark"
          >
            Kết nối
          </button>
        </div>
      </form>
    </div>
  );
}
