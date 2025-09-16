import cx from "classnames";

import Div from "@/baseComponents/reusableComponents/Div";

import styles from "./MobileView.module.scss";

const MobileView = ({ children }) => {
  return (
    <>
      <Div className="width-per-100 bg-white text-theme-one">
        <Div className={cx("width-per-100 p-all-temp-7", styles.imgContainer)}>
          {children}
        </Div>
      </Div>
    </>
  );
};

export default MobileView;
