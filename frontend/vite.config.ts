import tailwindcss from "@tailwindcss/vite";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vitest/config";

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    // Same origin for the browser, so no CORS. 127.0.0.1 instead of localhost, because
    // Node resolves localhost to ::1 first, while uvicorn listens on 127.0.0.1 only.
    // Docker Compose overrides the target with the service name (http://backend:8000).
    proxy: {
      "/api": process.env.API_PROXY_TARGET ?? "http://127.0.0.1:8000",
    },
    // File change events from a Windows host do not reach Vite inside a container.
    watch: { usePolling: process.env.VITE_USE_POLLING === "true" },
  },
  test: {
    environment: "jsdom",
    setupFiles: ["./src/test/setup.ts"],
  },
});
