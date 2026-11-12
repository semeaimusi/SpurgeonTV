import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..');

const baseUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://www.spurgeon.tv';
const langs = ['en', 'pt', 'es'];

// Helper to ensure trailing slash
const withTrailingSlash = (url) => url.endsWith('/') ? url : `${url}/`;

const sitemapMap = new Map();
const now = new Date().toISOString();

// Helper to add URL with deduplication
function addUrl(entry) {
  const normalizedUrl = withTrailingSlash(entry.url);
  sitemapMap.set(normalizedUrl, {
    ...entry,
    url: normalizedUrl
  });
}

// ── 1. High-Value Static & Hub Routes ────────────────────────────────────────
// Note: Low-value / utility routes (/volumes, /videos, /download) are disallowed in robots.txt
// and thus excluded from sitemap to prevent "Submitted URL blocked by robots.txt" in Google Search Console.
const staticRoutes = [
  { path: '',                    changeFreq: 'daily',   priority: 1.0 },
  { path: '/sermons',            changeFreq: 'weekly',  priority: 0.9 },
  { path: '/store',              changeFreq: 'weekly',  priority: 0.9 },
  { path: '/devotional',         changeFreq: 'daily',   priority: 0.9 },
  { path: '/bible',              changeFreq: 'weekly',  priority: 0.8 },
  { path: '/about',              changeFreq: 'weekly',  priority: 0.8 },
  { path: '/about-us',           changeFreq: 'monthly', priority: 0.7 },
  { path: '/about/biography',    changeFreq: 'weekly',  priority: 0.8 },
  { path: '/about/controversies',changeFreq: 'weekly',  priority: 0.8 },
  { path: '/about/preacher',     changeFreq: 'weekly',  priority: 0.8 },
  { path: '/about/theology',     changeFreq: 'weekly',  priority: 0.8 },
  { path: '/about/extra',        changeFreq: 'weekly',  priority: 0.8 },
  { path: '/dictionary',         changeFreq: 'weekly',  priority: 0.8 },
  { path: '/support',            changeFreq: 'monthly', priority: 0.5 },
  { path: '/transparency',       changeFreq: 'monthly', priority: 0.5 },
  { path: '/contact',            changeFreq: 'monthly', priority: 0.5 },
  { path: '/privacy-policy',     changeFreq: 'monthly', priority: 0.3 },
  { path: '/terms-of-service',   changeFreq: 'monthly', priority: 0.3 },
  { path: '/cookie-policy',      changeFreq: 'monthly', priority: 0.3 },
];

for (const route of staticRoutes) {
  const alternates = langs.map(l => ({
    lang: l,
    url: withTrailingSlash(`${baseUrl}/${l}${route.path}`)
  }));
  alternates.push({ lang: 'x-default', url: withTrailingSlash(`${baseUrl}/en${route.path}`) });

  for (const lang of langs) {
    addUrl({
      url: `${baseUrl}/${lang}${route.path}`,
      lastModified: now,
      changeFrequency: route.changeFreq,
      priority: route.priority,
      alternates
    });
  }
}

// ── 2. Volume Hubs (Volume 01 to Volume 63 × 3 languages) ────────────────────
// Route: /volume/volume-XX/ (allowed by robots.txt, distinct from /volumes)
for (let v = 1; v <= 63; v++) {
  const volId = `volume-${String(v).padStart(2, '0')}`;
  const alternates = langs.map(l => ({
    lang: l,
    url: withTrailingSlash(`${baseUrl}/${l}/volume/${volId}`)
  }));
  alternates.push({ lang: 'x-default', url: withTrailingSlash(`${baseUrl}/en/volume/${volId}`) });

  for (const lang of langs) {
    addUrl({
      url: `${baseUrl}/${lang}/volume/${volId}`,
      lastModified: now,
      changeFrequency: 'monthly',
      priority: 0.6,
      alternates
    });
  }
}

// ── 3. Articles (all categories & translated slugs) ───────────────────────────
const articlesIndexPath = path.join(ROOT, 'public', 'articles-index.json');
const articlesLibPath = path.join(ROOT, 'lib', 'articles-index.json');
const resolvedArticlesPath = fs.existsSync(articlesIndexPath) ? articlesIndexPath : articlesLibPath;

