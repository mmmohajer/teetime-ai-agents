import CarouselType1 from "./subs/CarouselType1";
import CarouselType2 from "./subs/CarouselType2";

const Carousel = ({ type = 1, ...props }) => {
  return (
    <>
      {type === 1 ? <CarouselType1 {...props} /> : ""}
      {type === 2 ? <CarouselType2 {...props} /> : ""}
    </>
  );
};

export default Carousel;
