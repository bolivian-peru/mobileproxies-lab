import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: './tests',
  timeout: 45_000,
  workers: 1,
  retries: 0,
  reporter: 'list',
  use: { browserName: 'chromium', trace: 'off', screenshot: 'off', video: 'off' },
  webServer: {
    command: 'node fixture.mjs',
    url: 'http://127.0.0.1:47127/health',
    reuseExistingServer: false,
    timeout: 20_000,
  },
});
