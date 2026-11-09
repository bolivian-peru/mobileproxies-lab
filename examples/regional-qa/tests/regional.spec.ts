import { test, expect } from '@playwright/test';
test('authorized regional page returns the expected country', async ({ browser }) => {
  test.skip(!process.env.MP_TEST_URL, 'Set MP_TEST_URL to your authorized fixture to run the proxy test.');
  for (const key of ['MP_PROXY_SERVER', 'MP_PROXY_USERNAME', 'MP_PROXY_PASSWORD', 'MP_EXPECTED_COUNTRY']) {
    if (!process.env[key]) throw new Error(`Missing ${key}`);
  }
  const target = new URL(process.env.MP_TEST_URL!);
  if (target.protocol !== 'https:') throw new Error('The remote test fixture must use HTTPS.');
  if (target.username || target.password) throw new Error('Keep authentication out of the fixture URL.');
  const context = await browser.newContext({
    proxy: {
      server: process.env.MP_PROXY_SERVER!,
      username: process.env.MP_PROXY_USERNAME!,
      password: process.env.MP_PROXY_PASSWORD!,
    },
    locale: process.env.MP_LOCALE || 'en-GB',
    timezoneId: process.env.MP_TIMEZONE || 'Europe/London',
  });
  try {
    const page = await context.newPage();
    const response = await page.goto(target.toString(), { waitUntil: 'domcontentloaded', timeout: 30_000 });
    expect(response?.ok()).toBeTruthy();
    await expect(page.getByTestId('country-code')).toHaveText(process.env.MP_EXPECTED_COUNTRY!);
  } finally { await context.close(); }
});
