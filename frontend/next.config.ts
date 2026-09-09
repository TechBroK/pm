import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "export",
  distDir: "dist",
  // NOTE: rewrites() is silently ignored under output: "export" (static builds
  // can't run server-side proxy logic). The API base URL is instead injected
  // at build time via the NEXT_PUBLIC_API_URL env var — see src/lib/api.ts.
};

export default nextConfig;
