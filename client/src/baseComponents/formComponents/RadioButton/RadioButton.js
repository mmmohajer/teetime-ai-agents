import Div from "@/baseComponents/reusableComponents/Div";

import Type1 from "./subs/Type1";

const RadioButton = ({ radioType = 1, ...props }) => {
  return (
    <>
      {radioType === 1 ? <Type1 {...props} /> : null}
      {/* You can add more radio types here if needed */}
    </>
  );
};

export default RadioButton;
