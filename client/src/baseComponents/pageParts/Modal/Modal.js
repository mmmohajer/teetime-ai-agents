import { useDispatch, useSelector } from "react-redux";
import cx from "classnames";

import Div from "@/baseComponents/reusableComponents/Div";
import Icon from "@/baseComponents/reusableComponents/Icon";

import { COLORS } from "@/constants/vars";
import { clearModal } from "@/reducer/subs/modal";

import PromptMessage from "./subs/PromptMessage";
import styles from "./Modal.module.scss";

const Modal = () => {
  const dispatch = useDispatch();
  const { type } = useSelector((state) => state.modal);
  return (
    <>
      <Div className={cx("pos-fix br-rad-px-10 p-b-temp-8", styles.container)}>
        <Div className="width-per-100 height-px-40 pos-rel">
          <Div
            type="flex"
            hAlign="center"
            vAlign="center"
            className="pos-abs bg-theme-five width-px-30 height-px-30 br-rad-per-50 mouse-hand"
            style={{ top: "5px", right: "10px" }}
            onClick={() => dispatch(clearModal())}
          >
            <Icon type="close" color={COLORS["theme-one"]} />
          </Div>
        </Div>
        <Div className="p-x-temp-8">
          {type === "prompt-message" ? <PromptMessage /> : ""}
        </Div>
      </Div>
    </>
  );
};

export default Modal;
