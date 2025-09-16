import Div from "@/baseComponents/reusableComponents/Div";
import Icon from "@/baseComponents/reusableComponents/Icon/Icon";

import { ICON_TYPES } from "./constants";

const DisplayIcons = () => {
  return (
    <>
      <Div className="width-per-100 p-x-temp-4 m-y-temp-8">
        {ICON_TYPES?.map((item, idx) => (
          <Div
            type="flex"
            vAlign="center"
            className="width-per-100 bg-theme-one p-x-temp-4 m-b-32"
            key={idx}
          >
            <Div className="f-b m-r-32">{item}:</Div>
            <Div
              type="flex"
              hAlign="center"
              vAlign="center"
              className="width-px-40 height-px-40"
            >
              <Icon type={item} width={40} height={40} />
            </Div>
          </Div>
        ))}
      </Div>
    </>
  );
};

export default DisplayIcons;
