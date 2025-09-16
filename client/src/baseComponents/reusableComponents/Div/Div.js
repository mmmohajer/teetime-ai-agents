import React from "react";
import cx from "classnames";

import { showInCssClass } from "./utils";

const Div = React.forwardRef(
  (
    {
      children,
      type = "block",
      direction = "horizontal",
      hAlign = "start",
      vAlign = "start",
      textAlign = "left",
      distributedBetween = false,
      distributedAround = false,
      showIn = ["xs", "sm", "md", "lg"],
      className,
      ...props
    },
    ref
  ) => {
    return (
      <>
        <div
          className={cx(
            type === "flex" && "flex",
            direction === "vertical" && "flex--dir--col",
            direction === "vertical" &&
              hAlign === "center" &&
              "flex--ai--center",
            direction !== "vertical" &&
              hAlign === "center" &&
              "flex--jc--center",
            direction === "vertical" && hAlign === "end" && "flex--ai--end",
            direction !== "vertical" && hAlign === "end" && "flex--jc--end",
            direction === "vertical" &&
              vAlign === "center" &&
              "flex--jc--center",
            direction !== "vertical" &&
              vAlign === "center" &&
              "flex--ai--center",
            direction === "vertical" && vAlign === "end" && "flex--jc--end",
            direction !== "vertical" && vAlign === "end" && "flex--ai--end",
            distributedBetween && "flex--jc--between",
            distributedAround && "flex--jc--around",
            textAlign === "center" && "text-center",
            textAlign === "right" && "text-rtl",
            showIn && showInCssClass(type, showIn),
            className
          )}
          {...props}
          ref={ref}
        >
          {children}
        </div>
      </>
    );
  }
);

export default Div;
