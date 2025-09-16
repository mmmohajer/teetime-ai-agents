import { useState } from "react";
import cx from "classnames";

import Div from "@/baseComponents/reusableComponents/Div";
import Icon from "@/baseComponents/reusableComponents/Icon";
import Label from "@/baseComponents/formComponents/Label";

import { COLORS } from "@/constants/vars";

const Type1 = ({
  options,
  val,
  optionChanged,
  placeHolder,
  label,
  isRequired,
  optionsContainerIsAbsolute = true,
  optionsContainerWidth = "100%",
}) => {
  const [showOptions, setShowOptions] = useState(false);
  return (
    <>
      {showOptions && optionsContainerIsAbsolute ? (
        <Div
          onClick={() => {
            setShowOptions(false);
          }}
          className="pos-fix pos-fix--lt height-vh-full width-per-100 z-100 of-hidden"
        />
      ) : (
        ""
      )}
      <Label label={label} isRequired={isRequired} />
      <Div
        className={cx(
          "p-all-temp-1 f-s-px-14 br-rad-px-10 br-all-solid-2 br-black width-per-100 pos-rel"
        )}
      >
        <Div
          onClick={() => setShowOptions(!showOptions)}
          type="flex"
          distributedBetween
          vAlign="center"
          className={cx("width-per-100 p-x-temp-3 height-px-35 mouse-hand")}
        >
          <Div>
            {val ? (
              options.find((opt) => opt.value === val)?.shownText || val
            ) : (
              <span className="text-slategray f-s-px-12">{placeHolder}</span>
            )}
          </Div>
          <Div
            className={cx(
              "global-transition-one",
              showOptions ? "global-rotate-180" : ""
            )}
          >
            <Icon type="angle-up" color={"black"} />
          </Div>
        </Div>

        <Div
          type="flex"
          direction="vertical"
          className={cx(
            `bg-white width-per-100 global-transition-one of-y-auto br-rad-px-10 global-box-shadow-type-one`,
            optionsContainerIsAbsolute ? "pos-abs pos-abs--lb" : "pos-rel"
          )}
          style={{
            maxHeight: showOptions ? "300px" : "0px",
            zIndex: 100000000,
            width: optionsContainerWidth,
          }}
        >
          {options?.map((item, idx) => (
            <Div
              className={cx(
                "p-all-temp-3 bg-silver-on-hover text-center mouse-hand"
              )}
              key={idx}
              onClick={() => {
                if (optionChanged) {
                  optionChanged(item?.value);
                }
                setShowOptions(false);
              }}
            >
              {item?.shownText}
            </Div>
          ))}
        </Div>
      </Div>
    </>
  );
};

export default Type1;
