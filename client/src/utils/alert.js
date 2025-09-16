import {
  addAlertItem,
  removeAlertItem,
  updateAlertDisplay,
} from "@/reducer/subs/alert";
import { generateRandomString } from "./helpers";

export const removeAnAlertItem = (dispatch, key) => {
  dispatch(updateAlertDisplay({ key, display: false }));
  setTimeout(() => {
    dispatch(removeAlertItem({ key }));
  }, 300);
};

export const addNewAlertItem = (dispatch, type, message) => {
  const key = generateRandomString(16);
  dispatch(
    addAlertItem({
      type,
      key,
      message,
    })
  );
  setTimeout(() => {
    dispatch(updateAlertDisplay({ key, display: true }));
  }, 5);
  setTimeout(() => {
    removeAnAlertItem(dispatch, key);
  }, 15000);
};
