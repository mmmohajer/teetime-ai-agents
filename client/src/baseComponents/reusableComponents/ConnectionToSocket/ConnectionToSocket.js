import { useState, useEffect } from "react";
import { useSelector } from "react-redux";

import Div from "@/baseComponents/reusableComponents/Div";

import useWebSocket from "@/hooks/useWebSocket";

const ConnectionToSocket = ({
  socketRefManager,
  setWsData,
  wsUrl,
  sendWsReq,
  children,
}) => {
  const accessToken = useSelector((state) => state.accessToken);
  // -------------------------------------------------
  // Chat Socket Request Handler Start
  // -------------------------------------------------
  const [sendReq, setSendReq] = useState(false);
  const { socketRef, send } = useWebSocket({
    sendReq,
    setSendReq,
    url: `${wsUrl}?token=${accessToken}`,
    onMessage: (event) => {
      const data = JSON.parse(event.data);
      setWsData((prev) => ({ ...prev, ...data }));
    },
  });
  useEffect(() => {
    if (sendWsReq) {
      setSendReq(true);
    }
  }, [sendWsReq]);
  useEffect(() => {
    if (socketRef && send) {
      socketRefManager.current = { ref: socketRef, send: send };
    }
  }, [socketRef, send]);
  // -------------------------------------------------
  // Chat Socket Request Handler End
  // -------------------------------------------------
  return <>{children}</>;
};

export default ConnectionToSocket;
