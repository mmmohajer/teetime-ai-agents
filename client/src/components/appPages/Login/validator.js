import { addNewAlertItem } from "@/utils/alert";
import { isValidEmail } from "@/utils/validators";

export const formValidated = (dispatch, email, password) => {
  let validated = true;
  if (!email) {
    validated = false;
    addNewAlertItem(dispatch, "error", "Email is required");
    return validated;
  }
  if (!isValidEmail(email)) {
    validated = false;
    addNewAlertItem(dispatch, "error", "Email is not valid");
    return validated;
  }
  if (!password) {
    validated = false;
    addNewAlertItem(dispatch, "error", "Password is required");
    return validated;
  }
  return validated;
};
