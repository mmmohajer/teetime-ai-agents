import cx from "classnames";

import Div from "@/baseComponents/reusableComponents/Div";
import Icon from "@/baseComponents/reusableComponents/Icon";

import { COLORS } from "@/constants/vars";

const Type1 = ({ label, val, setVal, isRequired = false }) => {
  return (
    <>
      <Div type="flex" vAlign="center">
        <Div
          type="flex"
          hAlign="center"
          vAlign="center"
          onClick={() => setVal(!val)}
          className="width-px-30 height-px-30 bg-white br-all-solid-2 br-rad-px-5 br-theme-five mouse-hand"
        >
          {val ? (
            <Div
              type="flex"
              hAlign="center"
              vAlign="center"
              className="width-px-20 height-px-20"
            >
              <Icon type="check-mark" scale={1.5} color={COLORS["theme-two"]} />
            </Div>
          ) : (
            ""
          )}
        </Div>
        <Div
          className={cx(
            "m-l-8 f-s-px-14",
            isRequired ? "global-is-required" : ""
          )}
        >
          {label}
        </Div>
      </Div>
    </>
  );
};

export default Type1;
