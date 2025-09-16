import cx from "classnames";

import Div from "@/baseComponents/reusableComponents/Div";
import Label from "@/baseComponents/formComponents/Label";
import Icon from "@/baseComponents/reusableComponents/Icon";

import Preview from "./subs/Preview";
import styles from "./Type1.module.scss";

const Type1 = ({
  label,
  isRequired,
  fileChangeHandler,
  src,
  setSrc,
  setFile,
  setFileName,
  inputFileField,
  setInitialSrc,
  previewer = "default",
  hasMarginBottom = true,
  className,
}) => {
  return (
    <>
      <Div className={cx("pos-rel", hasMarginBottom && "m-b-32", className)}>
        {label && <Label label={label} isRequired={isRequired} />}
        <Div type="flex" hAlign="start" vAlign="center" className={cx("")}>
          <label>
            <input
              type="file"
              onChange={fileChangeHandler}
              className="no-display"
              accept=".mp4,.webm,.ogg,.avi,.mkv,.flv,.wmv,.mov"
              ref={(el) => (inputFileField.current = el)}
            />
            <Div
              type="flex"
              hAlign="center"
              vAlign="center"
              className={cx(styles.iconContainer)}
              color="#ccc"
            >
              <Icon type="circle-play" color={"white"} scale={4} />
            </Div>
          </label>
          {previewer === "default" ? (
            <Preview
              src={src}
              setSrc={setSrc}
              setFile={setFile}
              setFileName={setFileName}
              inputFileField={inputFileField}
              setInitialSrc={setInitialSrc}
            />
          ) : (
            ""
          )}
        </Div>
      </Div>
    </>
  );
};

export default Type1;
