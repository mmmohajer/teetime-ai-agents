import Div from "@/baseComponents/reusableComponents/Div";
import SVGIcon from "@/baseComponents/reusableComponents/SVGIcon";
import Anchor from "@/baseComponents/reusableComponents/Anchor";

import { GOOGLE_AUTH_URL } from "./constants";

const GoogleAuth = () => {
  return (
    <>
      <Anchor
        to={GOOGLE_AUTH_URL}
        target="_self"
        internal={false}
        anchorType="no-effect"
        className={"m-l-auto-m-r-auto"}
      >
        <Div
          type="flex"
          hAlign="center"
          vAlign="center"
          className="br-rad-px-5 height-px-50 width-px-300 m-l-auto m-r-auto br-all-solid-2 br-theme-two br-rad-px-25 mouse-hand"
        >
          <SVGIcon type={"google"} />
          <Div className="m-l-8">Sign In With Google</Div>
        </Div>
      </Anchor>
    </>
  );
};

export default GoogleAuth;
