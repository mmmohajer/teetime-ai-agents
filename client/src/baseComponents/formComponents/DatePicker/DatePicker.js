import Type1 from "./subs/Type1";

const DatePicker = ({ datePickerType = 1, ...props }) => {
  return (
    <>
      {datePickerType === 1 ? <Type1 {...props} /> : null}
      {/* You can add more date picker types here if needed */}
    </>
  );
};

export default DatePicker;
