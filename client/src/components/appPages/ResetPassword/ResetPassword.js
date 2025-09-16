import { useState, useEffect } from "react";
import { useDispatch } from "react-redux";
import { useRouter } from "next/navigation";

import Div from "@/baseComponents/reusableComponents/Div";
import Heading from "@/baseComponents/reusableComponents/Heading";
import TextBox from "@/baseComponents/formComponents/TextBox";
import Form from "@/baseComponents/formComponents/Form";
import Button from "@/baseComponents/reusableComponents/Button";

import LoginRegisterTemplate from "../shared/LoginRegisterTemplate";

import useApiCalls from "@/hooks/useApiCalls";
import { USER_RESET_PASSWORD_API_ROUTE } from "@/constants/apiRoutes";
import { PAGE_ROUTES } from "@/constants/pageRoutes";
import { addNewAlertItem } from "@/utils/alert";

import { formValidated } from "./validator";

const ResetPassword = ({ token, email }) => {
  const dispatch = useDispatch();
  const router = useRouter();

  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  // ----------------------------------------------------------------
  // ----------------------------------------------------------------
  const [resetPassword, setResetPassword] = useState(false);
  const { status, data } = useApiCalls({
    method: "POST",
    url: USER_RESET_PASSWORD_API_ROUTE,
    bodyData: {
      token,
      email,
      password,
    },
    sendReq: resetPassword,
    setSendReq: setResetPassword,
  });
  useEffect(() => {
    if (data?.success) {
      addNewAlertItem(
        dispatch,
        "success",
        "Password reset successfully, and you can now login with the updated password!"
      );
      router.push(PAGE_ROUTES.LOGIN);
    }
  }, [data]);
  // ----------------------------------------------------------------
  // ----------------------------------------------------------------
  return (
    <>
      <LoginRegisterTemplate>
        <Heading type={1} className="text-center m-b-32">
          Reset Your Password
        </Heading>
        <Form
          onSubmit={(e) => {
            if (formValidated(dispatch, email, password, confirmPassword)) {
              setResetPassword(true);
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
              setVal={null}
              isNotEditable
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
            <TextBox
              label={"Confirm Password"}
              placeHolder={"Confirm Your Password"}
              type={"password"}
              name={"password"}
              isRequired
              forceLightMode
              val={confirmPassword}
              setVal={setConfirmPassword}
            />
          </Div>
          <Div type="flex" hAlign="center" className="m-y-32 width-per-100">
            <Button btnText={"Reset Password"} className="width-px-300" />
          </Div>
        </Form>
      </LoginRegisterTemplate>
    </>
  );
};

export default ResetPassword;
