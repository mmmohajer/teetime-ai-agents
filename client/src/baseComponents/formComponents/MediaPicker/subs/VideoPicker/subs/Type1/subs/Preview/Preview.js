import cx from "classnames";

import Div from "@/baseComponents/reusableComponents/Div";
import Close from "@/baseComponents/reusableComponents/Close";
import AppVideo from "@/baseComponents/reusableComponents/AppVideo";

import { COLORS } from "@/constants/vars";

import styles from "./Preview.module.scss";

const Preview = ({
  src,
  setFile,
  setSrc,
  setFileName,
  inputFileField,
  setInitialSrc,
}) => {
  return (
    <>
      {src && (
        <Div
          type="flex"
          direction="vertical"
          className={cx(
            "ml1 of-hidden width-px-100 height-px-100",
            styles.previewContainer
          )}
        >
          <Close
            barColor={COLORS.themeOne}
            barHeight="25px"
            iconScale={0.8}
            iconCircleSize="15px"
            onClick={() => {
              setFile("");
              setSrc("");
              setFileName("");
              if (setInitialSrc) {
                setInitialSrc("");
              }
              inputFileField.current.value = null;
            }}
          />
          <Div
            type="flex"
            hAlign="center"
            vAlign="center"
            className={cx("pos-rel width-per-100 height-px-70")}
          >
            <Div
              type="flex"
              hAlign="center"
              vAlign="center"
              className={cx(
                "pos-rel mouse-hand of-hidden",
                styles.imagePreviewContainer
              )}
            >
              <AppVideo src={src} width={90} height={60} />
            </Div>
          </Div>
        </Div>
      )}
    </>
  );
};

export default Preview;
