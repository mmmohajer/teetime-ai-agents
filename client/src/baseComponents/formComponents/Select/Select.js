import Div from "@/baseComponents/reusableComponents/Div";

import Type1 from "./subs/Type1";
import Type2 from "./subs/Type2";

const Select = ({ selectType = 1, ...props }) => {
  return (
    <>
      {selectType === 1 ? <Type1 {...props} /> : null}
      {selectType === 2 ? <Type2 {...props} /> : null}
    </>
  );
};

export default Select;
