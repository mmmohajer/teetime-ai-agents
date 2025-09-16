import { useEffect } from "react";
import { useRouter } from "next/router";
import { Provider } from "react-redux";
import Script from "next/script";
import { Open_Sans } from "next/font/google";

import { store } from "@/root/src/store";
import { IS_STAGING_OR_DEVELOPMENT, GA_TRACKING_ID } from "config";
import "../assets/styles/main.scss";

const openSans = Open_Sans({
  subsets: ["latin"],
  weight: ["400", "500", "700"],
  display: "swap",
});

const App = ({ Component, pageProps }) => {
  const router = useRouter();

  // Track route changes
  useEffect(() => {
    if (!IS_STAGING_OR_DEVELOPMENT) {
      const handleRouteChange = (url) => {
        if (window.gtag) {
          window.gtag("config", GA_TRACKING_ID, {
            page_path: url,
          });
        }
      };
      router.events.on("routeChangeComplete", handleRouteChange);
      return () => {
        router.events.off("routeChangeComplete", handleRouteChange);
      };
    }
  }, [router.events, IS_STAGING_OR_DEVELOPMENT]);

  return (
    <>
      {/* -------------------------------- */}
      {/* Google Analytics Integration */}
      {/* -------------------------------- */}
      {!IS_STAGING_OR_DEVELOPMENT && GA_TRACKING_ID ? (
        <>
          <Script
            strategy="afterInteractive"
            async
            src={`https://www.googletagmanager.com/gtag/js?id=${GA_TRACKING_ID}`}
          />
          <Script
            id="google-analytics"
            strategy="afterInteractive"
            dangerouslySetInnerHTML={{
              __html: `
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', '${GA_TRACKING_ID}', {
              page_path: window.location.pathname,
            });
          `,
            }}
          />
        </>
      ) : (
        ""
      )}

      <Script src="/scriptjanus.js" strategy="beforeInteractive" />
      <Script src="/adapter.js" strategy="beforeInteractive" />

      {/* -------------------------------- */}
      {/* Main App with Redux Provider */}
      {/* -------------------------------- */}
      <Provider store={store}>
        <Component className={openSans.className} {...pageProps} />
      </Provider>
    </>
  );
};

export default App;
