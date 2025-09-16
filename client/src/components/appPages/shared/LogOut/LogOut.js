import { useState, useEffect, useRef } from "react";
import { useDispatch } from "react-redux";
import { useRouter } from "next/navigation";

import Div from "@/baseComponents/reusableComponents/Div";

import { getLocalStorage, removeLocalStorage } from "@/utils/storage";
import useApiCalls from "@/hooks/useApiCalls";
import { USER_LOGOUT_API_ROUTE } from "@/constants/apiRoutes";
import { PAGE_ROUTES } from "@/constants/pageRoutes";
import { setProfile } from "@/reducer/subs/profile";
import { clearAccessToken } from "@/reducer/subs/accessToken";

const LogOut = ({ children, ...props }) => {
  const dispatch = useDispatch();
  const router = useRouter();

  const refreshTokenRef = useRef("");

  useEffect(() => {
    if (typeof window !== "undefined") {
      if (getLocalStorage("refresh_token")) {
        const token = getLocalStorage("refresh_token");
        refreshTokenRef.current = token;
      }
    }
  }, []);

  const [logOutUser, setLogOutUser] = useState(false);
  const { status, data } = useApiCalls({
    method: "POST",
    url: USER_LOGOUT_API_ROUTE,
    bodyData: {
      refresh_token: refreshTokenRef.current,
    },
    sendReq: logOutUser,
    setSendReq: setLogOutUser,
    showLoading: false,
    showErrerMessage: false,
    handleError: () => {
      removeLocalStorage("access_token");
      dispatch(clearAccessToken());
      removeLocalStorage("refresh_token");
      dispatch(setProfile({}));
      router.push(PAGE_ROUTES.LOGIN);
    },
  });
  useEffect(() => {
    if (data?.success) {
      removeLocalStorage("access_token");
      dispatch(clearAccessToken());
      removeLocalStorage("refresh_token");
      dispatch(setProfile({}));
      router.push(PAGE_ROUTES.LOGIN);
    }
  }, [data]);
  // --------------------------------------------------------
  // --------------------------------------------------------
  return (
    <>
      <Div
        className="width-per-100"
        onClick={() => setLogOutUser(true)}
        {...props}
      >
        {children}
      </Div>
    </>
  );
};

export default LogOut;
