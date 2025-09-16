import { useState } from "react";
import cx from "classnames";
import Image from "next/legacy/image";

import Div from "@/baseComponents/reusableComponents/Div";

import useDivWidth from "@/hooks/useDivWidth";

import ImageLoader from "./subs/ImageLoader";
import styles from "./AppImage.module.scss";

const AppImage = ({
  type = 1,
  width = 0,
  height = 0,
  heightOverWidthAsprctRatio = 1,
  containerClassName = "",
  ...props
}) => {
  const { containerRef, width: containerWidth } = useDivWidth();

  const [loading, setLoading] = useState(true);

  return (
    <>
      <Div
        ref={containerRef}
        type="flex"
        className={cx("pos-rel", containerClassName)}
        style={{
          width: width ? width : containerWidth,
          height: height ? height : containerWidth * heightOverWidthAsprctRatio,
        }}
      >
        <Image
          width={width ? width : containerWidth}
          height={height ? height : containerWidth * heightOverWidthAsprctRatio}
          {...props}
          onLoad={() => setLoading(false)}
        />

        {loading && (
          <Div
            type="flex"
            hAlign="center"
            vAlign="center"
            className={cx("pos-abs pos-abs--center", styles.spinner)}
            style={{
              width: width ? width : containerWidth,
              height: height
                ? height
                : containerWidth * heightOverWidthAsprctRatio,
            }}
          >
            <ImageLoader type={type} />
          </Div>
        )}
      </Div>
    </>
  );
};

export default AppImage;
