#!/usr/bin/env python3
"""Build the lab's static documentation and Markdown article copies."""
from pathlib import Path
from html import escape
from urllib.parse import urlsplit
import json
import re
import textwrap

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs'
BASE = 'https://bolivian-peru.github.io/mobileproxies-lab'
PREFIX = '/mobileproxies-lab'
DATE = '2026-11-09'
ARTICLES = json.loads((ROOT / 'content/articles.json').read_text())


def inline(text):
    parts = []
    cursor = 0
    for match in re.finditer(r'\[([^\]]+)\]\((https://[^\s)]+)\)', text):
        parts += [escape(text[cursor:match.start()]), f'<a href="{escape(match[2], quote=True)}">{escape(match[1])}</a>']
        cursor = match.end()
    return ''.join(parts) + escape(text[cursor:])


def render(block):
    kind, *body = block
    if kind in ['p', 'h2']:
        return f'<{kind}>{inline(body[0])}</{kind}>'
    if kind == 'code':
        return f'<pre tabindex="0" aria-label="Code example"><code class="language-{escape(body[0])}">{escape(body[1])}</code></pre>'
    if kind == 'list':
        return '<ul>' + ''.join('<li>' + inline(x) + '</li>' for x in body[0]) + '</ul>'
    if kind == 'table':
        return '<div class="table-wrap" tabindex="0" role="region" aria-label="Comparison table"><table><thead><tr>' + ''.join('<th scope="col">'+inline(x)+'</th>' for x in body[0]) + '</tr></thead><tbody>' + ''.join('<tr>'+''.join('<td>'+inline(x)+'</td>' for x in row)+'</tr>' for row in body[1]) + '</tbody></table></div>'
    raise ValueError(kind)


def markdown(article):
    parts = ['# ' + article['title'], article['description'], 'Published ' + article['date'] + ' by Mobileproxies.org.']
    for kind, *body in article['blocks']:
        if kind == 'p':parts.append(body[0])
        elif kind == 'h2':parts.append('## '+body[0])
        elif kind == 'code':parts.append('```'+body[0]+'\n'+body[1]+'\n```')
        elif kind == 'list':parts.append('\n'.join('- '+x for x in body[0]))
        elif kind == 'table':parts.append('| '+' | '.join(body[0])+' |\n| '+' | '.join(['---']*len(body[0]))+' |\n'+'\n'.join('| '+' | '.join(row)+' |' for row in body[1]))
    return '\n\n'.join(parts)+'\n'


