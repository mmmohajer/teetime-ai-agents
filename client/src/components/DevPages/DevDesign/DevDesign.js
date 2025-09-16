import { useState } from "react";
import { useSelector } from "react-redux";
import cx from "classnames";

import Div from "@/baseComponents/reusableComponents/Div/Div";
import Icon from "@/baseComponents/reusableComponents/Icon/Icon";

import DisplayColors from "./subs/DisplayColors";
import DisplayButton from "./subs/DisplayButton";
import DisplayIcons from "./subs/DisplayIcons";
import DisplayAnchor from "./subs/DisplayAnchor";
import DisplayCards from "./subs/DisplayCards";
import DisplayModal from "./subs/DisplayModal";
import DisplayCarousel from "./subs/DisplayCarousel";
import DisplayAlert from "./subs/DisplayAlert";
import DisplayRowColumn from "./subs/DisplayRowColumn";
import DisplayForm from "./subs/DisplayForm";
import DisplayTable from "./subs/DisplayTable";
import TestSocket from "./subs/TestSocket";
import DisplayVoiceRecorder from "./subs/DisplayVoiceRecorder";
import DisplayPagination from "./subs/DisplayPagination";
import DisplayStreaming from "./subs/DisplayStreaming";
import DisplayChatBox from "./subs/DisplayChatBox";
import DisplayConnectionToSocket from "./subs/DisplayConnectionToSocket";

import { DESIGN_ITEMS } from "./constants";

const DevDesign = () => {
  const [showMenu, setShowMenu] = useState(true);
  const [chosenItem, setChosenItem] = useState("");
  return (
    <>
      <Div className={cx("min-height-vh-full bg-theme-three")}>
        {showMenu ? (
          <Div className="width-px-200 min-height-vh-full of-y-auto bg-theme-one scroll-type-one">
            {DESIGN_ITEMS?.map((item, idx) => (
              <Div
                key={idx}
                className={cx(
                  "p-y-8 p-x-16 text-center m-b-8 text-black mouse-hand",
                  chosenItem === item?.identifier
                    ? "bg-theme-two"
                    : "bg-theme-three"
                )}
                onClick={() => {
                  setShowMenu(false);
                  setChosenItem(item?.identifier);
                }}
              >
                {item?.title}
              </Div>
            ))}
          </Div>
        ) : (
          <Div
            type="flex"
            direction="vertical"
            hAlign="center"
            className={cx("width-per-100")}
          >
            <Div
              type="flex"
              hAlign="center"
              vAlign="center"
              className="pos-abs bg-theme-seven br-rad-per-50 width-px-30 height-px-30 mouse-hand"
              style={{ top: "8px", right: "8px" }}
              onClick={() => {
                setChosenItem("");
                setShowMenu(true);
              }}
            >
              <Icon type="close" scale={1.5} color="white" />
            </Div>
            <Div
              type="flex"
              hAlign="center"
              className={cx("width-per-100 flex--wrap bg-blue")}
            >
              {chosenItem === "colors" ? <DisplayColors /> : ""}
              {chosenItem === "buttons" ? <DisplayButton /> : ""}
              {chosenItem === "icons" ? <DisplayIcons /> : ""}
              {chosenItem === "anchors" ? <DisplayAnchor /> : ""}
              {chosenItem === "cards" ? <DisplayCards /> : ""}
              {chosenItem === "modals" ? <DisplayModal /> : ""}
              {chosenItem === "carousel" ? <DisplayCarousel /> : ""}
              {chosenItem === "alert" ? <DisplayAlert /> : ""}
              {chosenItem === "row-column" ? <DisplayRowColumn /> : ""}
              {chosenItem === "form" ? <DisplayForm /> : ""}
              {chosenItem === "table" ? <DisplayTable /> : ""}
              {chosenItem === "test-socket" ? <TestSocket /> : ""}
              {chosenItem === "voice-recorder" ? <DisplayVoiceRecorder /> : ""}
              {chosenItem === "pagination" ? <DisplayPagination /> : ""}
              {chosenItem === "streaming" ? <DisplayStreaming /> : ""}
              {chosenItem === "chat-box" ? <DisplayChatBox /> : ""}
              {chosenItem === "connection-to-socket" ? (
                <DisplayConnectionToSocket />
              ) : (
                ""
              )}
            </Div>
          </Div>
        )}

        <Div
          className="pos-fix z-100"
          style={{ bottom: "10px", right: "10px" }}
        ></Div>
      </Div>
    </>
  );
};

export default DevDesign;
