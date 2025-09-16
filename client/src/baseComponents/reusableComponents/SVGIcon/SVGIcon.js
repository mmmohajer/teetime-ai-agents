import Google from "./subs/Google";

const SVGIcon = ({
  type,
  fill = "none",
  stroke = "black",
  width = 30,
  height = 30,
}) => {
  const IconComponent = iconMap[type];
  if (!IconComponent) return null;
  return (
    <IconComponent fill={fill} stroke={stroke} height={height} width={width} />
  );
};

const iconMap = {
  google: Google,
};

export default SVGIcon;
