/** @type {import('next').NextConfig} */
const nextConfig = {
  trailingSlash: true,
  compress: true,
  poweredByHeader: false,
  images: {
    unoptimized: true,
  },
  typescript: {
    ignoreBuildErrors: true,
  },
  outputFileTracingIncludes: {
    '/[lang]/volume/[id]/[sermonId]': [
      './public/data/sermons/**/*',
      './public/data/*.json',
      './public/*.json',
      './chspurgeon-sermons-*/**/*',
    ],
    '/[lang]/volume/[id]': [
      './public/data/sermons/**/*',
      './public/data/*.json',
      './public/*.json',
    ],
  },
  output: process.env.BUILD_STANDALONE ? 'standalone' : undefined,

  async headers() {
    return [
      {
        // Global security headers
        source: '/(.*)',
        headers: [
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'X-Frame-Options',
            value: 'SAMEORIGIN',
          },
          {
            key: 'Referrer-Policy',
            value: 'strict-origin-when-cross-origin',
          },
        ],
      },
      {
        // Bibles JSON: cache for 7 days, revalidate up to 30 days
        source: '/bibles/:path*',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=604800, stale-while-revalidate=2592000',
          },
        ],
      },
      {
        // Paginated sermon data: cache for 24h, revalidate up to 7 days
        source: '/data/:path*',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=86400, stale-while-revalidate=604800',
          },
        ],
      },
      {
        source: '/search-index.json',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=86400, stale-while-revalidate=604800',
          },
        ],
      },
      {
        source: '/sitemap.xml',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=86400, stale-while-revalidate=604800',
          },
        ],
      },
    ];
  },

  async redirects() {
    return [
      {
        source: '/:lang/about/biography/allan-roman',
        destination: '/:lang/about/extra/allan-roman',
        permanent: true,
      },
      {
        source: '/:lang/about/biography/allan-roman/',
        destination: '/:lang/about/extra/allan-roman/',
        permanent: true,
      },
    ];
  },
};

export default nextConfig;
