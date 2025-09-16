import { useEffect, useState } from "react";
import cx from "classnames";

import Div from "@/baseComponents/reusableComponents/Div";
import Icon from "@/baseComponents/reusableComponents/Icon";
import Select from "@/baseComponents/formComponents/Select";

const Type1 = ({ currentPage, setCurrentPage, numberOfTotalPages }) => {
  const [options, setOptions] = useState([]);

  useEffect(() => {
    const localOptions = [];
    for (let i = 1; i <= numberOfTotalPages; i++) {
      localOptions.push({ value: i, shownText: `${i}` });
    }
    setOptions([...localOptions]);
  }, [numberOfTotalPages]);
  return (
    <>
      {numberOfTotalPages > 1 ? (
        <Div type="flex" vAlign="center" className="">
          <Div
            type="flex"
            hAlign="center"
            vAlign="center"
            className="m-r-16 mouse-hand width-px-20 bg-silver height-px-20 br-rad-per-50"
            onClick={() => {
              if (currentPage > 1) {
                setCurrentPage(currentPage - 1);
              } else {
                setCurrentPage(numberOfTotalPages);
              }
            }}
          >
            <Icon type="left" color={"black"} scale={0.7} />
          </Div>
          <Div className="text-off-black">Page </Div>
          <Div className="width-px-80 m-l-temp-2 m-r-temp-2">
            <Select
              options={options}
              val={currentPage}
              optionChanged={setCurrentPage}
              selectIntialShownText={""}
              labelText=""
              hasMarginBottom={false}
            />
          </Div>
          <Div className="text-black">of {numberOfTotalPages}</Div>
          <Div
            type="flex"
            hAlign="center"
            vAlign="center"
            className="m-l-16 mouse-hand width-px-20 bg-silver height-px-20 br-rad-per-50"
            onClick={() => {
              if (currentPage < numberOfTotalPages) {
                setCurrentPage(currentPage + 1);
              } else {
                setCurrentPage(1);
              }
            }}
          >
            <Icon type="right" color={"black"} scale={0.7} />
          </Div>
        </Div>
      ) : (
        ""
      )}
    </>
  );
};

export default Type1;
