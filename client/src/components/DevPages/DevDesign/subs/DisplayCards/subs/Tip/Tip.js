import Div from "@/baseComponents/reusableComponents/Div";
import Card from "@/baseComponents/reusableComponents/Card";

const Tip = () => {
  return (
    <>
      <Div className="width-px-350">
        <Card
          cardType="tip"
          tipNumber={1}
          imgSrc="https://picsum.photos/400/400"
          imgAlt="Test"
          title="Tip Card"
          excerpt={`Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.`}
          publishedDate="Mar 03, 2025"
        />
      </Div>
    </>
  );
};

export default Tip;
