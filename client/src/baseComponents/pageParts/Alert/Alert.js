import { useDispatch, useSelector } from "react-redux";
import cx from "classnames";

import Div from "@/baseComponents/reusableComponents/Div";
import Close from "@/baseComponents/reusableComponents/Close";

import { removeAnAlertItem } from "@/utils/alert";
import { COLORS } from "@/constants/vars";

const Alert = () => {
  const dispatch = useDispatch();
  const alert = useSelector((state) => state.alert);

  return (
    <>
      <Div
        className="pos-fix pos-fix--rt width-per-80 max-width-px-700"
        style={{ zIndex: 100000000000000000 }}
      >
        {alert?.map((item, idx) => (
          <Div
            type="flex"
            direction="vertical"
            key={item?.key}
            className={cx(
              "bg-white br-all-solid-3 p-all-temp-4 br-rad-px-10 pos-rel m-b-8 global-transition-one m-l-auto of-hidden width-per-100",
              item?.type === "success" ? "br-green" : "",
              item?.type === "error" ? "br-red" : ""
            )}
            style={{ right: item?.display ? "0px" : "-100%" }}
          >
            {item?.message}
            <Close
              onClick={() => {
                removeAnAlertItem(dispatch, item?.key);
              }}
              bgColor={
                item?.type === "success"
                  ? COLORS["theme-six"]
                  : item?.type === "error"
                  ? "red"
                  : "gray"
              }
              iconColor={"white"}
            />
          </Div>
        ))}
      </Div>
    </>
  );
};

export default Alert;
