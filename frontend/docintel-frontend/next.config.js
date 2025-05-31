/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  experimental: {
    // Correct serverActions format
    serverActions: {
      enabled: true,
    },
    // Add other experimental features here
  },
  images: {
    domains: [],
  },
  typescript: {
    ignoreBuildErrors: false,
  },
  eslint: {
    ignoreDuringBuilds: false,
  },
  // Remove i18n if using App Router (see note below)
  // Remove swcMinify (now automatic in Next.js 15+)
};

export default nextConfig; // or module.exports for .js