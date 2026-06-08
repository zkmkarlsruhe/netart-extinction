import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://extinction.zkm.de',
  output: 'static',
  integrations: [sitemap()],
});
