import cx from "classnames";

import Div from "@/baseComponents/reusableComponents/Div";

import styles from "./Loading.module.scss";

const Loading = () => {
  return (
    <>
      <Div
        type="flex"
        hAlign="center"
        vAlign="center"
        className={cx(
          "pos-fix pos-fix--lt width-per-100 height-vh-full loadingZIndex",
          styles.fullHeight
        )}
      >
        <Div className="width-px-150 height-px-150">
          <Div className={cx(styles.loading)}></Div>
        </Div>
      </Div>
    </>
  );
};

export default Loading;
