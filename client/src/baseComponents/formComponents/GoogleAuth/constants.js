import { APP_DOMAIN_FOR_CLIENT_SIDE, GOOGLE_AUTH_CLIENT_ID } from "config";

const GOOGLE_AUTH_BASE_URL = "https://accounts.google.com/o/oauth2/v2/auth";
const GOOGLE_AUTH_SCOPE_PROFILE_URL =
  "https://www.googleapis.com/auth/userinfo.profile";
const GOOGLE_AUTH_SCOPE_EMAIL_URL =
  "https://www.googleapis.com/auth/userinfo.email";
const GOOGLE_AUTH_SCOPE_OPEN_ID = "openid";
const GOOGLE_AUTH_REDIRECT_URL = `${APP_DOMAIN_FOR_CLIENT_SIDE}/app/google-auth/`;

export const GOOGLE_AUTH_URL = `${GOOGLE_AUTH_BASE_URL}?scope=${GOOGLE_AUTH_SCOPE_PROFILE_URL} ${GOOGLE_AUTH_SCOPE_EMAIL_URL} ${GOOGLE_AUTH_SCOPE_OPEN_ID}&access_type=offline&include_granted_scopes=true&response_type=code&state=state_parameter_passthrough_value&redirect_uri=${GOOGLE_AUTH_REDIRECT_URL}&client_id=${GOOGLE_AUTH_CLIENT_ID}`;
