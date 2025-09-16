import { useState, useEffect } from "react";
import { useDispatch } from "react-redux";
import { useRouter } from "next/navigation";

import Div from "@/baseComponents/reusableComponents/Div";
import Heading from "@/baseComponents/reusableComponents/Heading";
import TextBox from "@/baseComponents/formComponents/TextBox";
import CheckBox from "@/baseComponents/formComponents/CheckBox";
import Button from "@/baseComponents/reusableComponents/Button";
import Anchor from "@/baseComponents/reusableComponents/Anchor";
import Form from "@/baseComponents/formComponents/Form";
import GoogleAuth from "@/baseComponents/formComponents/GoogleAuth";

import LoginRegisterTemplate from "../shared/LoginRegisterTemplate";
import { PAGE_ROUTES } from "@/constants/pageRoutes";
import useApiCalls from "@/hooks/useApiCalls";
import { USER_LOGIN_API_ROUTE } from "@/constants/apiRoutes";
import { setLocalStorage } from "@/utils/storage";
import { setAccessToken } from "@/reducer/subs/accessToken";

import { formValidated } from "./validator";

const Login = () => {
  const dispatch = useDispatch();
  const router = useRouter();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [rememberMe, setRememberMe] = useState(true);

  // ----------------------------------------------------------------
  // ----------------------------------------------------------------
  const [loginUser, setLoginUser] = useState(false);
  const { status, data } = useApiCalls({
    method: "POST",
    url: USER_LOGIN_API_ROUTE,
    bodyData: {
      email,
      password,
      remember_me: rememberMe,
    },
    sendReq: loginUser,
    setSendReq: setLoginUser,
  });
  useEffect(() => {
    if (data?.access_token) {
      setLocalStorage("access_token", data.access_token);
      dispatch(setAccessToken(data.access_token));
      if (data?.refresh_token) {
        setLocalStorage("refresh_token", data.refresh_token);
      }

      if (data?.user && data?.user?.is_active) {
        router.push(PAGE_ROUTES.DASHBOARD);
      }
    }
  }, [data]);
  // ----------------------------------------------------------------
  // ----------------------------------------------------------------

  return (
    <>
      <LoginRegisterTemplate>
        <Heading type={1} className="text-center m-b-32">
          Sign In
        </Heading>
        <Form
          onSubmit={(e) => {
            if (formValidated(dispatch, email, password)) {
              setLoginUser(true);
            }
          }}
        >
          <Div className="width-per-100 m-b-16">
            <TextBox
              label={"Email"}
              placeHolder={"Enter your email address"}
              type={"email"}
              name={"email"}
              isRequired
              forceLightMode
              val={email}
              setVal={setEmail}
            />
          </Div>
          <Div className="width-per-100 m-b-16">
            <TextBox
              label={"Password"}
              placeHolder={"Enter your email address"}
              type={"password"}
              name={"password"}
              isRequired
              forceLightMode
              val={password}
              setVal={setPassword}
            />
          </Div>
          <Div className="width-per-100 m-b-16">
            <CheckBox
              label={"Remember me?"}
              val={rememberMe}
              setVal={setRememberMe}
            />
          </Div>
          <Div type="flex" hAlign="center" className="m-y-32 width-per-100">
            <Button btnText={"Sign In"} className="width-px-300" />
          </Div>
        </Form>
        <Div className="">
          <Div className="text-underline mouse-hand f-s-px-14">
            Forgot Password?
          </Div>
        </Div>
        <Div distributedBetween type="flex" className="m-b-16" vAlign="center">
          <Div
            className="width-per-45 bg-theme-two"
            style={{ height: "2px" }}
          />
          <Div className="f-s-px-12">OR</Div>
          <Div
            className="width-per-45 bg-theme-two"
            style={{ height: "2px" }}
          />
        </Div>
        <GoogleAuth />
        <Div type="flex" className="">
          <Anchor to={PAGE_ROUTES.REGISTER} anchorType="no-effect" internal>
            <Div className="text-underline m-t-16 text-center">
              Don't have an account yet? Create a new one!
            </Div>
          </Anchor>
        </Div>
      </LoginRegisterTemplate>
    </>
  );
};

export default Login;