def page(title, description, path, body, article=None):
    url = BASE + path
    image = BASE + '/assets/' + (article['slug'] if article else 'lab') + '.png'
    structured = {'@context':'https://schema.org','@type':'TechArticle' if article else 'CollectionPage','headline':title,'description':description,'url':url,'author':{'@type':'Organization','name':'Mobileproxies.org','url':'https://mobileproxies.org/'},'image':image}
    if article:structured.update(datePublished=article['date'],dateModified=article['date'],mainEntityOfPage=url)
    data=json.dumps(structured).replace('<','\\u003c')
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)} | Mobileproxies Lab</title><meta name="description" content="{escape(description,quote=True)}"><link rel="canonical" href="{url}"><link rel="stylesheet" href="{PREFIX}/assets/style.css"><link rel="alternate" type="application/rss+xml" title="Mobileproxies Lab" href="{PREFIX}/feed.xml"><meta property="og:type" content="{'article' if article else 'website'}"><meta property="og:title" content="{escape(title,quote=True)}"><meta property="og:description" content="{escape(description,quote=True)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{image}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{image}"><script type="application/ld+json">{data}</script></head><body><a class="skip" href="#content">Skip to content</a><header><div class="frame"><a class="brand" href="{PREFIX}/">Mobileproxies <span>Lab</span></a><nav aria-label="Main"><a href="{PREFIX}/">Articles</a><a href="https://github.com/bolivian-peru/mobileproxies-lab">Source code</a></nav></div></header><main id="content" class="frame">{body}</main><footer><div class="frame"><p>Maintained by <a href="https://mobileproxies.org/">Mobileproxies.org</a>, a commercial mobile proxy provider.</p><p>Local examples, explicit test limits. <a href="{PREFIX}/feed.xml">RSS</a> · <a href="https://github.com/bolivian-peru/mobileproxies-lab">Repository</a></p></div></footer></body></html>'''


OUT.mkdir(exist_ok=True)
(OUT/'assets').mkdir(exist_ok=True)
(ROOT/'articles').mkdir(exist_ok=True)
(OUT/'.nojekyll').write_text('')
css='''*{box-sizing:border-box}html{font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:#182435;background:#fff;line-height:1.7}body{margin:0}a{color:#174ca1;text-underline-offset:3px}a:hover{text-decoration-thickness:2px}a:focus-visible,pre:focus-visible,.table-wrap:focus-visible{outline:3px solid #225ac0;outline-offset:4px}.frame{max-width:1080px;margin:0 auto;padding:0 24px}header{border-bottom:1px solid #d7dfe8}header .frame{display:flex;justify-content:space-between;align-items:center;gap:18px;min-height:84px}.brand{font-size:21px;font-weight:750;text-decoration:none;color:#172539}.brand span{font-weight:450;color:#4c6078}nav{display:flex;gap:22px;font-size:14px}main{padding-top:64px!important;padding-bottom:64px!important;min-height:65vh}h1,h2,h3{line-height:1.22;letter-spacing:-.025em;color:#172539}h1{font-size:clamp(30px,5vw,48px);max-width:850px;margin:0 0 22px}h2{font-size:25px;margin:44px 0 16px}h3{font-size:23px;margin:0 0 12px}p{margin:16px 0}.intro{font-size:20px;color:#43566e;max-width:780px}.meta{font-size:14px;color:#4d5d72}.article{max-width:780px}.article li{margin:9px 0}.article ul{padding-left:23px}.article a{overflow-wrap:anywhere}pre{max-width:100%;overflow:auto;padding:20px;background:#f0f4f9;border:1px solid #d7dfe8;border-radius:5px;font:13px/1.65 ui-monospace,SFMono-Regular,Consolas,monospace}code{font:inherit}.table-wrap{overflow:auto;max-width:100%;margin:24px 0}table{border-collapse:collapse;width:100%;font-size:14px}th,td{text-align:left;padding:14px;border:1px solid #d7dfe8;vertical-align:top;min-width:125px}th{background:#f0f4f9}.entries{list-style:none;padding:0;max-width:850px;margin:40px 0}.entries li{border-top:1px solid #d7dfe8;padding:30px 0}.entries h2{margin:0 0 10px}.entries p{margin:10px 0}.note{padding:18px 22px;background:#f0f4f9;border-left:3px solid #225ac0;max-width:850px}.related{border-top:1px solid #d7dfe8;margin-top:45px;padding-top:10px}footer{border-top:1px solid #d7dfe8;background:#f6f8fb;font-size:14px;color:#43566e;padding:25px 0}.skip{position:absolute;top:-100px;left:16px;padding:10px;background:white;z-index:10}.skip:focus{top:10px}@media(max-width:520px){.frame{padding-left:20px;padding-right:20px}header .frame{align-items:flex-start;flex-direction:column;justify-content:center;gap:6px;padding-top:14px;padding-bottom:14px}main{padding-top:40px!important}nav{gap:20px}.intro{font-size:18px}pre{padding:15px;font-size:12px}h2{font-size:23px}}'''
(OUT/'assets/style.css').write_text(css+'\n')
entries=''.join(f'<li><h2><a href="{PREFIX}/{a["slug"]}/">{escape(a["title"])}</a></h2><p>{escape(a["description"])}</p><p class="meta">{a["date"]} · Runnable example included</p></li>' for a in ARTICLES)
body='<p class="meta">DOCUMENTATION AND RUNNABLE EXAMPLES</p><h1>Make a proxy test answer one clear question.</h1><p class="intro">Separate network routing from browser settings, then record what each check can actually establish.</p><p class="note">Start locally without proxy credentials. These examples make no claim about measured carrier speed or a real proxy\'s exit country.</p><ol class="entries">'+entries+'</ol><h2>Start with the code</h2><p>Run the <a href="https://github.com/bolivian-peru/mobileproxies-lab/blob/main/examples/curl-routing-demo.py">curl routing demonstration</a> or the <a href="https://github.com/bolivian-peru/mobileproxies-lab/tree/main/examples/regional-qa">Playwright regional QA example</a>. The repository documents setup and validation limits.</p>'
(OUT/'index.html').write_text(page('Proxy routing and regional testing examples','Runnable curl and Playwright examples with original articles about proxy routing, browser location and timing measurements.','/',body)+'\n')
for a in ARTICLES:
    slug=a['slug'];d=OUT/slug;d.mkdir(exist_ok=True)
    related=''.join(f'<li><a href="{PREFIX}/{other["slug"]}/">{escape(other["title"])}</a></li>' for other in ARTICLES if other['slug']!=slug)
    body='<article class="article"><p class="meta">'+a['date']+' · Mobileproxies.org</p><h1>'+escape(a['title'])+'</h1><p class="intro">'+escape(a['description'])+'</p>'+''.join(render(b) for b in a['blocks'])+'<aside class="related"><h2>More from the lab</h2><ul>'+related+'</ul></aside></article>'
    (d/'index.html').write_text(page(a['title'],a['description'],'/'+slug+'/',body,a)+'\n')
    (ROOT/'articles'/f'{slug}.md').write_text(markdown(a))
for slug,title in [('lab','Proxy routing and regional testing examples')]+[(a['slug'],a['title']) for a in ARTICLES]:
    lines=textwrap.wrap(title,width=31)
    t=''.join(f'<text x="74" y="{228+i*73}" fill="#172539" font-family="Arial,sans-serif" font-size="57" font-weight="700">{escape(line)}</text>' for i,line in enumerate(lines))
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630"><rect width="1200" height="630" fill="#f2f5fa"/><rect x="0" y="0" width="1200" height="13" fill="#225ac0"/><text x="74" y="100" fill="#174ca1" font-family="Arial,sans-serif" font-size="29">MOBILEPROXIES LAB</text>{t}<text x="74" y="568" fill="#43566e" font-family="Arial,sans-serif" font-size="24">Documentation and runnable examples · Mobileproxies.org</text></svg>'
    (OUT/'assets'/f'{slug}.svg').write_text(svg+'\n')
urls=[BASE+'/']+[BASE+'/'+a['slug']+'/' for a in ARTICLES]
(OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+u+'</loc><lastmod>'+DATE+'</lastmod></url>' for u in urls)+'</urlset>\n')
(OUT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+BASE+'/sitemap.xml\n')
(OUT/'feed.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>Mobileproxies Lab</title><link>'+BASE+'/</link><description>Proxy routing and regional testing examples.</description>'+''.join('<item><title>'+escape(a['title'])+'</title><link>'+BASE+'/'+a['slug']+'/</link><guid>'+BASE+'/'+a['slug']+'/</guid><description>'+escape(a['description'])+'</description><pubDate>Mon, 09 Nov 2026 00:00:00 +0000</pubDate></item>' for a in ARTICLES)+'</channel></rss>\n')
print('Built 4 HTML pages, 3 Markdown articles, RSS, sitemap and 4 social-image sources.')
