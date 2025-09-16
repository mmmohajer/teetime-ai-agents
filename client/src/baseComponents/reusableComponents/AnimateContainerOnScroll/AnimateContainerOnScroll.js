import React, { useState, useEffect, useRef } from "react";
import cx from "classnames";
import { useSelector } from "react-redux";

import Div from "@/baseComponents/reusableComponents/Div";

const AnimateContainerOnScroll = ({
  className,
  activeClassName,
  children,
  ...props
}) => {
  const containerRef = useRef();
  const scrollPos = useSelector((state) => state.scrollPos);

  const [showAnimation, setShowAnimation] = useState(false);

  useEffect(() => {
    if (containerRef?.current) {
      if (
        containerRef.current.getBoundingClientRect().top - window.innerHeight <=
          0 &&
        !showAnimation
      ) {
        setShowAnimation(true);
      }
    }
  }, [scrollPos, containerRef, showAnimation]);

  return (
    <>
      <Div
        ref={(el) => (containerRef.current = el)}
        className={cx(className, showAnimation && activeClassName)}
        {...props}
      >
        {children}
      </Div>
    </>
  );
};

export default AnimateContainerOnScroll;
