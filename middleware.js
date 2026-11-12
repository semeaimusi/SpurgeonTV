import { NextResponse } from 'next/server';

const PUBLIC_FILE = /\.(.*)$/;
const LOCALES = ['en', 'pt', 'es'];

export function middleware(request) {
  const { pathname } = request.nextUrl;
  const host = request.headers.get('host') || '';

  // 0. Canonical host redirect: naked domain spurgeon.tv -> www.spurgeon.tv
  if (host === 'spurgeon.tv') {
    const targetUrl = new URL(request.url);
    targetUrl.host = 'www.spurgeon.tv';
    targetUrl.protocol = 'https:';
    return NextResponse.redirect(targetUrl, 301);
  }

  // 1. Redirect legacy Blogger posts (e.g. /2011/09/post.html) to /pt/sermons/
  if (/^\/\d{4}\/\d{2}\/.*\.html$/i.test(pathname)) {
    return NextResponse.redirect(new URL('/pt/sermons/', request.url), 301);
  }

  // 2. Redirect legacy Blogger RSS feeds (e.g. /feeds/posts/default) to /pt/sermons/
  if (pathname.startsWith('/feeds')) {
    return NextResponse.redirect(new URL('/pt/sermons/', request.url), 301);
  }

  // Ignore API routes, public files (except html), and Next.js internals
  if (
    pathname.startsWith('/_next') ||
    pathname.startsWith('/api') ||
    (PUBLIC_FILE.test(pathname) && !pathname.endsWith('.html'))
  ) {
    return NextResponse.next();
  }

  // 3. Normalization of Volume & Sermon URLs (301 Permanent Redirect)
  // Handles:
  // - Non-www host redirect
  // - Unpadded volume: /volume/14/ -> /pt/volume/volume-14/
  // - Single digit: /volume/volume-4/ -> /pt/volume/volume-04/
  // - Bare volume number: /es/volume/55 -> /es/volume/volume-55/
  // - Underscores: /volume/volume-27/sermon_1586/ -> /volume/volume-27/sermon-1586/
  // - Uppercase: /volume/volume-25/sermon_1451A/ -> /volume/volume-25/sermon-1451a/
  // - Missing trailing slash: /sermon-443 -> /sermon-443/
  // - Missing locale: /volume/volume-01/sermon-10/ -> /pt/volume/volume-01/sermon-10/
  const volSermonMatch = pathname.match(
    /^(?:\/(en|pt|es))?\/volume\/(?:volume-)?0*([1-9][0-9]?)(?:\/(sermon[_-][^/]+))?\/?$/i
  );

  if (volSermonMatch) {
    const [, matchedLang, volNumStr, sermonSlug] = volSermonMatch;
    const acceptLanguage = request.headers.get('accept-language') || '';
    let lang = matchedLang;
    if (!lang) {
      if (acceptLanguage.includes('es')) lang = 'es';
      else if (acceptLanguage.includes('en')) lang = 'en';
      else lang = 'pt';
    }

    const volNum = parseInt(volNumStr, 10);
    if (volNum >= 1 && volNum <= 63) {
      const canonicalVol = `volume-${String(volNum).padStart(2, '0')}`;
      let canonicalPath;
      if (sermonSlug) {
        const canonicalSermon = sermonSlug.replace(/_/g, '-').toLowerCase();
        canonicalPath = `/${lang}/volume/${canonicalVol}/${canonicalSermon}/`;
      } else {
        canonicalPath = `/${lang}/volume/${canonicalVol}/`;
      }

      // If the incoming path is not strictly identical to the canonical path, 301 redirect
      if (pathname !== canonicalPath) {
        return NextResponse.redirect(new URL(canonicalPath, request.url), 301);
      }
    }
  }

  // Check if the pathname already has a supported locale
  const pathnameHasLocale = LOCALES.some(
    (locale) => pathname.startsWith(`/${locale}/`) || pathname === `/${locale}`
  );
  
  if (pathnameHasLocale) {
    return NextResponse.next();
  }

  // Explicit redirect for /store or /store/ directly to /en/store/
  if (pathname === '/store' || pathname === '/store/') {
    return NextResponse.redirect(new URL('/en/store/', request.url), 301);
  }

  // 4. Default locale redirect for general URLs without locale
  const acceptLanguage = request.headers.get('accept-language') || '';
  let locale = 'en';
  if (acceptLanguage.includes('pt')) {
    locale = 'pt';
  } else if (acceptLanguage.includes('es')) {
    locale = 'es';
  }

  // Redirect to the same path but with the locale prefixed
  request.nextUrl.pathname = `/${locale}${pathname}`;
  return NextResponse.redirect(request.nextUrl, 307);
}

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
};
