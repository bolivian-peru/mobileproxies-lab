import { createServer } from 'node:http';
const server = createServer((req, res) => {
  if (req.url === '/health') { res.writeHead(200); res.end('ok'); return; }
  res.writeHead(200, { 'content-type': 'text/html; charset=utf-8' });
  res.end(`<!doctype html><html lang="en"><meta charset="utf-8"><title>Regional QA fixture</title><main><h1>Local QA fixture</h1><p>This fixture uses a fixed country value. It does not locate an IP.</p><span data-testid="country-code">FIXTURE</span><span data-testid="browser-locale"></span><script>document.querySelector('[data-testid="browser-locale"]').textContent = navigator.language;</script></main></html>`);
});
server.listen(47127, '127.0.0.1');
for (const signal of ['SIGINT', 'SIGTERM']) process.on(signal, () => server.close(() => process.exit(0)));
