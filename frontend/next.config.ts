import type { NextConfig } from 'next';

const config: NextConfig = {
  async rewrites() {
    const backend = process.env.AGENT_BACKEND_URL;
    if (!backend) return [];
    return [
      { source: '/api/run/:path*', destination: `${backend}/api/:path*` },
    ];
  },
};

export default config;

