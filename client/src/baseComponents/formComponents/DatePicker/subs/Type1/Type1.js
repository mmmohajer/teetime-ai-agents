import cx from "classnames";
import { default as BaseDatePicker } from "react-datepicker";

import Div from "@/baseComponents/reusableComponents/Div";
import Label from "@/baseComponents/formComponents/Label";

import "react-datepicker/dist/react-datepicker.css";

const Type1 = ({
  className,
  isRequired,
  label,
  chosenDate,
  setChosenDate,
  dateFormat = "dd-MM-yyyy",
  yearDropdownItemNumber = 100,
  showYearDropdown = true,
  showMonthDropdown = false,
  placeHolder,
  showTimeSelect = false,
  showTimeSelectOnly = false,
  hasMarginBottom = true,
  ...props
}) => {
  return (
    <>
      <Div className={cx("pos-rel", hasMarginBottom && "m-b-32", className)}>
        {label && <Label label={label} isRequired={isRequired} />}
        <Div className={cx("customDatePickerWidth")}>
          <BaseDatePicker
            selected={chosenDate}
            onChange={(date) => setChosenDate(date)}
            className={cx(
              "width-per-100 p-y-16 p-x-8 br-none global-outline-none bg-gray-bright text-gray br-rad-px-10"
            )}
            dateFormat={dateFormat}
            yearDropdownItemNumber={yearDropdownItemNumber}
            scrollableYearDropdown={true}
            showYearDropdown={showYearDropdown}
            showMonthDropdown={showMonthDropdown}
            placeholderText={placeHolder}
            showTimeSelect={showTimeSelect}
            showTimeSelectOnly={showTimeSelectOnly}
            // timeFormat="HH:mm"
            // timeIntervals={15}
            // timeCaption="Time"
            {...props}
          />
        </Div>
      </Div>
    </>
  );
};

export default Type1;
