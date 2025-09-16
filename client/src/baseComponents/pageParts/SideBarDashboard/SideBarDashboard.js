import cx from "classnames";
import { useDispatch, useSelector } from "react-redux";

import Div from "@/baseComponents/reusableComponents/Div";

import { toggleSideBarDashboard } from "@/reducer/subs/sideBarDashboardIsActive";

const SideBarDashboard = () => {
  const dispatch = useDispatch();
  const sideBarDashboardIsActive = useSelector(
    (state) => state.sideBarDashboardIsActive
  );

  return (
    <>
      <Div
        className={cx(
          "height-vh-full br-right-solid-2 br-black p-all-16 of-y-auto global-transition-one of-x-hidden",
          sideBarDashboardIsActive ? "width-px-250" : "width-px-80"
        )}
      >
        <Div
          type="flex"
          hAlign="center"
          vAlign="center"
          className="bg-blue text-white mouse-hand p-all-4"
          onClick={() => dispatch(toggleSideBarDashboard())}
        >
          {">"}
        </Div>
      </Div>
    </>
  );
};

export default SideBarDashboard;
