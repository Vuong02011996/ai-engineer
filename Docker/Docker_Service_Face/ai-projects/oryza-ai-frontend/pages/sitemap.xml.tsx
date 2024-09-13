const globby = require("globby");

function generateSiteMap(pages: any) {
  return `<?xml version="1.0" encoding="UTF-8"?>
   <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
     <!--We manually set the two URLs we know already-->
     ${pages.map(addPage).join("\n")} 
   </urlset>
 `;
}
function addPage(page: any) {
  const path = page
    .replace("pages", "")
    .replace("index.tsx", "")
    .replace(".js", "")
    .replace(".tsx", "")
    .replace(".mdx", "");
  const route = path === "/index" ? "" : path;
  return `
    <url>
        <loc>${`${process.env.WEBSITE_URL}${route}`}</loc>
        <lastmod>${new Date().toISOString()}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>1.0</priority>
    </url>`;
}

async function getAllPage() {
  // excludes Nextjs files and API routes.
  const pages = await globby([
    "pages/**/*{.ts,.tsx}",
    "!pages/_*.ts",
    "!pages/api",
    "!pages/_app.tsx",
    "!pages/_document.tsx",
    "!pages/news/[slug].tsx",
    "!pages/**/[camera_name].tsx",
  ]);

  return pages;
}

function SiteMap() {
  // getServerSideProps will do the heavy lifting pages.map(addPage).join('\n')
}

export async function getServerSideProps({ res }: any) {
  // We generate the XML sitemap with the posts data
  const pages = await getAllPage();
  const sitemap = generateSiteMap(pages);

  res.setHeader("Content-Type", "text/xml");
  // we send the XML to the browser
  res.write(sitemap);
  res.end();

  return {
    props: {},
  };
}

export default SiteMap;