if (fs.existsSync(resolvedArticlesPath)) {
  const articlesIndex = JSON.parse(fs.readFileSync(resolvedArticlesPath, 'utf8'));
  
  const allHrefs = new Set();
  for (const l of langs) {
    for (const a of (articlesIndex[l] || [])) {
      if (a.href) allHrefs.add(a.href);
    }
  }

  for (const href of allHrefs) {
    const alternates = langs.map(l => ({
      lang: l,
      url: withTrailingSlash(`${baseUrl}/${l}${href}`)
    }));
    alternates.push({ lang: 'x-default', url: withTrailingSlash(`${baseUrl}/en${href}`) });

    for (const lang of langs) {
      const art = (articlesIndex[lang] || []).find(a => a.href === href);
      let lastMod = now;
      if (art && art.sortDate && !isNaN(art.sortDate)) {
        lastMod = new Date(art.sortDate).toISOString();
      }

      addUrl({
        url: `${baseUrl}/${lang}${href}`,
        lastModified: lastMod,
        changeFrequency: 'monthly',
        priority: 0.8,
        alternates
      });
    }
  }
}

// ── 4. Devotional (all 366 days × 3 languages) ───────────────────────────────
const d30 = [4, 6, 9, 11];
const daysInMonth = (m) => (m === 2 ? 29 : d30.includes(m) ? 30 : 31);

for (let month = 1; month <= 12; month++) {
  const days = daysInMonth(month);
  for (let day = 1; day <= days; day++) {
    const dateStr = `${month.toString().padStart(2, '0')}-${day.toString().padStart(2, '0')}`;
    const alternates = langs.map(l => ({
      lang: l,
      url: withTrailingSlash(`${baseUrl}/${l}/devotional/${dateStr}`)
    }));
    alternates.push({ lang: 'x-default', url: withTrailingSlash(`${baseUrl}/en/devotional/${dateStr}`) });

    for (const lang of langs) {
      addUrl({
        url: `${baseUrl}/${lang}/devotional/${dateStr}`,
        lastModified: now,
        changeFrequency: 'yearly',
        priority: 0.8,
        alternates
      });
    }
  }
}

// ── 5. Sermons (all volumes, standardized hyphens) ────────────────────────────
const searchIndexPath = path.join(ROOT, 'public', 'search-index.json');
const searchIndexLibPath = path.join(ROOT, 'lib', 'search-index.json');
const resolvedSearchPath = fs.existsSync(searchIndexPath) ? searchIndexPath : searchIndexLibPath;

if (fs.existsSync(resolvedSearchPath)) {
  const searchIndex = JSON.parse(fs.readFileSync(resolvedSearchPath, 'utf8'));
  for (const lang of langs) {
    const list = searchIndex[lang] || [];
    for (const item of list) {
      if (item.volume && item.slug) {
        // Enforce canonical hyphenated volume and slug (e.g. volume-01/sermon-1)
        const cleanVolume = item.volume.replace(/_/g, '-').toLowerCase();
        const cleanSlug = item.slug.replace(/_/g, '-').toLowerCase();
        addUrl({
          url: `${baseUrl}/${lang}/volume/${cleanVolume}/${cleanSlug}`,
          lastModified: now,
          changeFrequency: 'monthly',
          priority: 0.7,
        });
      }
    }
  }
}

// ── Build XML with multilingual xhtml:link alternates ─────────────────────────
let xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
`;

for (const item of sitemapMap.values()) {
  xml += `  <url>\n`;
  xml += `    <loc>${item.url}</loc>\n`;
  if (item.alternates && item.alternates.length > 0) {
    for (const alt of item.alternates) {
      xml += `    <xhtml:link rel="alternate" hreflang="${alt.lang}" href="${alt.url}"/>\n`;
    }
  }
  xml += `    <lastmod>${item.lastModified}</lastmod>\n`;
  xml += `    <changefreq>${item.changeFrequency}</changefreq>\n`;
  xml += `    <priority>${item.priority}</priority>\n`;
  xml += `  </url>\n`;
}

xml += `</urlset>\n`;

fs.writeFileSync(path.join(ROOT, 'public', 'sitemap.xml'), xml);
console.log(`✅ Sitemap generated at public/sitemap.xml (${sitemapMap.size} URLs)`);
