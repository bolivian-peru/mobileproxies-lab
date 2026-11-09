# Why curl can bypass an explicitly configured proxy

A short local demonstration of NO_PROXY overriding curl proxy selection, plus a checklist for comparing browser and command-line requests.

Published 2026-11-09 by Mobileproxies.org.

Adding --proxy to a curl command does not guarantee that the request uses that proxy. A matching NO_PROXY exclusion can send it directly. This is easy to miss when a shell, container or CI environment already defines exclusions.

The example below creates a destination handler and a proxy handler on random loopback ports. Both return a different label. It runs the same target URL twice: once with NO_PROXY=*, then with the command-line exclusion list explicitly cleared. Nothing leaves the computer.

```sh
python3 examples/curl-routing-demo.py
```

The expected output is:

```text
NO_PROXY=*: direct-handler
NO_PROXY=* with --noproxy "": proxy-handler
PASS: both routing decisions matched the expected handler.
This HTTP fixture does not forward traffic or test real proxy authentication.
```

The proxy handler is a stand-in. It answers the HTTP request itself, so this demonstration proves which handler curl selected. It does not implement HTTPS CONNECT, forward requests to another server or validate a paid proxy account.

## Make the comparison explicit

The example uses a clean child-process environment for proxy-selection variables and places -q first in the curl arguments to avoid reading a default curl configuration file. It keeps NO_PROXY=* set in both runs. The second run adds --noproxy with an empty value. The different result is therefore attributable to the exclusion override.

```sh
# Proxy host and fixture URL are placeholders.
# This exclusion applies to every host.
NO_PROXY='*' curl -q --proxy http://proxy.example:8080 \
  http://fixture.example/status

# Explicitly clear the exclusion list for this request.
NO_PROXY='*' curl -q --proxy http://proxy.example:8080 \
  --noproxy '' http://fixture.example/status
```

Real proxy credentials should be supplied through your existing secret-handling setup. Do not paste a username and password into a shared command transcript. Check whether both uppercase and lowercase proxy variables are present; curl treats http_proxy specially and only accepts its lowercase form. The official curl documentation explains the precedence and exclusions.

## Compare the actual clients

A browser extension can route the browser while a Node.js process, Python client or container uses a separate configuration. A successful browser request is useful evidence about that browser request. It does not verify the route of a different program.

- Use the same authorized target URL in both clients and note whether either follows redirects.
- Record which process owns the proxy setting: the browser, application client, shell environment or container.
- Check matching exclusions before replacing credentials or changing the proxy endpoint.
- Confirm the exit IP from each client through a diagnostic endpoint you control. Compare the address actually observed, not only the configured hostname.
- Separate proxy authentication errors from destination responses. An HTTP 407 concerns proxy authentication; a destination response needs its own context.

Keep failures in the comparison. A timeout, a direct request and a successful proxied request are three different outcomes. Hiding failed runs can make a configuration appear reliable when it is only intermittently used.

The [browser-versus-code proxy checklist](https://mobileproxies.org/blog/proxy-works-in-browser-not-in-code) provides a worksheet for these comparisons. The [general proxy testing guide](https://mobileproxies.org/blog/how-to-test-a-proxy) covers the evidence to collect before attributing a problem to a provider.

## Reference and source

See curl's [proxy environment variable documentation](https://everything.curl.dev/usingcurl/proxies/env.html) and [command-line reference](https://curl.se/docs/manpage.html). The complete [local routing demonstration](https://github.com/bolivian-peru/mobileproxies-lab/blob/main/examples/curl-routing-demo.py) includes assertions and closes both servers when it finishes. Mobileproxies.org maintains this example and sells mobile proxy services.
