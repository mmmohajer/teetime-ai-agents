import Type1 from "./subs/Type1";

const ImagePicker = ({ type = 1, ...props }) => {
  return <>{type === 1 ? <Type1 {...props} /> : ""}</>;
};

export default ImagePicker;
