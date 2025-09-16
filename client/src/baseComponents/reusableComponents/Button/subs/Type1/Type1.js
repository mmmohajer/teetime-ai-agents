import cx from "classnames";
import Div from "@/baseComponents/reusableComponents/Div";

const Type1 = ({ btnText, className, ...props }) => {
  return (
    <>
      <button
        className={cx(
          "p-y-8 p-x-16 br-rad-px-50 mouse-hand",
          props?.disabled
            ? "bg-silver text-gray opacity-60"
            : "bg-theme-one br-all-solid-2 br-green bg-blue-on-hover text-black text-white-on-hover br-blue-on-hover",
          className
        )}
        {...props}
      >
        {btnText}
      </button>
    </>
  );
};

export default Type1;
