import { defineConfig, devices } from "@playwright/test";
export default defineConfig({
  testDir: "./tests", testMatch: "**/*.spec.ts", fullyParallel: false, workers: 1, timeout: 90_000,
  use: { baseURL: process.env.BASE_URL || "http://127.0.0.1:3000", trace: "retain-on-failure", actionTimeout: 15_000 },
  projects: [{ name: "chromium", use: { ...devices["Desktop Chrome"] } }],
});
