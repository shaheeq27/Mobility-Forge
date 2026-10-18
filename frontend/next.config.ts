import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Keep Turbopack's project boundary inside this repository's frontend.
  // Tailwind CSS v4 is detected by Next.js; a custom CSS loader is unnecessary.
  turbopack: { root: __dirname },
  cacheComponents: true,
  partialPrefetching: true,
};

export default nextConfig;
