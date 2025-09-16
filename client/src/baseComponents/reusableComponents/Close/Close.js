import cx from "classnames";

import Div from "@/baseComponents/reusableComponents/Div";
import Icon from "@/baseComponents/reusableComponents/Icon";

const Close = ({ bgColor, iconColor, ...props }) => {
  return (
    <>
      <Div
        type="flex"
        hAlign="center"
        vAlign="center"
        className={cx(
          "width-px-25 height-px-25 br-rad-per-50 pos-abs mouse-hand"
        )}
        style={{
          backgroundColor: bgColor || "gray",
          top: "8px",
          right: "8px",
          zIndex: 1000000000000000000,
        }}
        {...props}
      >
        <Icon type="close" scale={1} color={iconColor || "white"} />
      </Div>
    </>
  );
};

export default Close;
