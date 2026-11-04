"""Red "Signal on Paper" layout, charts and helpers.

build_pages.py execs this file after its own definitions, so everything here
overrides the earlier versions. Page copy and data live in build_pages.py and
service_seo.py; this file controls how the pages look.
"""
import re as _re

SYM = open(SC + 'symbols.txt').read()
SPARK = '<svg aria-hidden="true"><use href="#star"/></svg>'


# ---------------------------------------------------------------- charts
def _rnd(seed, n):
    x = math.sin(seed * 99 + n * 7.13) * 10000
    return x - math.floor(x)


def _smooth(pts):
    d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"
    for i in range(1, len(pts)):
        (x0, y0), (x1, y1) = pts[i - 1], pts[i]
        c = (x0 + x1) / 2
        d += f" C{c:.1f},{y0:.1f} {c:.1f},{y1:.1f} {x1:.1f},{y1:.1f}"
    return d


def cover_svg(seed, W=400, H=225, uid=''):
    """Printed-chart cover: hatched bars, red trend line, last bar red."""
    n = max(8, int(W / 46))
    series = [10 + i * 2.2 + _rnd(seed, i) * 9 for i in range(n)]
    mx, mn = max(series), min(series)
    pad, top = W * 0.07, H * 0.16
    pts = [(pad + i / (n - 1) * (W - 2 * pad), H - H * 0.12 - (v - mn) / (mx - mn) * (H - top - H * 0.22)) for i, v in enumerate(series)]
    bw = (W - 2 * pad) / n * 0.55
    sw = max(2, W / 260)
    pid = f"h{uid}{seed}"
    grid = ''.join(f'<line x1="0" y1="{y:.0f}" x2="{W}" y2="{y:.0f}" stroke="#0B0B0B" stroke-opacity=".09"/>' for y in range(0, int(H), max(20, int(H / 8))))
    grid += ''.join(f'<line x1="{x:.0f}" y1="0" x2="{x:.0f}" y2="{H}" stroke="#0B0B0B" stroke-opacity=".09"/>' for x in range(0, int(W), max(20, int(H / 8))))
    bars = ''.join(f'<rect x="{x - bw / 2:.1f}" y="{y + H * 0.05:.1f}" width="{bw:.1f}" height="{H - y - H * 0.05:.1f}" fill="{"#F83232" if i == n - 1 else f"url(#{pid})"}" stroke="#0B0B0B" stroke-width="{sw:.1f}"/>' for i, (x, y) in enumerate(pts))
    d = _smooth(pts)
    lx, ly = pts[-1]
    return (f'<svg viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><defs>'
            f'<pattern id="{pid}" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="8" height="8" fill="#F5F4F0"/><line x1="0" y1="0" x2="0" y2="8" stroke="#0B0B0B" stroke-width="2.2"/></pattern></defs>'
            f'<rect width="{W}" height="{H}" fill="#E4E1DA"/>{grid}{bars}'
            f'<path d="{d}" transform="translate({sw * 2:.1f} {sw * 2:.1f})" fill="none" stroke="#0B0B0B" stroke-width="{sw * 3:.1f}" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" stroke="#F83232" stroke-width="{sw * 3:.1f}" stroke-linecap="round"/>'
            f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="{sw * 6:.1f}" fill="#F83232" stroke="#0B0B0B" stroke-width="{sw * 1.4:.1f}"/></svg>')


def spark_svg(series, W=150, H=46):
    mx, mn = max(series), min(series); r = (mx - mn) or 1
    pts = [(6 + i / (len(series) - 1) * (W - 14), H - 6 - (v - mn) / r * (H - 14)) for i, v in enumerate(series)]
    d = _smooth(pts); lx, ly = pts[-1]
    bars = ''.join(f'<rect x="{x - 3:.1f}" y="{y:.1f}" width="6" height="{H - y:.1f}" fill="#0B0B0B" opacity=".08"/>' for x, y in pts)
    s = max(3, W / 60)
    return (f'<svg class="svcx__spark" viewBox="0 0 {W} {H}" aria-hidden="true">{bars}<path d="{d}" fill="none" stroke="#F83232" stroke-width="{s * .9:.1f}" stroke-linecap="round"/>'
            f'<rect x="{lx - s * 1.6:.1f}" y="{ly - s * 1.6:.1f}" width="{s * 3.2:.1f}" height="{s * 3.2:.1f}" fill="#F83232" stroke="#0B0B0B" stroke-width="2" transform="rotate(45 {lx:.1f} {ly:.1f})"/></svg>')


MONO = 'font-family="Space Mono, monospace"'
HAND = 'font-family="Caveat, cursive" font-weight="700"'


def ga4_chart():
    ga = [148, 156, 151, 162, 159, 121, 118, 124, 122, 127]
    real = [112, 116, 114, 119, 117, 117, 115, 121, 120, 125]
    out = []
    for i, (g, r) in enumerate(zip(ga, real)):
        x = 34 + i * 59
        out.append(f'<rect x="{x}" y="{230 - g * 1.1:.0f}" width="20" height="{g * 1.1:.0f}" fill="#F83232" stroke="#0B0B0B" stroke-width="2"/>'
                   f'<rect x="{x + 22}" y="{230 - r * 1.1:.0f}" width="20" height="{r * 1.1:.0f}" fill="url(#hatchA)" stroke="#0B0B0B" stroke-width="2"/>'
                   f'<text x="{x + 8}" y="250" {MONO} font-size="10" fill="#0B0B0B">W{i + 1}</text>')
    return f'''<svg viewBox="0 0 640 260" role="img" aria-label="Bar chart: purchases in GA4 compared with real orders, before and after the fixes">
  <defs><pattern id="hatchA" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="7" height="7" fill="#F5F4F0"/><line x1="0" y1="0" x2="0" y2="7" stroke="#0B0B0B" stroke-width="2"/></pattern></defs>
  <text x="20" y="22" {MONO} font-size="11" font-weight="700" fill="#0B0B0B">WEEKLY PURCHASES · GA4 VS REAL ORDERS</text>
  <rect x="452" y="12" width="12" height="12" fill="#F83232" stroke="#0B0B0B" stroke-width="2"/><text x="470" y="22" {MONO} font-size="10">GA4</text>
  <rect x="512" y="12" width="12" height="12" fill="url(#hatchA)" stroke="#0B0B0B" stroke-width="2"/><text x="530" y="22" {MONO} font-size="10">REAL ORDERS</text>
  <line x1="20" x2="620" y1="230" y2="230" stroke="#0B0B0B" stroke-width="2"/>
  {''.join(out)}
  <line x1="330" x2="330" y1="40" y2="236" stroke="#0B0B0B" stroke-width="2" stroke-dasharray="6 5"/>
  <text x="338" y="54" {HAND} font-size="24" fill="#D61F1F">fixes shipped →</text>
</svg>'''


def roas_chart():
    pts = [(0, 0), (5, 20), (10, 34), (15, 43), (20, 48)]
    X = lambda v: 50 + v * 27
    Y = lambda v: 220 - v * 3.6
    xy = [(X(a), Y(b)) for a, b in pts]
    d = _smooth(xy)
    dots = ''.join(f'<rect x="{x - 6:.0f}" y="{y - 6:.0f}" width="12" height="12" fill="#F83232" stroke="#0B0B0B" stroke-width="2" transform="rotate(45 {x:.0f} {y:.0f})"/><text x="{x + 10:.0f}" y="{y - 10:.0f}" {MONO} font-size="11" font-weight="700">${b}k</text>' for (x, y), (_, b) in list(zip(xy, pts))[1:])
    ticks = ''.join(f'<text x="{X(a) - 12:.0f}" y="242" {MONO} font-size="10">${a}k</text>' for a, _ in pts)
    return f'''<svg viewBox="0 0 640 260" role="img" aria-label="Line chart: revenue flattens as ad spend rises and drops below the breakeven line">
  <text x="20" y="22" {MONO} font-size="11" font-weight="700">REVENUE VS MONTHLY AD SPEND · BREAKEVEN AT 2.5X</text>
  <line x1="50" x2="620" y1="220" y2="220" stroke="#0B0B0B" stroke-width="2"/>
  <path d="M{X(0)},{Y(0)} L{X(20)},{Y(50)}" stroke="#0B0B0B" stroke-width="2.5" stroke-dasharray="8 6" fill="none"/>
  <text x="{X(13.4):.0f}" y="{Y(39):.0f}" {HAND} font-size="22">breakeven line</text>
  <path d="{d}" transform="translate(4 4)" stroke="#0B0B0B" stroke-width="5" fill="none"/>
  <path d="{d}" stroke="#F83232" stroke-width="5" fill="none"/>
  {dots}{ticks}
  <text x="{X(15.2):.0f}" y="{Y(54):.0f}" {HAND} font-size="22" fill="#D61F1F">the last $10k lost money ↓</text>
</svg>'''


def site_tree():
    return f'''<svg viewBox="0 0 640 230" role="img" aria-label="Site architecture: home links to service pages, which link to suburb pages">
  <g {MONO} font-size="11" font-weight="700">
    <g stroke="#0B0B0B" stroke-width="2" fill="none"><path d="M320 52 V80 M140 80 H500 M140 80 V100 M320 80 V100 M500 80 V100"/><path d="M140 136 V160 M80 160 H200 M80 160 V176 M140 160 V176 M200 160 V176"/><path d="M320 136 V160 M260 160 H380 M260 160 V176 M320 160 V176 M380 160 V176"/></g>
    <rect x="264" y="24" width="120" height="32" fill="#0B0B0B"/><rect x="260" y="20" width="120" height="32" fill="#F83232" stroke="#0B0B0B" stroke-width="2"/><text x="298" y="40">HOME</text>
    <g fill="#F5F4F0" stroke="#0B0B0B" stroke-width="2"><rect x="80" y="100" width="120" height="36"/><rect x="260" y="100" width="120" height="36"/><rect x="440" y="100" width="120" height="36"/></g>
    <g fill="#0B0B0B" font-size="10"><text x="96" y="122">/plumbing/</text><text x="276" y="122">/hot-water/</text><text x="447" y="122">/blocked-drains/</text></g>
    <g fill="#F83232" fill-opacity=".25" stroke="#0B0B0B" stroke-width="1.5"><rect x="46" y="176" width="68" height="30"/><rect x="118" y="176" width="44" height="30"/><rect x="166" y="176" width="68" height="30"/><rect x="226" y="176" width="68" height="30"/><rect x="298" y="176" width="44" height="30"/><rect x="346" y="176" width="68" height="30"/></g>
    <g fill="#0B0B0B" font-size="10" font-weight="400"><text x="54" y="195">fitzroy</text><text x="124" y="195">kew</text><text x="172" y="195">carlton</text><text x="232" y="195">fitzroy</text><text x="304" y="195">kew</text><text x="352" y="195">carlton</text></g>
  </g>
  <text x="440" y="192" {HAND} font-size="22">one page per suburb</text><text x="440" y="214" {HAND} font-size="22">you actually serve</text>
</svg>'''


# ---------------------------------------------------------------- titles + cards
def phero_title(lines):
    out = []
    for t, g in lines:
        if g:
            out.append(f'          <span class="line line--blk"><span class="blk">{t}</span></span>')
        else:
            out.append(f'          <span class="line"><span>{t}</span></span>')
    return '\n'.join(out)


def post_card(P, p, cls='bcard paper reveal'):
    ex = E(p["dek"][:130].rsplit(" ", 1)[0]) + '…'
    return f'''<a class="{cls}" href="{P}blog/{p["slug"]}/" data-post data-tags="{p["tagkey"]}" data-text="{E((p["title"] + " " + p["dek"] + " " + p["tag"]).lower())}" data-cursor="Read">
            <div class="bcard__cover">{cover_svg(p["seed"], uid="c")}<span class="bcard__tag">{E(p["tag"])}</span></div>
            <div class="bcard__body"><p class="bcard__meta">{fmt_date(p["date"])} · {p["minutes"]} min read</p><h3>{E(p["title"])}</h3><p>{ex}</p><span class="bcard__more">Read article <b aria-hidden="true">→</b></span></div>
          </a>'''


# ---------------------------------------------------------------- page stickers
def badge(text, x, y, r):
    return (f'<div class="sticker sticker--badge sm" style="--x:{x};--y:{y};--r:{r}" data-drag>'
            f'<svg viewBox="0 0 200 200" class="badge__ring"><defs><path id="circ" d="M100,100 m-74,0 a74,74 0 1,1 148,0 a74,74 0 1,1 -148,0"/></defs>'
            f'<text><textPath href="#circ" textLength="462" lengthAdjust="spacing">{text} ✱ {text} ✱ </textPath></text></svg>'
            f'<svg class="badge__star"><use href="#star"/></svg></div>')


def tag_sticker(html, x, y, r):
    return f'<div class="sticker sticker--tag" style="--x:{x};--y:{y};--r:{r}" data-drag>{html}</div>'


def pill_sticker(text, x, y, r):
    return f'<div class="sticker sticker--pill" style="--x:{x};--y:{y};--r:{r}" data-drag>{text}</div>'


STICKERS = {
    'services/': badge('NO LOCK-IN', '82%', '19%', '-8deg') + tag_sticker('<span class="pixel">KPI</span> &gt; <span class="pixel">VIBES</span>', '58%', '60%', '5deg'),
    'services/seo/': badge('RANK HIGHER', '40%', '76%', '10deg'),
    'book/': badge('FREE CALL', '80%', '22%', '-10deg') + pill_sticker('30 min · no pitch', '64%', '58%', '4deg'),
    'contact/': tag_sticker('<span class="pixel">SAY</span> <span class="pixel">HI</span> ✱', '42%', '24%', '-6deg'),
    'blog/': badge('NEW POSTS', '80%', '20%', '8deg') + tag_sticker('<span class="pixel">READ</span> &gt; <span class="pixel">SCROLL</span>', '66%', '62%', '-4deg'),
}


def masthead(label):
    return (f'<div class="masthead mono"><span><svg class="i-star red"><use href="#star"/></svg> {label}</span>'
            '<span class="hide-sm">Data-driven digital marketing</span><span class="hide-sm" data-mel-clock>Melbourne</span>'
            '<span><i class="live"></i> Open for work</span></div>')


# ---------------------------------------------------------------- restyle pass
_SWAPS = [
    ('class="goth glow"', 'class="hi"'), ('chip chip--uv', 'tag tag--red'), ('class="chip"', 'class="tag"'),
    ('class="num"', 'class="hnum"'), ('class="phero__chips', 'class="tags phero__chips'), ('class="hero__proof', 'class="proof'),
    ('btn--violet', 'btn--red'), ('btn--ghost', 'btn--paper'), ('class="online"', 'class="live"'), ('href="#spark"', 'href="#star"'),
    ('filter="url(#uvglow)"', ''), ('#B596FF', '#F83232'), ('#DCCBFF', '#F83232'), ('#7844E9', '#F83232'),
    ('rgba(236,232,244,.12)', 'rgba(245,244,240,.25)'), ('#8F8B9A', '#BDB9B0'), ('Geist Mono, monospace', 'Space Mono, monospace'),
    ('class="faq__q"', 'class="faq__q"'),
]
_PAPER = ['svcx__item', 'svcx__index', 'booker', 'side-card', 'method', 'feature', 'topic', 'toc', 'toc-mobile', 'tldr', 'callout',
          'figure__box', 'author-box', 'post-cover', 'incl__item', 'pain', 'case-mini', 'serp', 'confirm__card', 'checklist']


def redify(html, path):
    for a, b in _SWAPS:
        html = html.replace(a, b)
    # hidden UV notes: margin notes become paper sticky notes, other notes go
    html = _re.sub(r'<span class="note uv note--margin" data-note><span>(.*?)</span></span>', r'<span class="sticky">\1</span>', html, flags=_re.S)
    html = _re.sub(r'\s*<div class="note uv"[^>]*><span>.*?</span></div>', '', html, flags=_re.S)
    html = _re.sub(r'\s*<div class="phero__ink uv"[^>]*>.*?</div>', '', html, flags=_re.S)
    html = html.replace(' uv"', '"').replace(' data-note', '')
    # paper-card class on card-like blocks
    for c in _PAPER:
        html = _re.sub(rf'class="({c})(\s|")', r'class="\1 paper\2', html)
    html = html.replace('class="prep">', 'class="prep">').replace('<div class="reveal"><b>', '<div class="paper reveal"><b>')
    html = _re.sub(r'<nav class="post-nav"[^>]*>.*?</nav>', lambda m: m.group(0).replace('<a href', '<a class="paper" href'), html, flags=_re.S)
    # pricing tickets need a wrapper for the drop shadow (clip-path cuts box-shadow)
    html = html.replace('<article class="plan plan--hot reveal">\n            <span class="plan__badge">Most popular</span>', '<div class="plan-wrap reveal"><span class="plan__badge">Most popular</span><article class="plan plan--hot">')
    html = html.replace('<article class="plan reveal">', '<div class="plan-wrap reveal"><article class="plan">')
    html = _re.sub(r'(btn--block"[^>]*>[^<]*</a>\s*</article>)', r'\1</div>', html)
    # black ink bands for rhythm
    for lab in ('How it works', 'The roadmap'):
        html = html.replace(f'<section class="section section--tight">\n      <div class="container">\n        <div class="head"><p class="label reveal">{lab}</p>', f'<section class="section section--tight band--ink">\n      <div class="container">\n        <div class="head"><p class="label reveal">{lab}</p>')
    # masthead + stickers at the top of every page hero
    label = {'services/': 'Services', 'services/seo/': 'Service · SEO', 'book/': 'Free consultation', 'contact/': 'Contact', 'blog/': 'The blog'}.get(path, 'Field notes')
    st = STICKERS.get(path, '')
    st = f'\n      <div class="stickers" aria-hidden="true">{st}</div>' if st else ''
    html = _re.sub(r'(<(?:section|header) class="phero[^"]*" id="top">)(\s*<div class="container">)',
                   lambda m: m.group(1) + st + m.group(2) + '\n        ' + masthead(label), html, count=1)
    return html


# ---------------------------------------------------------------- layout
NAV = [('About', '#about', None), ('Services', 'services/', 'services'), ('Calculator', '#calculator', None), ('Work', '#work', None), ('Blog', 'blog/', 'blog'), ('Contact', 'contact/', 'contact')]


def layout(P, path, title, desc, active, body, scripts=(), ld=(), og_type='website', noindex=False, og_image='assets/img/og-image.png'):
    canon = SITE + path
    nav = '\n      '.join(f'<a href="{P}{h}"{" class=\"is-active\" aria-current=\"page\"" if k == active else ""}>{n}</a>' for n, h, k in NAV)
    menu = '\n      '.join(f'<a href="{P}{h}"><small>0{i + 1}</small>{n}</a>' for i, (n, h, k) in enumerate(NAV + [('Book a call', 'book/', 'book')]))
    lds = '\n'.join(f'  <script type="application/ld+json">{x}</script>' for x in ld)
    scr = '\n'.join(f'  <script src="{P}js/{s}"></script>' for s in scripts)
    robots = 'noindex, follow' if noindex else 'index, follow, max-image-preview:large'
    body = redify(body, path)
    return f'''<!DOCTYPE html>
<html lang="en-AU">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{E(title)}</title>
  <meta name="description" content="{E(desc)}">
  <meta name="author" content="Manjil Shrestha">
  <meta name="robots" content="{robots}">
  <meta name="theme-color" content="#E9E7E1">
  <link rel="canonical" href="{canon}">
  <meta property="og:type" content="{og_type}">
  <meta property="og:locale" content="en_AU">
  <meta property="og:site_name" content="Manjil Shrestha">
  <meta property="og:title" content="{E(title)}">
  <meta property="og:description" content="{E(desc)}">
  <meta property="og:url" content="{canon}">
  <meta property="og:image" content="{SITE}{og_image}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{E(title)}">
  <meta name="twitter:description" content="{E(desc)}">
  <meta name="twitter:image" content="{SITE}{og_image}">
  <link rel="icon" type="image/svg+xml" href="{P}assets/favicon.svg">
  <link rel="manifest" href="{P}site.webmanifest">
  <link rel="alternate" type="application/rss+xml" title="Manjil Shrestha — Blog" href="{P}blog/feed.xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Anybody:ital,wdth,wght@0,50..150,100..900;1,50..150,100..900&family=Archivo:wght@400;500;600;700&family=Space+Mono:wght@400;700&family=Silkscreen&family=Caveat:wght@700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{P}css/styles.css">
  <link rel="stylesheet" href="{P}css/pages.css">
{lds}
</head>

<body class="no-js">
  <script>document.body.classList.replace('no-js','js');</script>
  <svg width="0" height="0" style="position:absolute" aria-hidden="true">
    {SYM}
  </svg>

  <div class="cursor" id="cursor" aria-hidden="true"><svg class="cursor__star"><use href="#star"/></svg><span class="cursor__label" id="cursorLabel"></span></div>
  <div class="progress" id="progress" aria-hidden="true"></div>
  <div class="grain" aria-hidden="true"></div>
  <div class="toast" id="toast" role="status" aria-live="polite"></div>

  <header class="nav" id="nav">
    <a class="nav__brand" href="{P}" aria-label="Manjil Shrestha, home"><svg viewBox="0 0 1463 317" class="nav__logo"><use href="#logo"/></svg></a>
    <nav class="nav__links" aria-label="Primary">
      {nav}
    </nav>
    <div class="nav__right">
      <span class="nav__clock mono"><i class="live"></i><span data-mel-clock>MEL --:--</span></span>
      <a href="{P}book/" class="btn btn--red btn--sm" data-magnetic>Book a call <svg class="i-star"><use href="#star"/></svg></a>
      <button class="nav__burger" id="burger" aria-label="Open menu" aria-expanded="false" aria-controls="menu"><span></span><span></span></button>
    </div>
  </header>
  <div class="mobile-menu" id="menu" aria-hidden="true">
    <nav class="mobile-menu__links">
      {menu}
    </nav>
    <div class="mobile-menu__foot" data-socials></div>
  </div>

  <main>
{body}
  </main>

  <footer class="footer" data-theme="ink">
    <div class="container">
      <div class="footer__top">
        <p class="footer__line">Digital marketing expert in Melbourne.<br>Measured, not guessed.</p>
        <nav class="footer__links" aria-label="Footer"><a href="{P}services/">Services</a><a href="{P}#work">Work</a><a href="{P}blog/">Blog</a><a href="{P}book/">Book a call</a><a href="{P}contact/">Contact</a><a href="{P}blog/feed.xml">RSS</a></nav>
      </div>
      <svg class="footer__logo" viewBox="0 0 1463 317" role="img" aria-label="Manjil"><use href="#logo"/></svg>
      <div class="footer__bar mono">
        <span>© <span data-year>2026</span> Manjil Shrestha</span>
        <span class="hide-sm">Made in Melbourne ✱ on paper</span>
        <a href="#top">Back to top ↑</a>
      </div>
    </div>
  </footer>

  <script src="{P}js/vendor/gsap.min.js"></script>
  <script src="{P}js/vendor/ScrollTrigger.min.js"></script>
  <script src="{P}js/vendor/lenis.min.js"></script>
  <script src="{P}js/content.js"></script>
  <script src="{P}js/core.js"></script>
{scr}
</body>
</html>
'''
