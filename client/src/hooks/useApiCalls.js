import { useDispatch, useSelector } from "react-redux";
import { useState, useEffect } from "react";
import axios from "axios";

import { WITH_DOCKER } from "config";
import { addNewAlertItem } from "@/utils/alert";
import { setLoading, setLoaded } from "@/reducer/subs/isLoading";
import { getLocalStorage } from "@/utils/storage";
import { JWT_PRE_WORD } from "@/constants/vars";

const useApiCalls = ({
  method,
  url,
  bodyData,
  headers,
  sendReq,
  setSendReq,
  handleError,
  useDefaultHeaders = true,
  showLoading = true,
  showErrerMessage = true,
}) => {
  const dispatch = useDispatch();
  const accessToken = useSelector((state) => state.accessToken);

  const [data, setData] = useState();
  const [status, setStatus] = useState();

  const handleReq = async () => {
    try {
      let curUrl;
      let res;
      if (useDefaultHeaders && accessToken) {
        if (!headers) {
          headers = { Authorization: `${JWT_PRE_WORD} ${accessToken}` };
        } else {
          headers["Authorization"] = `${JWT_PRE_WORD} ${accessToken}`;
        }
      }
      if (!WITH_DOCKER) {
        curUrl = `http://localhost:8000${url}`;
      } else {
        curUrl = `${url}`;
      }
      if (method === "GET") {
        if (showLoading) {
          dispatch(setLoading());
        }
        res = await axios.get(curUrl, { headers: headers || {} });
        if (showLoading) {
          dispatch(setLoaded());
        }
        if (res?.data) {
          setData(res.data);
        }
        if (res?.status) {
          setStatus(res.status);
        }
      }

      if (method === "POST") {
        if (showLoading) {
          dispatch(setLoading());
        }
        res = await axios.post(curUrl, bodyData || {}, {
          headers: headers || {},
        });
        if (showLoading) {
          dispatch(setLoaded());
        }
        if (res?.data) {
          setData(res.data);
        }
        if (res?.status) {
          setStatus(res.status);
        }
      }

      if (method === "PUT") {
        if (showLoading) {
          dispatch(setLoading());
        }
        res = await axios.put(curUrl, bodyData || {}, {
          headers: headers || {},
        });
        if (showLoading) {
          dispatch(setLoaded());
        }
        if (res?.data) {
          setData(res.data);
        }
        if (res?.status) {
          setStatus(res.status);
        }
      }

      if (method === "DELETE") {
        if (showLoading) {
          dispatch(setLoading());
        }
        res = await axios.delete(curUrl, { headers: headers || {} });
        if (showLoading) {
          dispatch(setLoaded());
        }
        if (res?.data) {
          setData(res.data);
        }
        if (res?.status) {
          setStatus(res.status);
        }
      }
    } catch (err) {
      if (showLoading) {
        dispatch(setLoaded());
      }
      if (handleError) {
        handleError();
      }
      if (err?.response?.data?.message) {
        if (showErrerMessage) {
          addNewAlertItem(dispatch, "error", `❌ ${err.response.data.message}`);
        }
      } else {
        if (showErrerMessage) {
          addNewAlertItem(
            dispatch,
            "error",
            "❌ Something went wrong; please try again!"
          );
        }
      }
    }
  };

  useEffect(() => {
    if (sendReq) {
      handleReq();
      setTimeout(() => {
        setSendReq(false);
      }, 10);
    }
  }, [sendReq]);

  return { data, status };
};

export default useApiCalls;
