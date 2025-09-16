import { useState, useEffect } from "react";
import cx from "classnames";

import Div from "@/baseComponents/reusableComponents/Div";
import Icon from "@/baseComponents/reusableComponents/Icon";
import Label from "@/baseComponents/formComponents/Label";
import TextBox from "@/baseComponents/formComponents/TextBox";

const Type2 = ({
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
  const [searchTerm, setSearchTerm] = useState("");
  const [filteredOptions, setFilteredOptions] = useState();

  useEffect(() => {
    setFilteredOptions([...options]);
  }, [options]);

  useEffect(() => {
    if (!searchTerm) {
      setFilteredOptions([...options]);
      return;
    } else {
      setFilteredOptions((prev) =>
        prev.filter((option) =>
          option.shownText.toLowerCase().includes(searchTerm.toLowerCase())
        )
      );
    }
  }, [searchTerm]);
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
          "f-s-px-14 br-rad-px-10 width-per-100 pos-rel z-1000",
          !showOptions ? "p-x-8 br-all-solid-2 br-black" : ""
        )}
      >
        {!showOptions ? (
          <Div
            onClick={() => setShowOptions(!showOptions)}
            type="flex"
            distributedBetween
            vAlign="center"
            className={cx("width-per-100 height-px-35 mouse-hand")}
          >
            <Div className="p-x-8">
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
        ) : (
          <Div className="">
            <TextBox
              placeHolder="Search a language ..."
              val={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </Div>
        )}

        <Div
          type="flex"
          direction="vertical"
          className={cx(
            `bg-white width-per-100 global-transition-one of-y-auto br-rad-px-10 global-box-shadow-type-one`,
            optionsContainerIsAbsolute ? "pos-abs" : "pos-rel"
          )}
          style={{
            maxHeight: showOptions ? "200px" : "0px",
            zIndex: 100000000,
            width: optionsContainerWidth,
          }}
        >
          {filteredOptions?.map((item, idx) => (
            <Div
              className={cx(
                "p-all-temp-3 bg-silver-on-hover text-black text-center mouse-hand"
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

export default Type2;
