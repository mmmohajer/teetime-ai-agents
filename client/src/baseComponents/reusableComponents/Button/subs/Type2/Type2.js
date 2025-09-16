import cx from "classnames";
import Div from "@/baseComponents/reusableComponents/Div";
import Icon from "@/baseComponents/reusableComponents/Icon";

const Type2 = ({
  btnText,
  iconType,
  iconScale = 1,
  iconColor = "black",
  className,
  ...props
}) => {
  return (
    <>
      <button
        className={cx(
          "p-y-8 p-x-16 br-rad-px-50 mouse-hand",
          props?.disabled
            ? "bg-silver text-gray-500 cursor-not-allowed opacity-60"
            : "bg-theme-one br-all-solid-2 br-color-theme-five bg-theme-five-on-hover text-theme-five text-white-on-hover br-color-five-on-hover",
          className
        )}
        {...props}
      >
        <Div type="flex">
          <Div className="m-r-8">
            <Icon type={iconType} scale={iconScale} color={iconColor} />
          </Div>
          <Div>{btnText}</Div>
        </Div>
      </button>
    </>
  );
};

export default Type2;
