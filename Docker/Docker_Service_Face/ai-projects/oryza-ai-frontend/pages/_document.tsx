import { Html, Head, Main, NextScript } from "next/document";
import { useEffect } from "react";
const WEBSITE_URL = process.env.WEBSITE_URL;

export default function Document() {
  // Google Tag Manager
  useEffect(() => {
    (function (
      w: any,
      d: any,
      scriptTag: any,
      dataLayerName: any,
      containerId: any
    ) {
      w[dataLayerName] = w[dataLayerName] || [];
      w[dataLayerName].push({
        "gtm.start": new Date().getTime(),
        event: "gtm.js",
      });
      var firstScript = d.getElementsByTagName(scriptTag)[0];
      var scriptElement = d.createElement(scriptTag);
      scriptElement.async = true;
      scriptElement.src =
        "https://www.googletagmanager.com/gtm.js?id=" + containerId;
      firstScript.parentNode.insertBefore(scriptElement, firstScript);
    })(window, document, "script", "dataLayer", "G-22MJHQBV0S");
  }, []);
  return (
    <Html lang="vi">
      <Head>
        <link rel="stylesheet" href="/assets/css/lib/bootstrap-icons.css" />
        <link rel="stylesheet" href="/assets/css/lib/all.min.css" />
        <link rel="stylesheet" href="/assets/css/lib/animate.css" />
        <link rel="stylesheet" href="/assets/css/lib/bootstrap.min.css" />
        <link rel="stylesheet" href="/assets/css/style.css" />
        <link rel="stylesheet" href="/assets/css/rtl_style.css" />
        <meta
          name="copyright"
          content="Copyright ® oryza-ai.oryza.vn. All rights reserved"
        />
        <meta name="geo.region" content="VN" />
        <meta name="geo.placename" content="Bình Dương" />
        <meta name="geo.position" content="10.9588726;106.6943844" />
        <meta name="ICBM" content="0.9594605;106.6969003" />
        <meta property="og:locale" content="vi_VN" />
        <meta
          property="og:type"
          content="Oryza Systems Cung cấp mạng lưới đáp ứng mọi nhu cầu của bạn một cách dễ dàng và thú vị bằng cách sử dụng Oryza AI"
        />
        <meta property="og:url" content={WEBSITE_URL} />
        <meta property="og:site_name" content="Oryza Systems" />
        <meta
          property="article:modified_time"
          content={new Date().toISOString()}
        />
        <link rel="icon" type="image/x-icon" href="/favicon.ico"></link>

        <meta name="twitter:card" content="https://twitter.com/OryzaSystems" />
        <meta name="twitter:site" content="@OryzaSystems" />
        <meta name="twitter:title" content="Oryza Systems" />
        <meta
          name="twitter:description"
          content="Công ty cổ phần công nghệ Oryza Systems"
        />
        <meta
          name="twitter:image"
          content="https://twitter.com/OryzaSystems/photo"
        />
        <script
          dangerouslySetInnerHTML={{
            __html: `
                            (function(w,d,s,l,i){
                            w[l]=w[l]||[];
                            w[l].push({'gtm.start': new Date().getTime(),event:'gtm.js'});
                            var f=d.getElementsByTagName(s)[0],
                            j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';
                            j.async=true;
                            j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;
                            f.parentNode.insertBefore(j,f);
                            })(window,document,'script','dataLayer','G-22MJHQBV0S');
                        `,
          }}
        ></script>
      </Head>
      <body>
        <Main />
        <NextScript />
        <noscript>
          <iframe
            src="https://www.googletagmanager.com/ns.html?id=G-22MJHQBV0S"
            height="0"
            width="0"
            style={{ display: "none", visibility: "hidden" }}
          ></iframe>
        </noscript>
      </body>
    </Html>
  );
}
