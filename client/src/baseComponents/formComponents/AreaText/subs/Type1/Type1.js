import cx from "classnames";

import Div from "@/baseComponents/reusableComponents/Div";
import Label from "@/baseComponents/formComponents/Label";

const Type1 = ({ label, placeHolder, isRequired = false, ...props }) => {
  return (
    <>
      <Label label={label} isRequired={isRequired} />
      <Div className="pos-rel width-per-100">
        <textarea
          {...props}
          placeholder={placeHolder}
          className={cx(
            "p-all-temp-3 br-rad-px-10  width-per-100 bg-white height-px-80"
          )}
          style={{ outline: "none" }}
        />
      </Div>
    </>
  );
};

export default Type1;
