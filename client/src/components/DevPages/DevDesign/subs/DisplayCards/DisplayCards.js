import Div from "@/baseComponents/reusableComponents/Div";

import Blog from "./subs/Blog";
import Tip from "./subs/Tip";
import Project from "./subs/Project";

const DisplayCards = () => {
  return (
    <>
      <Div className="m-all-16">
        <Blog />
      </Div>
      <Div className="m-all-16">
        <Tip />
      </Div>
      <Div className="m-all-16">
        <Project />
      </Div>
    </>
  );
};

export default DisplayCards;
