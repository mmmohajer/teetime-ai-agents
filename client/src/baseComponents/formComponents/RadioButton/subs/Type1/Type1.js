import cx from "classnames";

import Div from "@/baseComponents/reusableComponents/Div";

import Label from "@/baseComponents/formComponents/Label";

const Type1 = ({
  label,
  isRequired,
  listOfOptions,
  setSelectedOption,
  selectedOption,
}) => {
  return (
    <>
      <Label label={label} isRequired={isRequired} />
      {listOfOptions.map((option) => (
        <Div type="flex" vAlign="center" key={option.value} className="m-b-16">
          <Div
            type="flex"
            vAlign="center"
            hAlign="center"
            className={cx(
              "width-px-20 height-px-20 br-rad-per-50 m-r-8 br-all-solid-1 mouse-hand"
            )}
            onClick={() => setSelectedOption(option.value)}
          >
            {selectedOption === option.value ? (
              <Div className="bg-blue width-px-10 height-px-10 br-rad-per-50" />
            ) : null}
          </Div>
          <Label label={option.label} />
        </Div>
      ))}
    </>
  );
};

export default Type1;
