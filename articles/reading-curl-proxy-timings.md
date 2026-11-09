# Read curl timings without calling everything proxy latency

Record curl timing milestones and failures consistently, distinguish connection and transfer measurements, and avoid claiming a proxy benchmark from a single page load.

Published 2026-11-09 by Mobileproxies.org.

A two-second request through a proxy is a two-second request. That number alone does not identify how much time was spent on the proxy connection, the destination or downloading the response. Start by recording the request configuration and curl's timing milestones together.

This repository includes a write-out format that emits response status, connection timings, response size and average download speed as JSON. The example is a collection format, not a published provider benchmark.

## Record the same fields for each attempt

Use a stable HTTPS fixture you own or are authorized to test. Put the proxy settings in an ignored configuration file with restricted permissions, populated through your normal secret workflow. The example filename proxy.curlrc is ignored by this repository. Keep credentials out of the destination URL.

```sh
chmod 600 proxy.curlrc
curl -q --config proxy.curlrc \
  --noproxy '' --silent --show-error \
  --connect-timeout 10 --max-time 30 \
  --output /dev/null \
  --write-out @examples/curl-timing-format.txt \
  https://your-authorized-fixture.example/status
curl_status=$?
printf 'curl_exit_code=%s\n' "$curl_status"
```

The configuration file should contain only the intended proxy settings. Do not add verbose tracing, saved response bodies or redirects without considering what they change or expose. The shell variable captures the exit status immediately after curl; the JSON response code by itself is not enough to classify every failed transfer.

## Interpret the fields as milestones

| Field in the format | How to read it |
| --- | --- |
| dns_s | Elapsed time to the name-resolution milestone. The name resolved depends on the proxy protocol and route. |
| connect_s | Elapsed time to the connection milestone. With an explicit proxy, the connection can be to the proxy rather than the origin. |
| tls_s | Elapsed time to the TLS handshake milestone for a supported secure transfer. A zero value is not proof of a zero-cost handshake. |
| first_byte_s | Elapsed time to the first response byte, including preceding setup and server work. |
| total_s | Elapsed time for the full operation, including transfer of the response. |
| download_bytes_per_second | Average download speed reported by curl, in bytes per second, not megabits per second. |
| remote_ip | The peer curl connected to. In a proxied request this can be the proxy endpoint, not the internet exit IP visible to the destination. |

Most timing values above are cumulative. Adding them together double-counts earlier stages. Subtracting milestones can help investigate a simple, fresh connection, but a redirect chain, reused connection or another protocol arrangement changes what the differences mean. Record those conditions before comparing runs.

## Keep the destination and failures in the result

A small HTML response and a large download answer different questions. A remote endpoint that caches responses also differs from an application doing database work. Hold the fixture, response size, client version and connection policy steady when comparing two routes. Run modest, sequential samples rather than increasing concurrency without a defined need.

Record timeouts and non-success HTTP responses alongside successful runs. Report the number of attempts and the failure rate before describing a typical successful duration. A handful of samples can help reproduce a symptom, but it is too little evidence for broad claims about carrier speed or reliability.

To establish the exit IP, use the address observed by an authorized destination. The remote_ip field in this format has a different job: it identifies curl's connected peer. Confusing the two can lead to a misleading country or latency conclusion.

The [mobile proxy speed-testing guide](https://mobileproxies.org/blog/mobile-proxy-speed-test) includes a worksheet for recording the test conditions and outcomes. Use the [capacity-planning guide](https://mobileproxies.org/blog/mobile-proxy-capacity-planning) when the question is how many concurrent jobs a workload can sustain.

## Reference and source

curl documents [write-out formatting](https://everything.curl.dev/usingcurl/verbose/writeout.html) and the [individual timing variables](https://curl.se/docs/manpage.html). The format file is [available in this repository](https://github.com/bolivian-peru/mobileproxies-lab/blob/main/examples/curl-timing-format.txt). Mobileproxies.org maintains the lab and sells mobile proxy services. No real carrier speed measurement is claimed here.
