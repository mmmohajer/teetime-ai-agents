/** @type {import('next-sitemap').IConfig} */
module.exports = {
  siteUrl: "https://makeclient.ngrok.io",
  generateRobotsTxt: true,
  exclude: ["/admin*", "/api/*", "/app", "/app/*", "/_next/*"],
  robotsTxtOptions: {
    policies: [{ userAgent: "*", allow: "/" }],
  },
};
