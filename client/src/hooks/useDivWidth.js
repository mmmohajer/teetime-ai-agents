import { useState, useEffect, useRef } from "react";
import { useDispatch } from "react-redux";

import { setMainContainerWidth } from "@/reducer/subs/mainContainerWidth";

const useDivWidth = (isMainContainer = false) => {
  const dispatch = useDispatch();
  const containerRef = useRef(null);
  const [width, setWidth] = useState(0);

  const updateWidth = () => {
    if (containerRef?.current?.clientWidth) {
      if (!isMainContainer) {
        setWidth(containerRef.current.clientWidth);
      } else {
        try {
          dispatch(setMainContainerWidth(containerRef.current.clientWidth));
        } catch (e) {
          console.error(e);
        }
      }
    }
  };

  useEffect(() => {
    if (containerRef?.current) {
      updateWidth();
      window.addEventListener("resize", updateWidth);
      return () => window.removeEventListener("resize", updateWidth);
    }
  }, []);

  return { containerRef, width };
};

export default useDivWidth;
