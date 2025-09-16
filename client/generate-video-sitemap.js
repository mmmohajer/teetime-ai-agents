const fs = require("fs");
const axios = require("axios");
const path = require("path");

const siteUrl = "https://tipsbymoh.tech";
const apiUrl = `${siteUrl}/api/tips/`; // assuming all videos are in tips

(async () => {
  try {
    const res = await axios.get(apiUrl);
    const items = res.data?.tips || [];

    const urls = items
      .filter((item) => item.video && item.preview_photo && item.slug)
      .map((item) => {
        const pageUrl = `${siteUrl}/tips/${item.slug}`;
        const title = item.title;
        const description = item.title;
        const thumbnail = item.preview_photo;
        const videoUrl = item.video;

        return `
<url>
  <loc>${pageUrl}</loc>
  <video:video>
    <video:thumbnail_loc>${thumbnail}</video:thumbnail_loc>
    <video:title><![CDATA[${title}]]></video:title>
    <video:description><![CDATA[${description}]]></video:description>
    <video:content_loc>${videoUrl}</video:content_loc>
  </video:video>
</url>`;
      });

    const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
  xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">
  ${urls.join("\n")}
</urlset>`;

    const outPath = path.join(__dirname, "./public/sitemap-video.xml");
    fs.writeFileSync(outPath, xml.trim());

    console.log("✅ Video sitemap generated at:", outPath);
  } catch (err) {
    console.error("❌ Failed to generate video sitemap:", err.message);
  }
})();
