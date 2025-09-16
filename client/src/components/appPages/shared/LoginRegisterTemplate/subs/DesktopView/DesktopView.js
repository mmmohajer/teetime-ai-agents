import cx from "classnames";

import Div from "@/baseComponents/reusableComponents/Div";

import styles from "./DesktopView.module.scss";

const DesktopView = ({ children }) => {
  return (
    <>
      <Div type="flex" className="width-per-100 bg-white">
        <Div
          type="flex"
          hAlign="center"
          vAlign="center"
          className={cx("width-per-50", styles.imgContainer)}
        >
          <Div
            className="text-center text-theme-one f-s-px-32 max-width-px-250 f-b f-i text-upper-case"
            style={{ lineHeight: "64px" }}
          >
            Make Your Dreams Come True!
          </Div>
        </Div>
        <Div
          type="flex"
          direction="vertical"
          className="width-per-50 p-all-temp-7 height-vh-full of-y-auto"
        >
          <Div className="flex--shrink--0">{children}</Div>
        </Div>
      </Div>
    </>
  );
};

export default DesktopView;
