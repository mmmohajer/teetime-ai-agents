import axios from "axios";
import { APP_DOMAIN_FOR_SERVER_SIDE_PROPS } from "config";

export async function fetchDataForSSR(dataType, apiRoute) {
  const url = `${APP_DOMAIN_FOR_SERVER_SIDE_PROPS}${apiRoute}`;
  let data = [];
  try {
    const res = await axios.get(url);
    if (res?.data) {
      data = res.data;
    }
    return data;
  } catch (err) {
    console.log(err);
    if (dataType === "list") {
      return [];
    } else if (dataType === "object") {
      return {};
    }
  }
}
