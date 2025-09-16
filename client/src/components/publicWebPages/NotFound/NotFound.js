import Div from "@/baseComponents/reusableComponents/Div";

const NotFound = () => {
  return (
    <>
      <Div
        type="flex"
        hAlign="center"
        vAlign="center"
        className="global-min-full-vh bg-green"
      >
        <Div className="width-per-100 max-width-px-500 p-all-temp-8 text-center bg-theme-two br-rad-md text-white">
          Oops! The page you're looking for isn't here. Explore the latest tech
          insights, coding tips, and system design strategies on Tech Tips by
          Moh.
        </Div>
      </Div>
    </>
  );
};

export default NotFound;
