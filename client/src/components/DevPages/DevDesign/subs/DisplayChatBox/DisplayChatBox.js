import { useState, useEffect } from "react";

import Div from "@/baseComponents/reusableComponents/Div";
import ChatBox from "@/baseComponents/reusableComponents/ChatBox";

const DisplayChatBox = () => {
  const [goBottomOfTheContainer, setGoBottomOfTheContainer] = useState(false);
  const [userChatMessage, setUserChatMessage] = useState("");
  const [handleChunk, setHandleChunk] = useState(null);
  const [handleAudioComplete, setHandleAudioComplete] = useState(null);
  const [showLoader, setShowLoader] = useState(false);
  const [isRecording, setIsRecording] = useState(false);

  return (
    <>
      <ChatBox
        goBottomOfTheContainer={goBottomOfTheContainer}
        userChatMessage={userChatMessage}
        handleChunk={handleChunk}
        handleAudioComplete={handleAudioComplete}
        showLoader={showLoader}
        isRecording={isRecording}
        setGoBottomOfTheContainer={setGoBottomOfTheContainer}
        setUserChatMessage={setUserChatMessage}
        setIsRecording={setIsRecording}
        mainContainerClassName={"height-vh-full bg-white"}
        onMessageSentClick={() => {
          console.log("Message to be sent:", userChatMessage);
        }}
      >
        <Div>DisplayChatBox</Div>
      </ChatBox>
    </>
  );
};

export default DisplayChatBox;
