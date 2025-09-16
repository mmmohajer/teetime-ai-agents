import { addNewAlertItem } from "@/utils/alert";
import { isValidEmail } from "@/utils/validators";

export const formValidated = (dispatch, email) => {
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
  return validated;
};
