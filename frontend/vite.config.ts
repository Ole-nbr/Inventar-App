import react from "@vitejs/plugin-react";
import { defineConfig } from "vitest/config";

export default defineConfig({
  plugins: [react()],
  server: {
    // Same origin for the browser, so no CORS. 127.0.0.1 instead of localhost, because
    // Node resolves localhost to ::1 first, while uvicorn listens on 127.0.0.1 only.
    proxy: { "/api": "http://127.0.0.1:8000" },
  },
  test: {
    environment: "jsdom",
    setupFiles: ["./src/test/setup.ts"],
  },
});
