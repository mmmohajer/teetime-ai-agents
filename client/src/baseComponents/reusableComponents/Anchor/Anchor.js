import cx from "classnames";
import Link from "next/link";

import Div from "@/baseComponents/reusableComponents/Div";

import styles from "./Anchor.module.scss";

const Anchor = ({
  anchorType = "scale",
  to,
  internal = true,
  target = "_blank",
  ariaLabel = "",
  className,
  children,
  ...props
}) => {
  return (
    <>
      {internal && (
        <Link
          href={to}
          {...(ariaLabel && { "aria-label": ariaLabel })}
          className={cx(
            "mouse-hand",
            anchorType === "scale" && styles.scale,
            anchorType === "internal-routing" &&
              "text-theme-two text-theme-three-on-hover",
            anchorType === "no-effect" && "",
            className
          )}
          {...props}
        >
          {children}
        </Link>
      )}
      {!internal && (
        <a
          className={cx(
            "mouse-hand",
            anchorType === "scale" && styles.scale,
            anchorType === "no-effect" && "",
            className
          )}
          href={to}
          target={target}
          {...(ariaLabel && { "aria-label": ariaLabel })}
          {...props}
        >
          {children}
        </a>
      )}
    </>
  );
};

export default Anchor;
