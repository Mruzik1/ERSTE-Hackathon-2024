/** @type {import('next').NextConfig} */
const nextConfig = {
    webpack: (config, { isServer }) => {
      config.module.rules.push({
        test: /\.(glb|gltf)$/,
        use: {
          loader: 'file-loader',
          options: {
            outputPath: 'static/models/',
            publicPath: '/_next/static/models/',
          },
        },
      });
  
      return config;
    },
  };
  
  module.exports = nextConfig;
  