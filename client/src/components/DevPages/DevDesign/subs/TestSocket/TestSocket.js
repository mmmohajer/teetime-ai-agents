import { useState, useEffect } from "react";

import Div from "@/baseComponents/reusableComponents/Div";

import useWebSocket from "@/hooks/useWebSocket";
import { WEBSOCKET_TEST_API_ROUTE } from "@/constants/apiRoutes";

const TestSocket = () => {
  // ------------------------------------------------
  // WebSocket connection
  // ------------------------------------------------
  const [sendReq, setSendReq] = useState(false);
  const { socketRef, send } = useWebSocket({
    sendReq,
    setSendReq,
    url: WEBSOCKET_TEST_API_ROUTE,
    onMessage: (event) => {
      const data = JSON.parse(event.data);
      console.log("WebSocket message received:", data);
    },
    onOpen: () => {
      console.log("WebSocket connection opened");
      send({ action: "process_data" });
    },
    onError: (error) => {
      console.error("WebSocket error:", error);
    },
    onClose: () => {
      console.log("WebSocket connection closed");
    },
  });
  useEffect(() => {
    setSendReq(true);
  }, []);
  // ------------------------------------------------
  // ------------------------------------------------

  return (
    <>
      <Div>TestSocket</Div>
    </>
  );
};

export default TestSocket;
