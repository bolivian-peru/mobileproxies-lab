import { test, expect } from '@playwright/test';
for (const locale of ['fr-FR', 'de-DE']) {
  test(`locale ${locale} does not change the fixture country`, async ({ browser }) => {
    const context = await browser.newContext({ locale, timezoneId: 'Europe/Paris' });
    try {
      const page = await context.newPage();
      await page.goto('http://127.0.0.1:47127/');
      await expect(page.getByTestId('country-code')).toHaveText('FIXTURE');
      await expect(page.getByTestId('browser-locale')).toHaveText(locale);
    } finally { await context.close(); }
  });
}
test('browser geolocation is an independent mocked input', async ({ browser }) => {
  const context = await browser.newContext({
    locale: 'en-GB', geolocation: { latitude: 51.5074, longitude: -0.1278 },
  });
  try {
    await context.grantPermissions(['geolocation'], { origin: 'http://127.0.0.1:47127' });
    const page = await context.newPage();
    await page.goto('http://127.0.0.1:47127/');
    const coords = await page.evaluate(() => new Promise<{ latitude: number; longitude: number }>((resolve, reject) => {
      navigator.geolocation.getCurrentPosition(p => resolve({ latitude: p.coords.latitude, longitude: p.coords.longitude }), reject, { timeout: 5000 });
    }));
    expect(coords.latitude).toBeCloseTo(51.5074, 4);
    expect(coords.longitude).toBeCloseTo(-0.1278, 4);
    await expect(page.getByTestId('country-code')).toHaveText('FIXTURE');
  } finally { await context.close(); }
});
