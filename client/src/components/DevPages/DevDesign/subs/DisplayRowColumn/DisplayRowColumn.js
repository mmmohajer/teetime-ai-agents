import Div from "@/baseComponents/reusableComponents/Div";
import Row from "@/baseComponents/reusableComponents/Row";
import Column from "@/baseComponents/reusableComponents/Column";

const DisplayRowColumn = () => {
  return (
    <>
      <Row className="width-per-100">
        <Column xs={12} sm={6} md={4} lg={3}>
          <Div className="width-per-100 m-all-16 bg-red text-white text-center">
            Column 1
          </Div>
        </Column>
        <Column xs={12} sm={6} md={4} lg={3}>
          <Div className="width-per-100 m-all-16 bg-red text-white text-center">
            Column 2
          </Div>
        </Column>
        <Column xs={12} sm={6} md={4} lg={3}>
          <Div className="width-per-100 m-all-16 bg-red text-white text-center">
            Column 3
          </Div>
        </Column>
        <Column xs={12} sm={6} md={4} lg={3}>
          <Div className="width-per-100 m-all-16 bg-red text-white text-center">
            Column 4
          </Div>
        </Column>
      </Row>
    </>
  );
};

export default DisplayRowColumn;
