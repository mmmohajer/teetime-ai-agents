import { useEffect, useRef } from "react";
import { useDispatch } from "react-redux";

import { setLoading, setLoaded } from "@/reducer/subs/isLoading";
import { addNewAlertItem } from "@/utils/alert";
import { WITH_DOCKER, APP_DOMAIN } from "config";

const useWebSocket = ({
  sendReq,
  setSendReq,
  url,
  onOpen,
  onMessage,
  onError,
  onClose,
  showLoading = true,
  showErrerMessage = true,
}) => {
  const socketRef = useRef(null);
  const dispatch = useDispatch();

  const send = (data) => {
    const socket = socketRef.current;
    if (socket && socket.readyState === WebSocket.OPEN) {
      if (
        data instanceof ArrayBuffer ||
        ArrayBuffer.isView(data) ||
        data instanceof Blob
      ) {
        socket.send(data); // send binary data directly
      } else if (typeof data === "object") {
        socket.send(JSON.stringify(data)); // send JSON for objects
      } else {
        socket.send(data); // send string
      }
    }
  };

  useEffect(() => {
    let curUrl;

    if (sendReq) {
      if (showLoading) {
        dispatch(setLoading());
      }
      if (!url) return;
      if (!WITH_DOCKER) {
        curUrl = `ws://localhost:8000${url}`;
      } else {
        curUrl = `wss://${APP_DOMAIN}${url}`;
      }

      const socket = new WebSocket(curUrl);
      socketRef.current = socket;

      socket.onopen = () => {
        if (showLoading) {
          dispatch(setLoaded());
        }
        if (onOpen) onOpen(socket);
      };

      socket.onmessage = (event) => {
        if (onMessage) onMessage(event);
      };

      socket.onerror = (error) => {
        if (showLoading) {
          dispatch(setLoaded());
        }
        if (showErrerMessage) {
          if (error?.message) {
            addNewAlertItem(dispatch, "error", `❌ ${error.message}`);
          } else {
            addNewAlertItem(
              dispatch,
              "error",
              "❌ Something went wrong; please try again!"
            );
          }
        }
        if (onError) onError(error);
      };

      socket.onclose = () => {
        if (showLoading) {
          dispatch(setLoaded());
        }
        if (onClose) onClose();
      };
      setTimeout(() => {
        setSendReq(false);
      }, 10);
    }
  }, [url, sendReq]);

  return { socketRef, send };
};

export default useWebSocket;
