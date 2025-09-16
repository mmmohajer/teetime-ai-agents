import cx from "classnames";

import Div from "@/baseComponents/reusableComponents/Div";

import styles from "./ImageLoader.module.scss";

const ImageLoader = ({ type = 1 }) => {
  return (
    <>
      {type === 1 && (
        <Div className="width-px-150 height-px-150">
          <Div className={cx(styles.loading)}></Div>
        </Div>
      )}
    </>
  );
};

export default ImageLoader;
