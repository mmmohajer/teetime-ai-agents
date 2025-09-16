import { useState, useEffect } from "react";
import { useDispatch } from "react-redux";
import { useRouter } from "next/navigation";

import Div from "@/baseComponents/reusableComponents/Div";
import Heading from "@/baseComponents/reusableComponents/Heading";

import LoginRegisterTemplate from "../shared/LoginRegisterTemplate";

import useApiCalls from "@/hooks/useApiCalls";
import { USER_ACTIVATE_ACCOUNT_API_ROUTE } from "@/constants/apiRoutes";
import { PAGE_ROUTES } from "@/constants/pageRoutes";
import { setLocalStorage } from "@/utils/storage";
import { setAccessToken } from "@/reducer/subs/accessToken";

const ActivateUser = ({ token, redirectUrl }) => {
  const dispatch = useDispatch();
  const router = useRouter();
  // ----------------------------------------------------------------
  // ----------------------------------------------------------------
  const [activateUser, setActivateUser] = useState(false);
  const { status, data } = useApiCalls({
    method: "PUT",
    url: USER_ACTIVATE_ACCOUNT_API_ROUTE,
    bodyData: {
      token,
    },
    sendReq: activateUser,
    setSendReq: setActivateUser,
    handleError: () => {
      router.push(PAGE_ROUTES.LOGIN);
    },
  });
  useEffect(() => {
    if (token) {
      setActivateUser(true);
    }
  }, [token]);
  useEffect(() => {
    if (data?.refresh_token) {
      setLocalStorage("refresh_token", data.refresh_token);
      if (data?.access_token) {
        setLocalStorage("access_token", data.access_token);
        dispatch(setAccessToken(data.access_token));
      }
      if (data?.user && data?.user?.is_active) {
        let localRedirectUrl = redirectUrl || PAGE_ROUTES.DASHBOARD;
        router.push(localRedirectUrl);
      }
    }
  }, [data]);
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
            Trying to activate your account, please wait...
          </Div>
        </Div>
      </LoginRegisterTemplate>
    </>
  );
};

export default ActivateUser;
