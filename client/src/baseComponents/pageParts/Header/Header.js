import cx from "classnames";

import Div from "@/baseComponents/reusableComponents/Div";

import styles from "./Header.module.scss";

const Header = () => {
  return (
    <>
      <Div className={cx("bg-red", styles.container)}>Header</Div>
    </>
  );
};

export default Header;
