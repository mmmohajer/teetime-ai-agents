import Type1 from "./subs/Type1";

const AreaText = ({ areaType = 1, ...props }) => {
  return (
    <>
      {areaType === 1 ? <Type1 {...props} /> : null}
      {/* You can add more area types here if needed */}
    </>
  );
};

export default AreaText;
