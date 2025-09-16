import Div from "@/baseComponents/reusableComponents/Div";
import Carousel from "@/baseComponents/reusableComponents/Carousel";

const DisplayCarousel = () => {
  return (
    <>
      <Carousel type={1} numberOfItems={9} itemWidth={500} gapBetweenItems={20}>
        <Div className="width-px-500 height-px-300 bg-green m-r-20">
          Hello 1
        </Div>
        <Div className="width-px-500 height-px-300 bg-green m-r-20">
          Hello 2
        </Div>
        <Div className="width-px-500 height-px-300 bg-green m-r-20">
          Hello 3
        </Div>
        <Div className="width-px-500 height-px-300 bg-green m-r-20">
          Hello 4
        </Div>
        <Div className="width-px-500 height-px-300 bg-green m-r-20">
          Hello 5
        </Div>
        <Div className="width-px-500 height-px-300 bg-green m-r-20">
          Hello 6
        </Div>
        <Div className="width-px-500 height-px-300 bg-green m-r-20">
          Hello 7
        </Div>
        <Div className="width-px-500 height-px-300 bg-green m-r-20">
          Hello 8
        </Div>
        <Div className="width-px-500 height-px-300 bg-green m-r-20">
          Hello 9
        </Div>
      </Carousel>
    </>
  );
};

export default DisplayCarousel;
