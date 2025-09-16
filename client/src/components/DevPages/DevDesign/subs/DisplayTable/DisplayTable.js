import { useMemo } from "react";

import Div from "@/baseComponents/reusableComponents/Div";
import Table from "@/baseComponents/reusableComponents/Table";

import { MOCK_DATA } from "./constants";
import { HEADING_TITLE_ROWS, HEADING_DATA, BODY_DATA } from "./utils";

const DisplayTable = () => {
  const bodyData = useMemo(() => BODY_DATA(MOCK_DATA), [MOCK_DATA]);
  return (
    <Div className="width-per-100">
      <Table
        headingTitleRows={HEADING_TITLE_ROWS()}
        headingData={HEADING_DATA()}
        bodyData={bodyData}
        useFullWidth={true}
        className={"bg-orange"}
      />
    </Div>
  );
};

export default DisplayTable;
