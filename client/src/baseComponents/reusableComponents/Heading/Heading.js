import Div from "@/baseComponents/reusableComponents/Div";

const Heading = ({ type = 1, children, ...props }) => {
  return (
    <>
      {type === 1 ? <h1 {...props}>{children}</h1> : ""}
      {type === 2 ? <h2 {...props}>{children}</h2> : ""}
      {type === 3 ? <h3 {...props}>{children}</h3> : ""}
      {type === 4 ? <h4 {...props}>{children}</h4> : ""}
      {type === 5 ? <h5 {...props}>{children}</h5> : ""}
      {type === 6 ? <h6 {...props}>{children}</h6> : ""}
    </>
  );
};

export default Heading;
