import cx from "classnames";

import Div from "@/baseComponents/reusableComponents/Div";

const Label = ({ label, isRequired = false }) => {
  return (
    <>
      <Div
        className={cx(
          "m-b-2 f-s-px-14",
          isRequired ? "global-is-required" : ""
        )}
      >
        {label}
      </Div>
    </>
  );
};

export default Label;
