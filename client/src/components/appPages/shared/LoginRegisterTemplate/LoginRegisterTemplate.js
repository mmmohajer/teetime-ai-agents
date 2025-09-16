import cx from "classnames";

import Div from "@/baseComponents/reusableComponents/Div";

import useDivWidth from "@/hooks/useDivWidth";

import DesktopView from "./subs/DesktopView";
import MobileView from "./subs/MobileView";

const LoginRegisterTemplate = ({ children }) => {
  const { containerRef, width } = useDivWidth();
  return (
    <>
      <Div
        type="flex"
        direction="vertical"
        hAlign="center"
        vAlign="center"
        className="width-per-100 min-height-vh-full m-l-auto m-r-auto"
      >
        <Div className={cx("width-per-100 bg-white")} ref={containerRef}>
          {width >= 1000 ? (
            <Div className={""}>
              <DesktopView>{children}</DesktopView>
            </Div>
          ) : (
            <MobileView>{children}</MobileView>
          )}
        </Div>
      </Div>
    </>
  );
};

export default LoginRegisterTemplate;
