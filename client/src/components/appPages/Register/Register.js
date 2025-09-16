import { useState, useEffect } from "react";
import { useDispatch } from "react-redux";

import Div from "@/baseComponents/reusableComponents/Div";
import Heading from "@/baseComponents/reusableComponents/Heading";
import TextBox from "@/baseComponents/formComponents/TextBox";
import SVGIcon from "@/baseComponents/reusableComponents/SVGIcon";
import Button from "@/baseComponents/reusableComponents/Button";
import Anchor from "@/baseComponents/reusableComponents/Anchor";
import GoogleAuth from "@/baseComponents/formComponents/GoogleAuth";
import Form from "@/baseComponents/formComponents/Form";

import { PAGE_ROUTES } from "@/constants/pageRoutes";
import useApiCalls from "@/hooks/useApiCalls";
import { USER_REGISTER_API_ROUTE } from "@/constants/apiRoutes";

import LoginRegisterTemplate from "../shared/LoginRegisterTemplate";

import { formValidated } from "./validator";
import { addNewAlertItem } from "@/utils/alert";
import { APP_DOMAIN_FOR_CLIENT_SIDE } from "config";

const Register = () => {
  const dispatch = useDispatch();

  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  // ----------------------------------------------------------------
  // ----------------------------------------------------------------
  const [registerUser, setRegisterUser] = useState(false);
  const { status, data } = useApiCalls({
    method: "POST",
    url: USER_REGISTER_API_ROUTE,
    bodyData: {
      first_name: firstName,
      last_name: lastName,
      email,
      password,
      redirect_url: `${APP_DOMAIN_FOR_CLIENT_SIDE}/app`,
    },
    sendReq: registerUser,
    setSendReq: setRegisterUser,
  });
  useEffect(() => {
    if (data?.id) {
      addNewAlertItem(
        dispatch,
        "success",
        "Account created successfully! Please check your email to activate your account."
      );
    }
  }, [data]);
  // ----------------------------------------------------------------
  // ----------------------------------------------------------------
  const handleSubmit = (e) => {
    if (
      formValidated(
        dispatch,
        firstName,
        lastName,
        email,
        password,
        confirmPassword
      )
    ) {
      setRegisterUser(true);
    }
  };

  return (
    <>
      <LoginRegisterTemplate>
        <Heading type={1} className="text-center m-b-32">
          Sign Up
        </Heading>

        <Form onSubmit={(e) => handleSubmit(e)}>
          <Div>
            <Div className="width-per-100 m-b-16">
              <TextBox
                label={"First Name"}
                placeHolder={"Enter your First Name"}
                type={"text"}
                name={"first_name"}
                isRequired
                forceLightMode
                val={firstName}
                setVal={setFirstName}
              />
            </Div>

            <Div className="width-per-100 m-b-16">
              <TextBox
                label={"Last Name"}
                placeHolder={"Enter your Last Name"}
                type={"text"}
                name={"last_name"}
                isRequired
                forceLightMode
                val={lastName}
                setVal={setLastName}
              />
            </Div>

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
                placeHolder={"Pick a strong password"}
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
                placeHolder={"Confirm your password"}
                type={"password"}
                name={"confirm_password"}
                isRequired
                forceLightMode
                val={confirmPassword}
                setVal={setConfirmPassword}
              />
            </Div>
          </Div>
          <Div type="flex" hAlign="center" className="m-y-32 width-per-100">
            <Button btnText={"Sign Up"} className="width-px-300" />
          </Div>
        </Form>

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
          <Anchor to={PAGE_ROUTES.LOGIN} anchorType="no-effect" internal>
            <Div className="text-underline m-t-16 text-center">
              Already have an account? Sign in to your account!
            </Div>
          </Anchor>
        </Div>
      </LoginRegisterTemplate>
    </>
  );
};

export default Register;
