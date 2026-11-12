/**
 * data-loader.js
 * Utility to load large JSON files without fetching them at runtime.
 */

let cache = {};

const isDev = process.env.NODE_ENV !== 'production';

export async function loadStaticText(filename, folder = 'data') {
  const cacheKey = `${folder}/${filename}`;
  if (!isDev && cache[cacheKey]) return cache[cacheKey];

  try {
    const isNode = typeof process !== 'undefined' && process.release && process.release.name === 'node';
    
    // 1. Build Time & SSR (Node.js/Vercel)
    if (isNode) {
      // Use eval to prevent Turbopack/Webpack from trying to bundle 27,000 files in public folder
      const req = eval('require');
      const fs = req('fs/promises');
      const path = req('path');
      const baseDir = process.cwd();

      // Candidate local paths on disk
      const candidatePaths = [
        folder ? `${baseDir}/public/${folder}/${filename}` : `${baseDir}/public/${filename}`,
        folder ? `${baseDir}/${folder}/${filename}` : `${baseDir}/${filename}`,
      ];

      // If it's a sermon markdown file, also check source sermon directories
      if (folder && folder.startsWith('data/sermons/')) {
        const parts = folder.split('/');
        const l = parts[2]; // en, pt, es
        const vol = parts[3]; // volume-XX
        const srcFolder = l === 'en' ? 'chspurgeon-sermons-main' : `chspurgeon-sermons-${l}`;
        candidatePaths.push(`${baseDir}/${srcFolder}/${vol}/${filename}`);
        if (filename.includes('-')) {
          candidatePaths.push(`${baseDir}/${srcFolder}/${vol}/${filename.replace(/-/g, '_')}`);
        }
      }

      // Try local filesystem candidates first
      for (const p of candidatePaths) {
        try {
          const fileContents = await fs.readFile(p, 'utf8');
          if (fileContents) {
            cache[cacheKey] = fileContents;
            return fileContents;
          }
        } catch (_) {}
      }

      // Fallback: fetch via HTTP from production CDN (with strict 4s timeout)
      if (process.env.VERCEL || process.env.NEXT_PUBLIC_SITE_URL || isDev === false) {
        const prodUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://www.spurgeon.tv';
        const fetchUrl = folder ? `${prodUrl}/${folder}/${filename}` : `${prodUrl}/${filename}`;
        try {
          const controller = typeof AbortController !== 'undefined' ? new AbortController() : null;
          const timeoutId = controller ? setTimeout(() => controller.abort(), 4000) : null;
          const res = await fetch(fetchUrl, {
            signal: controller ? controller.signal : undefined,
            cache: 'force-cache'
          });
          if (timeoutId) clearTimeout(timeoutId);
          if (res.ok) {
            const text = await res.text();
            cache[cacheKey] = text;
            return text;
          }
        } catch (fetchErr) {
          console.error(`[data-loader] Fetch fallback failed for ${fetchUrl}:`, fetchErr.message);
        }
      }

      console.error(`[data-loader] Error reading ${filename} locally or via fetch`);
      return null;
    } // close if(isNode)
    // 2. Client Side
    else {
      const filePathString = folder ? `/${folder}/${filename}` : `/${filename}`;
      const res = await fetch(filePathString);
      if (res.ok) {
        const text = await res.text();
        cache[cacheKey] = text;
        return text;
      }
    }
  } catch (error) {
    console.error(`[data-loader] Error reading ${filename}:`, error);
  }

  return null;
}

let jsonCache = {};

export async function loadStaticJson(filename, folder = 'data') {
  const cacheKey = `${folder}/${filename}`;
  if (!isDev && jsonCache[cacheKey]) return jsonCache[cacheKey];

  const text = await loadStaticText(filename, folder);
  if (text) {
    try {
      const parsed = JSON.parse(text);
      jsonCache[cacheKey] = parsed;
      return parsed;
    } catch (e) {
      console.error(`[data-loader] Failed to parse JSON for ${cacheKey}:`, e.message);
      return null;
    }
  }
  return null;
}
