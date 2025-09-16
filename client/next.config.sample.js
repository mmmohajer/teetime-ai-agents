/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,

  webpack: (config, { dev, isServer }) => {
    if (dev && isServer) {
      config.watchOptions = {
        poll: 1000,
        aggregateTimeout: 300,
      };
    }
    return config;
  },

  env: {
    APP_DOMAIN: "makeclient.ngrok.io",
    GA_TRACKING_ID: "",
    GOOGLE_AUTH_CLIENT_ID: "",
    ICE_SERVER_DOMAIN: "IP_ADDRESS_OR_DOMAIN",
    TURN_USER_NAME: "TURN_USER_NAME",
    TURN_USER_PASSWORD: "TURN_USER_PASSWORD",
  },

  publicRuntimeConfig: {
    PRODUCTION: false,
    IS_STAGING_OR_DEVELOPMENT: true,
    WITH_DOCKER: true,
  },

  images: {
    domains: ["localhost", "makeclient.ngrok.io", "picsum.photos"],
  },
};

module.exports = nextConfig;
