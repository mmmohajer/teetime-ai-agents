import { useState } from "react";

import Div from "@/baseComponents/reusableComponents/Div";
import Pagination from "@/baseComponents/reusableComponents/Pagination";

const DisplayPagination = () => {
  const [currentPage, setCurrentPage] = useState(1);
  const numberOfTotalPages = 5;
  return (
    <Pagination
      currentPage={currentPage}
      setCurrentPage={setCurrentPage}
      numberOfTotalPages={numberOfTotalPages}
    />
  );
};

export default DisplayPagination;
