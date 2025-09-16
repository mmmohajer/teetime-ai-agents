import { useState, useEffect } from "react";
import cx from "classnames";

import Div from "@/baseComponents/reusableComponents/Div";
import Icon from "@/baseComponents/reusableComponents/Icon";

import useDivWidth from "@/hooks/useDivWidth";
import { COLORS } from "@/constants/vars";

import styles from "./CarouselType1.module.scss";

const CarouselType1 = ({
  itemWidth,
  gapBetweenItems,
  numberOfItems,
  children,
}) => {
  const { containerRef, width } = useDivWidth();

  const [showNextItems, setShowNextItems] = useState(false);
  const [showPrevItems, setShowPrevItems] = useState(false);
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
    if (showNextItems && itemsHolderWidth) {
      if (
        translateX + itemsHolderWidth + gapBetweenItems <
        totalWidth - itemWidth
      ) {
        setTranslateX(translateX + itemsHolderWidth + gapBetweenItems);
      } else {
        setTranslateX(totalWidth - itemsHolderWidth);
      }
      setTimeout(() => {
        setShowNextItems(false);
      }, 10);
    }
  }, [showNextItems, itemsHolderWidth]);

  useEffect(() => {
    if (showPrevItems && itemsHolderWidth) {
      if (translateX - itemsHolderWidth - gapBetweenItems > 0) {
        setTranslateX(translateX - itemsHolderWidth - gapBetweenItems);
      } else {
        setTranslateX(0);
      }
      setTimeout(() => {
        setShowPrevItems(false);
      }, 10);
    }
  }, [showPrevItems, itemsHolderWidth]);
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
            className={cx("", styles.container)}
          >
            {children?.map((item, idx) => (
              <Div key={idx}>{item}</Div>
            ))}
          </Div>
        </Div>
      </Div>

      {totalWidth > itemsHolderWidth ? (
        <Div
          type="flex"
          hAlign="center"
          vAlign="center"
          className="width-per-100 m-t-temp-8"
        >
          <Div
            type="flex"
            hAlign="center"
            vAlign="center"
            className="width-px-40 height-px-40 bg-theme-seven br-rad-per-50 m-r-20 mouse-hand"
            onClick={() => setShowPrevItems(true)}
          >
            <Icon
              type="left"
              color={translateX === 0 ? "#333" : COLORS["theme-one"]}
            />
          </Div>
          <Div
            type="flex"
            hAlign="center"
            vAlign="center"
            className="width-px-40 height-px-40 bg-theme-seven br-rad-per-50 mouse-hand"
            onClick={() => setShowNextItems(true)}
          >
            <Icon
              type="right"
              color={
                translateX >= totalWidth - itemsHolderWidth
                  ? "#333"
                  : COLORS["theme-one"]
              }
            />
          </Div>
        </Div>
      ) : (
        ""
      )}
    </>
  );
};

export default CarouselType1;
