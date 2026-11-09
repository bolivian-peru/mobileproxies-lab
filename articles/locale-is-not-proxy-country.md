# A passing locale test does not prove your proxy changed country

Run a local Playwright example that separates browser locale, mocked geolocation and an application country label before adding a real proxy.

Published 2026-11-09 by Mobileproxies.org.

A browser can report fr-FR while the application still shows a different country. Our local example makes this distinction visible: it changes the browser locale and checks that the page continues to display FIXTURE as its country. The country is deliberately hard-coded. There is no proxy connection in this test.

That constraint gives the test a narrow job. If it passes, the locale setting reached the browser and the page displayed it. It has not established the country of an exit IP, the accuracy of a geolocation database or the routing used by a production application.

## Run the example before adding credentials

Clone this repository and run the example with Node.js 22.13 or later. The dependency lockfile pins the Playwright version used for the local checks.

```sh
git clone https://github.com/bolivian-peru/mobileproxies-lab.git
cd mobileproxies-lab/examples/regional-qa
npm ci
npx playwright install chromium
npm test
```

The server listens on 127.0.0.1:47127. Two tests create fresh browser contexts with fr-FR and de-DE locales. Each checks navigator.language through the fixture and confirms that the application country remains FIXTURE. A third test supplies mocked browser coordinates and checks those independently. A fourth, remote test is skipped unless MP_TEST_URL is set.

```ts
const context = await browser.newContext({ locale: 'fr-FR' });
try {
  const page = await context.newPage();
  await page.goto('http://127.0.0.1:47127/');
  await expect(page.getByTestId('browser-locale')).toHaveText('fr-FR');
  await expect(page.getByTestId('country-code')).toHaveText('FIXTURE');
} finally {
  await context.close();
}
```

## Give each assertion a source

The browser locale is a browser setting. Browser geolocation is a separate API whose result depends on permissions and the coordinates supplied by the browser or test environment. An exit IP belongs to the network path of a request. A storefront country is an application decision that may also use a cookie, account setting or selected delivery country.

| Observation | What this example establishes | What still needs checking |
| --- | --- | --- |
| navigator.language is fr-FR | The context uses the requested locale | The network exit and application country |
| Mocked coordinates match the configured values | The browser geolocation override works for the permitted origin | The real location of a network connection |
| The fixture country is FIXTURE | The application label stayed fixed | How a real application chooses its country |
| A remote page shows the expected country | That page rendered the expected label | Whether the label was selected from the proxy exit IP |

Start with a fresh browser context when comparing countries so that one test does not inherit another test's cookies. Keep the target page and account state consistent. Changing the proxy, language, timezone and saved country at once makes a failure harder to attribute.

## Add a real proxy as a separate check

The remote example reads the proxy server, username and password from separate environment variables. It opens an authorized HTTPS fixture and checks an element named country-code. Before trusting the result as an IP-based regional check, record the actual exit IP from the same proxied context using a diagnostic endpoint you control. A standalone curl request can use a different route and cannot establish what the browser did.

No authenticated remote proxy was used to validate this example. The local checks are reproducible demonstrations of browser inputs. For a real application, also define the expected currency, delivery region, language and regional content, then test the inputs that drive each one.

The [Mobileproxies.org Playwright regional testing guide](https://mobileproxies.org/blog/playwright-geolocation-testing) includes the broader application testing checklist. If the browser is routed correctly but a lookup reports the wrong country, use the [country-mismatch diagnostic guide](https://mobileproxies.org/blog/proxy-location-wrong-country) to compare the same exit address across the relevant signals.

## Reference and source

Playwright documents [browser emulation settings](https://playwright.dev/docs/emulation) and [HTTP proxy configuration](https://playwright.dev/docs/network#http-proxy) separately. The runnable source is in [examples/regional-qa](https://github.com/bolivian-peru/mobileproxies-lab/tree/main/examples/regional-qa). This article is maintained by Mobileproxies.org, which sells mobile proxy services.
