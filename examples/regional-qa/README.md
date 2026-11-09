# Regional QA example

Run `npm ci`, `npx playwright install chromium`, then `npm test` from this directory.

The local fixture binds to `127.0.0.1:47127`. The runner refuses to reuse an occupied port. Identify an existing listener before changing ports; do not stop another service to make this example run.

Three local checks compare French and German browser locales and a mocked browser location with a fixed country label. `FIXTURE` is not an IP geolocation result. Passing these checks does not demonstrate proxy routing.

The remote test is skipped until `MP_TEST_URL` is provided. It requires an HTTPS application you own or are authorized to test, containing an element with `data-testid="country-code"`. Adapt the selector to your application. The test compares its text with `MP_EXPECTED_COUNTRY`.

Provide these variables through your environment or secret manager:

| Variable | Meaning |
| --- | --- |
| `MP_PROXY_SERVER` | HTTP proxy scheme, host and port, without embedded credentials |
| `MP_PROXY_USERNAME` | Issued proxy username |
| `MP_PROXY_PASSWORD` | Issued proxy password |
| `MP_TEST_URL` | Authorized HTTPS application URL, without credentials or sensitive query tokens |
| `MP_EXPECTED_COUNTRY` | Exact expected country label |
| `MP_LOCALE` | Browser locale, default `en-GB` |
| `MP_TIMEZONE` | Browser timezone, default `Europe/London` |

`.env.example` lists the names; the test does not load an `.env` file automatically. Treat the target URL as potentially visible in test failures. Restrict who can edit code that runs with proxy secrets. Review any artifacts before enabling traces or screenshots.

The remote check verifies one application label. Record the actual exit IP from the same proxied browser context through a diagnostic endpoint you control before attributing that label to IP routing. Locale, saved preferences, account settings and browser geolocation can also influence a site's behavior.

For a fuller testing matrix, see the [Playwright regional testing guide](https://mobileproxies.org/blog/playwright-geolocation-testing).
