import { useState, useEffect, useRef } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useRouter } from "next/navigation";

import {
  setLocalStorage,
  getLocalStorage,
  removeLocalStorage,
} from "@/utils/storage";
import useApiCalls from "@/hooks/useApiCalls";
import {
  REFRESH_USER_ACCESS_TOKEN_API_ROUTE,
  PROFILE_API_ROUTE,
} from "@/constants/apiRoutes";
import { PAGE_ROUTES } from "@/constants/pageRoutes";
import { setProfile } from "@/reducer/subs/profile";
import { setAccessToken, clearAccessToken } from "@/reducer/subs/accessToken";

const BaseAppWrapper = ({ isAuthPage = false, children }) => {
  const dispatch = useDispatch();
  const router = useRouter();
  const profile = useSelector((state) => state.profile);
  const accessToken = useSelector((state) => state.accessToken);
  // --------------------------------------------------------
  // Authentication Handler
  // --------------------------------------------------------
  const refreshTokenRef = useRef("");
  const [showAuthPage, setShowAuthPage] = useState(false);
  useEffect(() => {
    if (typeof window !== "undefined") {
      if (getLocalStorage("refresh_token")) {
        const token = getLocalStorage("refresh_token");
        refreshTokenRef.current = token;
        if (isAuthPage) {
          router.push(PAGE_ROUTES.DASHBOARD);
        }
      } else {
        removeLocalStorage("access_token");
        dispatch(clearAccessToken());
        removeLocalStorage("refresh_token");
        if (!isAuthPage) {
          router.push(PAGE_ROUTES.LOGIN);
        }
        setShowAuthPage(true);
      }
    }
  }, []);

  const [refreshUserAccessToken, setRefreshUserAccessToken] = useState(false);
  const { status, data } = useApiCalls({
    method: "POST",
    url: REFRESH_USER_ACCESS_TOKEN_API_ROUTE,
    bodyData: {
      refresh_token: refreshTokenRef.current,
    },
    sendReq: refreshUserAccessToken,
    setSendReq: setRefreshUserAccessToken,
    showLoading: false,
    showErrerMessage: false,
    handleError: () => {
      removeLocalStorage("access_token");
      removeLocalStorage("refresh_token");
      if (!isAuthPage) {
        router.push(PAGE_ROUTES.LOGIN);
      }
    },
  });
  useEffect(() => {
    if (data?.access_token) {
      setLocalStorage("access_token", data.access_token);
      dispatch(setAccessToken(data.access_token));
    }
  }, [data]);
  useEffect(() => {
    if (refreshTokenRef?.current) {
      setRefreshUserAccessToken(true);
      const interval = setInterval(() => {
        setRefreshUserAccessToken(true);
      }, 5 * 60 * 1000);
      return () => clearInterval(interval);
    }
  }, [refreshTokenRef?.current]);
  // --------------------------------------------------------
  // --------------------------------------------------------

  const [getProfile, setGetProfile] = useState(false);
  const { status: profileReqStatus, data: profileReqData } = useApiCalls({
    method: "GET",
    url: PROFILE_API_ROUTE,
    sendReq: getProfile,
    setSendReq: setGetProfile,
    showErrerMessage: false,
    handleError: () => {
      removeLocalStorage("access_token");
      removeLocalStorage("refresh_token");
      if (!isAuthPage) {
        router.push(PAGE_ROUTES.LOGIN);
      }
    },
  });
  useEffect(() => {
    if (profileReqData?.id) {
      dispatch(setProfile(profileReqData));
    }
  }, [profileReqData]);
  useEffect(() => {
    if (accessToken && !profile?.id && !isAuthPage) {
      setGetProfile(true);
    }
  }, [accessToken]);
  // --------------------------------------------------------
  // --------------------------------------------------------
  return <>{children}</>;
};

export default BaseAppWrapper;
