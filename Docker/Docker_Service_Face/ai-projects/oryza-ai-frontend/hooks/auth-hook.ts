import { authApi } from "@/api-client/index";
import useSWR from "swr";
import { PublicConfiguration } from "swr/_internal";
import { CookieStoreControl } from "./cookie-storage";
import { useCallback } from "react";
import { IProfile } from "@/interfaces/proifle";

const HORSE_TO_MILLISECOND = 3000;

const instance = CookieStoreControl.getInstance();

export function useAuth(options?: Partial<PublicConfiguration>) {
  const {
    data: payload,
    error,
    mutate,
  } = useSWR("/user/get/me", {
    dedupingInterval: HORSE_TO_MILLISECOND,
    revalidateOnFocus: true,
    ...options,
  });

  async function login(payload: { username: string; password: string }) {
    const {
      data: { access_token, expire },
    } = await authApi.login({
      username: payload.username,
      password: payload.password,
    });

    if (!access_token) {
      console.log("Tài khoản hoặc mật khẩu không chính xác");

      return false;
    }

    instance.token.set_access_token(access_token, expire);

    await mutate();

    // showSnackbarWithClose("Đăng nhập thành công", {
    //   variant: "success",
    // });
    console.log("Đăng nhập thành công");

    return true;
  }

  async function logout() {
    instance.token.remove_access_token();

    window.location.replace("/login");

    mutate({}, false);
  }

  const firstLoading = payload === undefined && error === undefined;

  const transfer_profile_with_roles = useCallback((): IProfile | null => {
    if (payload?.data) {
      let data: IProfile = payload.data;

      return data;
    } else {
      return null;
    }
  }, [payload?.data]);

  return {
    profile: transfer_profile_with_roles(),
    error,
    firstLoading,
    login,
    logout,
  };
}
