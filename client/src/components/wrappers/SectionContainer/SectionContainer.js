import cx from "classnames";

import Div from "@/baseComponents/reusableComponents/Div";
import Heading from "@/baseComponents/reusableComponents/Heading";

const SectionContainer = ({
  title,
  children,
  isFullwidth = false,
  hasPadding = true,
  hasMargin = true,
}) => {
  return (
    <>
      <Div
        className={cx(
          !isFullwidth ? "global-container" : "width-per-100",
          hasPadding ? "p-x-32" : "",
          hasMargin ? "m-b-32" : ""
        )}
      >
        {title?.length ? (
          <Div className="f-b m-y-32">
            <Heading type={3}>{title}</Heading>
          </Div>
        ) : null}
        <Div className="width-per-100">{children}</Div>
      </Div>
    </>
  );
};

export default SectionContainer;
