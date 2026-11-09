# Mobileproxies Lab

Runnable examples for checking proxy routing and regional browser behavior. Maintained by [Mobileproxies.org](https://mobileproxies.org/), a commercial mobile proxy provider. These examples also work as learning material without a proxy subscription.

[Read the lab articles](https://bolivian-peru.github.io/mobileproxies-lab/).

## Start without proxy credentials

Run the curl routing demonstration with Python 3.9+ and curl:

```sh
python3 examples/curl-routing-demo.py
```

It creates two short-lived HTTP fixtures on random loopback ports. One represents the direct destination and the other a proxy handler. It demonstrates how `NO_PROXY=*` can bypass an explicit `--proxy`, then how `--noproxy ""` changes that decision. The handler does not forward traffic.

The Playwright example requires Node.js 22.13+:

```sh
cd examples/regional-qa
npm ci
npx playwright install chromium
npm test
```

Three local tests cover locale and browser geolocation. A remote proxy test is skipped until its environment variables are supplied. Local passes do not prove a real proxy's exit country, latency or availability.

## Articles

- [A passing locale test does not prove your proxy changed country](https://bolivian-peru.github.io/mobileproxies-lab/locale-is-not-proxy-country/)
- [Why curl can bypass an explicitly configured proxy](https://bolivian-peru.github.io/mobileproxies-lab/curl-no-proxy-routing/)
- [Read curl timings without calling everything proxy latency](https://bolivian-peru.github.io/mobileproxies-lab/reading-curl-proxy-timings/)

The examples extend the [regional testing starter](https://mobileproxies.org/blog/playwright-geolocation-testing) and [proxy troubleshooting guides](https://mobileproxies.org/blog/how-to-test-a-proxy) published on Mobileproxies.org.

## Run the remote example

Read [the regional example instructions](examples/regional-qa/README.md). Use a fixture you own or have permission to test. Credentials belong in your environment or secret manager. The project does not automatically load `.env` files. Traces, screenshots and videos are disabled by default.

## Build the documentation

```sh
python3 scripts/build.py
```

The build uses the Python standard library and writes static HTML, an RSS feed and a sitemap to `docs/`. GitHub Pages serves `docs/` from the `main` branch. Article source is in `content/articles.json`; Markdown copies are generated under `articles/`.

## Validation boundaries

The local tests were run with Playwright 1.64.1 and Chromium. No paid proxy rental or authenticated remote fixture was used to validate the remote example. This project publishes no carrier speed benchmarks and makes no claim about destination acceptance.
