import type { NextConfig } from 'next';

const config: NextConfig = {
  reactStrictMode: true,
  experimental: {},
  // Completely disable the feedback widget
  devIndicators: false
};

export default config;
