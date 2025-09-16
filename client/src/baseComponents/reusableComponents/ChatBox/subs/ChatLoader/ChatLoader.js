import cx from "classnames";

import Div from "@/baseComponents/reusableComponents/Div";

import styles from "./ChatLoader.module.scss";

const ChatLoader = () => {
  return (
    <>
      <Div
        type="flex"
        hAlign="center"
        vAlign="center"
        className={cx(
          "width-px-70 height-px-50 bg-silver br-all-solid-1 br-rad-px-10",
          styles.chatLoader
        )}
      >
        <div className={styles.dots}>
          <span className={styles.dot}></span>
          <span className={styles.dot}></span>
          <span className={styles.dot}></span>
        </div>
      </Div>
    </>
  );
};

export default ChatLoader;
