import getConfig from "next/config";
const { publicRuntimeConfig } = getConfig();

export const PRODUCTION = publicRuntimeConfig.PRODUCTION;
export const IS_STAGING_OR_DEVELOPMENT =
  publicRuntimeConfig.IS_STAGING_OR_DEVELOPMENT;
export const WITH_DOCKER = publicRuntimeConfig.WITH_DOCKER;
export const APP_DOMAIN = process.env.APP_DOMAIN;
export const APP_DOMAIN_FOR_CLIENT_SIDE =
  process.env.APP_DOMAIN === "localhost"
    ? "http://localhost:3000"
    : `https://${process.env.APP_DOMAIN}`;
export const APP_DOMAIN_FOR_SERVER_SIDE_PROPS =
  process.env.APP_DOMAIN === "localhost"
    ? "http://localhost:8000"
    : `https://${process.env.APP_DOMAIN}`;
export const STORAGE_BASE_URL =
  "https://techtipsbymoh.tor1.cdn.digitaloceanspaces.com";
export const GA_TRACKING_ID = process.env.GA_TRACKING_ID;
export const GOOGLE_AUTH_CLIENT_ID = process.env.GOOGLE_AUTH_CLIENT_ID;
export const ICE_SERVER_DOMAIN = process.env.ICE_SERVER_DOMAIN;
export const TURN_USER_NAME = process.env.TURN_USER_NAME;
export const TURN_USER_PASSWORD = process.env.TURN_USER_PASSWORD;
