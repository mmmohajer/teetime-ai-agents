import Div from "@/baseComponents/reusableComponents/Div";

const Form = ({ onSubmit, children, ...props }) => {
  return (
    <>
      <form
        onSubmit={(e) => {
          e.preventDefault();
          if (onSubmit) {
            onSubmit(e);
          }
        }}
        {...props}
      >
        {children}
      </form>
    </>
  );
};

export default Form;
