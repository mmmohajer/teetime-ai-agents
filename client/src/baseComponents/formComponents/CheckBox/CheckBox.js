import Type1 from "./subs/Type1";

const CheckBox = ({ checkBoxType = 1, ...props }) => {
  return (
    <>
      {checkBoxType === 1 ? <Type1 {...props} /> : null}
      {/* You can add more check box types here if needed */}
    </>
  );
};

export default CheckBox;
