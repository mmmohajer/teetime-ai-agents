import { useEffect, useState } from "react";
import cx from "classnames";

import Div from "@/baseComponents/reusableComponents/Div";
import Icon from "@/baseComponents/reusableComponents/Icon";
import Select from "@/baseComponents/formComponents/Select";

const Type2 = ({ currentPage, setCurrentPage, listOfPages }) => {
  const [options, setOptions] = useState([]);

  useEffect(() => {
    if (Array.isArray(listOfPages)) {
      setOptions(
        listOfPages.map((num) => ({ value: num, shownText: `${num}` }))
      );
    } else {
      setOptions([]);
    }
  }, [listOfPages]);
  const currentIndex = Array.isArray(listOfPages)
    ? listOfPages.indexOf(currentPage)
    : -1;
  const totalPages = Array.isArray(listOfPages) ? listOfPages.length : 0;

  return (
    <>
      {totalPages > 1 ? (
        <Div type="flex" vAlign="center" className="">
          <Div
            type="flex"
            hAlign="center"
            vAlign="center"
            className="m-r-16 mouse-hand width-px-20 bg-silver height-px-20 br-rad-per-50"
            onClick={() => {
              if (currentIndex > 0) {
                setCurrentPage(listOfPages[currentIndex - 1]);
              } else {
                setCurrentPage(listOfPages[totalPages - 1]);
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

          <Div
            type="flex"
            hAlign="center"
            vAlign="center"
            className="m-l-16 mouse-hand width-px-20 bg-silver height-px-20 br-rad-per-50"
            onClick={() => {
              if (currentIndex < totalPages - 1) {
                setCurrentPage(listOfPages[currentIndex + 1]);
              } else {
                setCurrentPage(listOfPages[0]);
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

export default Type2;
