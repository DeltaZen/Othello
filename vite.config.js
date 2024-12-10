import { webxdcViteConfig } from "@webxdc/vite-plugins";
import { watch } from "vite-plugin-watch"
import { defineConfig } from "vite";

const config = webxdcViteConfig()
config.plugins.push({
  ...watch({
    pattern: "**/*.py",
    command: "pnpm build:py",
  }),
  apply: "serve",
})

// https://vitejs.dev/config/
export default defineConfig(config);
