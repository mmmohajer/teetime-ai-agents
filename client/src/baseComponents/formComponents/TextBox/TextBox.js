import Div from "@/baseComponents/reusableComponents/Div";

import Type1 from "./subs/Type1";

const TextBox = ({ textBoxType = 1, ...props }) => {
  return (
    <>
      {textBoxType === 1 ? <Type1 {...props} /> : null}
      {/* You can add more text box types here if needed */}
    </>
  );
};

export default TextBox;
