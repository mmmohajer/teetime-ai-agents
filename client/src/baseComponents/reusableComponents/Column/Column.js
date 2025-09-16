import cx from "classnames";

import Div from "@/baseComponents/reusableComponents/Div";

const Column = ({
  xs = 12,
  sm = 12,
  md = 12,
  lg = 12,
  className,
  children,
  ...props
}) => {
  const getCssClass = (num, size) => {
    if (size === "xs") {
      return `row--${num}`;
    } else if (size === "sm") {
      return `row--sm--${num}`;
    } else if (size === "md") {
      return `row--md--${num}`;
    } else if (size === "lg") {
      return `row--lg--${num}`;
    }
  };

  return (
    <>
      <Div
        className={cx(
          "row",
          getCssClass(xs, "xs"),
          getCssClass(sm, "sm"),
          getCssClass(md, "md"),
          getCssClass(lg, "lg"),
          className
        )}
        {...props}
      >
        {children}
      </Div>
    </>
  );
};

export default Column;
