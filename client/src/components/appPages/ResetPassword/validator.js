import { addNewAlertItem } from "@/utils/alert";
import { isValidEmail } from "@/utils/validators";

export const formValidated = (dispatch, email, password, confirmPassword) => {
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
  if (password.length < 8) {
    validated = false;
    addNewAlertItem(
      dispatch,
      "error",
      "Password must be at least 8 characters long"
    );
    return validated;
  }
  if (password !== confirmPassword) {
    validated = false;
    addNewAlertItem(dispatch, "error", "Passwords do not match");
    return validated;
  }
  return validated;
};
