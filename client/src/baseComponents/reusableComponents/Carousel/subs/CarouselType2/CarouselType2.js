import { useState, useEffect } from "react";
import cx from "classnames";

import Div from "@/baseComponents/reusableComponents/Div";
import Icon from "@/baseComponents/reusableComponents/Icon";

import useDivWidth from "@/hooks/useDivWidth";
import { COLORS } from "@/constants/vars";

import styles from "./CarouselType2.module.scss";

const CarouselType2 = ({
  itemWidth,
  gapBetweenItems,
  numberOfItems,
  children,
}) => {
  const { containerRef, width } = useDivWidth();

  const [curSlideNum, setCurSlideNum] = useState(1);
  const [hasAnim, setHasAnim] = useState(false);
  const [numberOfSlides, setNumberOfSlides] = useState(1);
  const [itemsHolderWidth, setItemsHolderWidth] = useState(0);
  const [totalWidth, setTotalWidth] = useState(0);
  const [translateX, setTranslateX] = useState(0);

  useEffect(() => {
    if (width && itemWidth) {
      const numOfItems = Math.min(parseInt(width / itemWidth), numberOfItems);
      const holderWidth =
        numOfItems * itemWidth + (numOfItems - 1) * gapBetweenItems;
      if (holderWidth > width) {
        setItemsHolderWidth(
          (numOfItems - 1) * itemWidth + (numOfItems - 2) * gapBetweenItems
        );
      } else {
        setItemsHolderWidth(holderWidth);
      }
    }
  }, [width, itemWidth]);

  useEffect(() => {
    if (itemWidth && gapBetweenItems && numberOfItems) {
      setTotalWidth(
        itemWidth * numberOfItems + (numberOfItems - 1) * gapBetweenItems
      );
    }
  }, [itemWidth, gapBetweenItems, numberOfItems]);

  useEffect(() => {
    setNumberOfSlides(Math.ceil(totalWidth / itemsHolderWidth));
  }, [totalWidth, itemsHolderWidth]);

  useEffect(() => {
    let curTranslateX =
      (curSlideNum - 1) * itemsHolderWidth +
      (curSlideNum - 2) * gapBetweenItems;
    // if (curTranslateX > totalWidth - itemsHolderWidth) {
    //   curTranslateX = totalWidth - itemsHolderWidth;
    // }
    setTranslateX(curTranslateX);
  }, [curSlideNum, itemsHolderWidth, gapBetweenItems]);

  useEffect(() => {
    if (totalWidth > itemsHolderWidth) {
      const interval = setInterval(() => {
        let localCurSlideNum = curSlideNum + 1;
        setCurSlideNum(localCurSlideNum);
        if (localCurSlideNum > numberOfSlides) {
          setTimeout(() => {
            setCurSlideNum(1);
          }, 300);
        }
      }, 5000);

      return () => {
        clearInterval(interval);
      };
    }
  }, [totalWidth, itemsHolderWidth, curSlideNum, numberOfSlides]);

  return (
    <>
      <Div ref={containerRef} className="width-per-100">
        <Div
          style={{ maxWidth: `${itemsHolderWidth}px` }}
          className="width-per-100 of-hidden m-l-auto m-r-auto"
        >
          <Div
            type="flex"
            style={{
              width: totalWidth,
              transform: `translateX(${-translateX}px)`,
            }}
            className={cx(
              "",
              curSlideNum > 1 || hasAnim ? styles.container : ""
            )}
          >
            {children?.map((item, idx) => (
              <Div key={idx}>{item}</Div>
            ))}
            {children?.map((item, idx) => (
              <Div key={idx}>{item}</Div>
            ))}
          </Div>
        </Div>
      </Div>

      {numberOfSlides > 1 && Number.isFinite(numberOfSlides) ? (
        <Div type="flex">
          {Array.from({ length: numberOfSlides }).map((_, key) => (
            <Div
              type="flex"
              hAlign="center"
              vAlign="center"
              key={key}
              className={cx(
                "width-px-40 height-px-40 m-r-16 br-rad-per-50 mouse-hand",
                curSlideNum === key + 1 ? "bg-red" : "bg-yellow"
              )}
              onClick={() => {
                if (key === 0) {
                  setHasAnim(true);
                  setTimeout(() => {
                    setHasAnim(false);
                  }, 300);
                }
                setCurSlideNum(key + 1);
              }}
            />
          ))}
        </Div>
      ) : (
        ""
      )}
    </>
  );
};

export default CarouselType2;
