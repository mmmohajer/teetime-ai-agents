import { useState, useEffect, useRef } from "react";

import Div from "@/baseComponents/reusableComponents/Div";
import ConnectionToSocket from "@/baseComponents/reusableComponents/ConnectionToSocket";

import { WEBSOCKET_TEST_API_ROUTE } from "@/constants/apiRoutes";

import { handleWsData } from "./utils";

const DisplayConnectionToSocket = () => {
  const socketRefManager = useRef();

  const [sendWsReq, setSendWsReq] = useState(false);
  const [wsData, setWsData] = useState({});

  useEffect(() => {
    handleWsData(socketRefManager, wsData);
  }, [wsData]);

  useEffect(() => {
    setSendWsReq(true);
  }, []);

  return (
    <>
      <ConnectionToSocket
        socketRefManager={socketRefManager}
        setWsData={setWsData}
        sendWsReq={sendWsReq}
        wsUrl={`${WEBSOCKET_TEST_API_ROUTE}1234/`}
      >
        <Div>
          {wsData?.connection
            ? "Connection To Socket Component"
            : "No Connection"}
        </Div>
      </ConnectionToSocket>
    </>
  );
};

export default DisplayConnectionToSocket;
