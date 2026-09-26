import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./pruebas",
  workers: 1,
  reporter: "list",
  use: {
    baseURL: "http://127.0.0.1:8000",
  },
  projects: [
    { name: "chromium", use: { ...devices["Desktop Chrome"] } },
    { name: "firefox", use: { ...devices["Desktop Firefox"] } },
    { name: "webkit", use: { ...devices["Desktop Safari"] } },
  ],
  webServer: {
    command: "uv run python servidor_de_prueba.py",
    cwd: "..",
    url: "http://127.0.0.1:8000",
    reuseExistingServer: false,
    env: { LATENCIA_MAXIMA: "0.4" },
  },
});
