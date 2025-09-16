import { useState, useEffect } from "react";
import { useDispatch } from "react-redux";
import { useRouter } from "next/navigation";

import Div from "@/baseComponents/reusableComponents/Div";
import Heading from "@/baseComponents/reusableComponents/Heading";

import LoginRegisterTemplate from "@/components/appPages/shared/LoginRegisterTemplate";

import useApiCalls from "@/hooks/useApiCalls";
import {
  USER_AUTH_WITH_GOOGLE_API_ROUTE,
  USER_LOGIN_WITH_GOOGLE_API_ROUTE,
} from "@/constants/apiRoutes";
import { PAGE_ROUTES } from "@/constants/pageRoutes";
import { setLocalStorage } from "@/utils/storage";
import { setAccessToken } from "@/reducer/subs/accessToken";

const AuthWithGoogle = ({ code }) => {
  const dispatch = useDispatch();
  const router = useRouter();

  const [googleAccessToken, setGoogleAccessToken] = useState("");
  const [idToken, setIdToken] = useState("");

  // ----------------------------------------------------------------
  // ----------------------------------------------------------------
  const [authenticateUser, setAuthenticateUser] = useState(false);
  const { status, data } = useApiCalls({
    method: "POST",
    url: USER_AUTH_WITH_GOOGLE_API_ROUTE,
    bodyData: {
      code,
    },
    sendReq: authenticateUser,
    setSendReq: setAuthenticateUser,
    handleError: () => {
      router.push(PAGE_ROUTES.LOGIN);
    },
  });
  useEffect(() => {
    if (code) {
      setAuthenticateUser(true);
    }
  }, [code]);
  useEffect(() => {
    if (data?.access_token && data?.id_token) {
      setGoogleAccessToken(data.access_token);
      setIdToken(data.id_token);
    } else if (data?.error) {
      router.push(PAGE_ROUTES.LOGIN);
    }
  }, [data]);
  // ----------------------------------------------------------------
  // ----------------------------------------------------------------

  // ----------------------------------------------------------------
  // ----------------------------------------------------------------
  const [loginUser, setLoginUser] = useState(false);
  const { status: loginStatus, data: loginData } = useApiCalls({
    method: "POST",
    url: USER_LOGIN_WITH_GOOGLE_API_ROUTE,
    bodyData: {
      access_token: googleAccessToken,
      id_token: idToken,
    },
    sendReq: loginUser,
    setSendReq: setLoginUser,
    handleError: () => {
      router.push(PAGE_ROUTES.LOGIN);
    },
  });
  useEffect(() => {
    if (googleAccessToken && idToken) {
      setLoginUser(true);
    }
  }, [googleAccessToken, idToken]);
  useEffect(() => {
    if (loginData?.refresh_token) {
      setLocalStorage("refresh_token", loginData.refresh_token);
      if (data?.access_token) {
        setLocalStorage("access_token", loginData.access_token);
        dispatch(setAccessToken(loginData.access_token));
      }
      if (loginData?.user && loginData?.user?.is_active) {
        router.push(PAGE_ROUTES.DASHBOARD);
      }
    }
  }, [loginData]);
  // ----------------------------------------------------------------
  // ----------------------------------------------------------------

  return (
    <>
      <LoginRegisterTemplate>
        <Div type="flex" direction="vertical" className="flex--grow--1">
          <Heading type={1} className="text-center m-b-32">
            Activate Your Account!
          </Heading>
          <Div
            type="flex"
            hAlign="center"
            vAlign="center"
            className="flex--grow--1 text-center"
          >
            Trying to authenticate your account, please wait...
          </Div>
        </Div>
      </LoginRegisterTemplate>
    </>
  );
};

export default AuthWithGoogle;
