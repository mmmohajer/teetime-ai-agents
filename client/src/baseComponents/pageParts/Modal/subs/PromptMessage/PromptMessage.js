import { useDispatch, useSelector } from "react-redux";

import Div from "@/baseComponents/reusableComponents/Div";
import Button from "@/baseComponents/reusableComponents/Button";

import { clearModal } from "@/reducer/subs/modal";

const PromptMessage = () => {
  const dispatch = useDispatch();
  const { message } = useSelector((state) => state.modal.props);

  return (
    <>
      <Div className="m-b-temp-8">{message}</Div>
      <Button
        btnText={"OK"}
        className={"width-px-200"}
        onClick={() => dispatch(clearModal())}
      />
    </>
  );
};

export default PromptMessage;
