import SnackbarProviderCustom from "@/components/common/snackbar/snackbar-provider";
import { AppPropsWithLayout } from "@/interfaces/common";
import MainLayout from "@/layouts/main";
import "@/styles/globals.css";
import "@/styles/tooltip.css";
import "@/styles/fonts.css";
import "@/styles/loading.css";
import "@/styles/tailwind.css";
import "@/styles/color-picker.css";
import "@/styles/custom.css";
import "@fontsource/roboto/300.css";
import "@fontsource/roboto/400.css";
import "@fontsource/roboto/500.css";
import "@fontsource/roboto/700.css";
import { Router } from "next/router";
import nProgress from "nprogress";
import "nprogress/nprogress.css";
import { SWRConfig } from "swr";
import axiosClient from "@/helper/call-center";
import store from "@/store/store";
import { Provider } from "react-redux";
// Import Swiper styles
import "swiper/css";
import "swiper/css/effect-cards";
import "swiper/css/effect-cube";
import "swiper/css/pagination";
import { useLocalStorage } from "@mantine/hooks";
import { useEffect } from "react";

export default function App({ Component, pageProps }: AppPropsWithLayout) {
  const Layout = Component.Layout ?? MainLayout;

  Router.events.on("routeChangeStart", nProgress.start);
  Router.events.on("routeChangeError", nProgress.done);
  Router.events.on("routeChangeComplete", nProgress.done);

  const [theme, setTheme] = useLocalStorage({
    key: "color-scheme",
    defaultValue: "",
  });
  useEffect(() => {
    document.querySelector("html")?.setAttribute("data-theme", theme);
  }, [theme]);

  return (
    <SWRConfig
      value={{
        fetcher: (url: string) => axiosClient.get(url),
        revalidateOnFocus: true,
        revalidateOnReconnect: true,
      }}
    >
      <Provider store={store}>
        <SnackbarProviderCustom>
          <Layout>
            <Component {...pageProps} />
          </Layout>
        </SnackbarProviderCustom>
      </Provider>
    </SWRConfig>
  );
}
