import Div from "@/baseComponents/reusableComponents/Div";

import Type1 from "./subs/Type1";
import Type2 from "./subs/Type2";

const Pagination = ({ type = 1, ...props }) => {
  return (
    <>
      {type === 1 ? <Type1 {...props} /> : null}
      {type === 2 ? <Type2 {...props} /> : null}
    </>
  );
};

export default Pagination;
