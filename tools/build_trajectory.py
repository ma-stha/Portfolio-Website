"""Builds the "Trajectory" design (purple) into /trajectory/.

Run:  python3 tools/build_trajectory.py

Content is shared with the main red site:
  - home content comes from js/content.js (read through node)
  - services, SEO page, booking, contact and blog content comes from
    tools/build_pages.py (its data, not its layout)
Only the design here is different. The red site is not touched.
"""
import html, json, math, os, re, shutil, subprocess
from datetime import datetime

TOOLS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(TOOLS)
OUT = os.path.join(ROOT, 'trajectory')
SITE = 'https://manjilshrestha.online/'
E = html.escape

# ------------------------------------------------------------ shared content
SITE_DATA = json.loads(subprocess.check_output(
    ['node', '-e', "global.window={};require(process.argv[1]);process.stdout.write(JSON.stringify(window.SITE))", os.path.join(ROOT, 'js/content.js')]))

_src = open(os.path.join(TOOLS, 'build_pages.py')).read()
_src = _src[:_src.index("exec(open(SC + 'service_seo.py').read())")]
NS = {'__file__': os.path.join(TOOLS, 'build_pages.py'), '__name__': 'pages_data'}
exec(compile(_src, 'build_pages.py', 'exec'), NS)
SERVICES, POSTS, TEMPLATE, SOON, ICONS, fmt_date = NS['SERVICES'], NS['POSTS'], NS['TEMPLATE'], NS['SOON'], NS['ICONS'], NS['fmt_date']
SYMBOLS = open(os.path.join(TOOLS, 'symbols.txt')).read().replace('var(--star, #F83232)', 'var(--star, #6A2CFF)')

CLIENTS = ["Northside Dental", "Fitzroy Coffee Co.", "Yarra Home Services", "Kinetic SaaS", "Brunswick Bikes", "Southbank Legal", "Ember Skincare", "Laneway Eats", "Carlton Physio", "Arcade Studio"]  # DEMO

# ------------------------------------------------------------ chart helpers
def smooth(pts):
    d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"
    for i in range(1, len(pts)):
        (x0, y0), (x1, y1) = pts[i - 1], pts[i]
        c = (x0 + x1) / 2
        d += f" C{c:.1f},{y0:.1f} {c:.1f},{y1:.1f} {x1:.1f},{y1:.1f}"
    return d

def scale(series, W, H, px=12, py=14):
    mx, mn = max(series), min(series); r = (mx - mn) or 1
    return [(px + i / (len(series) - 1) * (W - 2 * px), H - py - (v - mn) / r * (H - 2 * py)) for i, v in enumerate(series)]

_uid = [0]
def line_chart(series, W=400, H=160, grid=True, dots=False, cls=''):
    _uid[0] += 1; gid = f"tg{_uid[0]}"
    pts = scale(series, W, H); d = smooth(pts); lx, ly = pts[-1]
    g = ''.join(f'<line x1="0" x2="{W}" y1="{H * f:.0f}" y2="{H * f:.0f}" class="ch-grid"/>' for f in (.25, .5, .75)) if grid else ''
    dt = ''.join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.6" class="ch-dot"/>' for x, y in pts[:-1]) if dots else ''
    return (f'<svg class="ch {cls}" viewBox="0 0 {W} {H}" preserveAspectRatio="none" aria-hidden="true"><defs><linearGradient id="{gid}" x1="0" x2="0" y1="0" y2="1">'
            f'<stop offset="0" stop-color="#6A2CFF" stop-opacity=".28"/><stop offset="1" stop-color="#6A2CFF" stop-opacity="0"/></linearGradient></defs>{g}'
            f'<path d="{d} L{lx:.1f},{H} L{pts[0][0]:.1f},{H}Z" fill="url(#{gid})"/><path d="{d}" class="ch-line" pathLength="1"/>{dt}'
            f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="5" class="ch-head"/></svg>')

def cover_svg(seed, W=640, H=400, uid='c'):
    """Generated cover: lavender field, orbit rings, a rising area chart and a lime point."""
    rnd = lambda n: (lambda x: x - math.floor(x))(math.sin(seed * 99 + n * 7.13) * 10000)
    series = [10 + i * 2.4 + rnd(i) * 8 for i in range(12)]
    pts = scale(series, W, H * .78, W * .06, H * .08); pts = [(x, y + H * .18) for x, y in pts]
    d = smooth(pts); lx, ly = pts[-1]; gid = f"cv{uid}{seed}"
    rings = ''.join(f'<circle cx="{W * (.72 + rnd(40) * .1):.0f}" cy="{H * (.26 + rnd(41) * .1):.0f}" r="{30 + i * 34}" fill="none" stroke="#6A2CFF" stroke-opacity="{.22 - i * .025:.3f}"/>' for i in range(7))
    grid = ''.join(f'<line x1="{x}" x2="{x}" y1="0" y2="{H}" stroke="#6A2CFF" stroke-opacity=".07"/>' for x in range(0, W, 40)) + ''.join(f'<line y1="{y}" y2="{y}" x1="0" x2="{W}" stroke="#6A2CFF" stroke-opacity=".07"/>' for y in range(0, H, 40))
    return (f'<svg viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><defs>'
            f'<linearGradient id="{gid}" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#6A2CFF" stop-opacity=".45"/><stop offset="1" stop-color="#6A2CFF" stop-opacity="0"/></linearGradient>'
            f'<radialGradient id="{gid}r" cx=".8" cy=".1" r=".9"><stop offset="0" stop-color="#C4B3FF"/><stop offset="1" stop-color="#EEE9FF"/></radialGradient></defs>'
            f'<rect width="{W}" height="{H}" fill="url(#{gid}r)"/>{grid}{rings}'
            f'<path d="{d} L{lx:.1f},{H} L{pts[0][0]:.1f},{H}Z" fill="url(#{gid})"/>'
            f'<path d="{d}" fill="none" stroke="#6A2CFF" stroke-width="{max(2.5, W / 220):.1f}" stroke-linecap="round"/>'
            f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="{max(7, W / 70):.0f}" fill="#D7FF3E" stroke="#170B38" stroke-width="2"/></svg>')

MONO = 'font-family="IBM Plex Mono, monospace"'

def ga4_chart():
    ga = [148, 156, 151, 162, 159, 121, 118, 124, 122, 127]; real = [112, 116, 114, 119, 117, 117, 115, 121, 120, 125]
    bars = ''.join(f'<rect x="{34 + i * 59}" y="{230 - g * 1.1:.0f}" width="20" height="{g * 1.1:.0f}" rx="5" fill="#6A2CFF"/>'
                   f'<rect x="{56 + i * 59}" y="{230 - r * 1.1:.0f}" width="20" height="{r * 1.1:.0f}" rx="5" fill="#C4B3FF"/>'
                   f'<text x="{40 + i * 59}" y="250" {MONO} font-size="10" fill="#6B6390">W{i + 1}</text>' for i, (g, r) in enumerate(zip(ga, real)))
    return f'''<svg viewBox="0 0 640 260" role="img" aria-label="Bar chart: purchases in GA4 compared with real orders, before and after the fixes">
  <text x="20" y="22" {MONO} font-size="11" fill="#170B38">Weekly purchases · GA4 vs real orders</text>
  <rect x="456" y="13" width="10" height="10" rx="3" fill="#6A2CFF"/><text x="472" y="22" {MONO} font-size="10" fill="#6B6390">GA4</text>
  <rect x="512" y="13" width="10" height="10" rx="3" fill="#C4B3FF"/><text x="528" y="22" {MONO} font-size="10" fill="#6B6390">Real orders</text>
  <g stroke="#170B38" stroke-opacity=".08"><line x1="20" x2="620" y1="70" y2="70"/><line x1="20" x2="620" y1="150" y2="150"/></g><line x1="20" x2="620" y1="230" y2="230" stroke="#170B38" stroke-opacity=".25"/>
  {bars}
  <line x1="330" x2="330" y1="40" y2="236" stroke="#170B38" stroke-dasharray="4 5" stroke-opacity=".5"/>
  <rect x="338" y="40" width="112" height="22" rx="11" fill="#D7FF3E"/><text x="350" y="55" {MONO} font-size="10" fill="#170B38">fixes shipped →</text>
</svg>'''

def roas_chart():
    pts = [(0, 0), (5, 20), (10, 34), (15, 43), (20, 48)]
    X = lambda v: 50 + v * 27; Y = lambda v: 220 - v * 3.6
    xy = [(X(a), Y(b)) for a, b in pts]
    dots = ''.join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="6" fill="#fff" stroke="#6A2CFF" stroke-width="3"/><text x="{x + 10:.0f}" y="{y - 10:.0f}" {MONO} font-size="11" fill="#170B38">${b}k</text>' for (x, y), (_, b) in list(zip(xy, pts))[1:])
    ticks = ''.join(f'<text x="{X(a) - 12:.0f}" y="242" {MONO} font-size="10" fill="#6B6390">${a}k</text>' for a, _ in pts)
    return f'''<svg viewBox="0 0 640 260" role="img" aria-label="Line chart: revenue flattens as ad spend rises and drops below the breakeven line">
  <text x="20" y="22" {MONO} font-size="11" fill="#170B38">Revenue vs monthly ad spend · breakeven at 2.5x</text>
  <line x1="50" x2="620" y1="220" y2="220" stroke="#170B38" stroke-opacity=".25"/>
  <path d="M{X(0)},{Y(0)} L{X(20)},{Y(50)}" stroke="#170B38" stroke-opacity=".45" stroke-width="2" stroke-dasharray="6 6" fill="none"/>
  <text x="{X(13.6):.0f}" y="{Y(39.5):.0f}" {MONO} font-size="10" fill="#6B6390">breakeven</text>
  <path d="{smooth(xy)}" stroke="#6A2CFF" stroke-width="4" fill="none" stroke-linecap="round"/>{dots}{ticks}
  <rect x="{X(13.2):.0f}" y="{Y(55):.0f}" width="190" height="22" rx="11" fill="#D7FF3E"/><text x="{X(13.2) + 12:.0f}" y="{Y(55) + 15:.0f}" {MONO} font-size="10" fill="#170B38">the last $10k lost money ↓</text>
</svg>'''

def site_tree():
    return f'''<svg viewBox="0 0 640 230" role="img" aria-label="Site architecture: home links to service pages, which link to suburb pages">
  <g fill="none" stroke="#6A2CFF" stroke-opacity=".5" stroke-width="1.6"><path d="M320 52 V80 M140 80 H500 M140 80 V100 M320 80 V100 M500 80 V100"/><path d="M140 136 V160 M80 160 H200 M80 160 V176 M140 160 V176 M200 160 V176"/><path d="M320 136 V160 M260 160 H380 M260 160 V176 M320 160 V176 M380 160 V176"/></g>
  <g {MONO} font-size="11">
    <rect x="260" y="20" width="120" height="32" rx="16" fill="#6A2CFF"/><text x="302" y="40" fill="#fff">Home</text>
    <g fill="#fff" stroke="#E6DEFF"><rect x="80" y="100" width="120" height="36" rx="12"/><rect x="260" y="100" width="120" height="36" rx="12"/><rect x="440" y="100" width="120" height="36" rx="12"/></g>
    <g fill="#170B38" font-size="10"><text x="98" y="122">/plumbing/</text><text x="280" y="122">/hot-water/</text><text x="449" y="122">/blocked-drains/</text></g>
    <g fill="#E6DEFF"><rect x="46" y="176" width="68" height="30" rx="10"/><rect x="118" y="176" width="44" height="30" rx="10"/><rect x="166" y="176" width="68" height="30" rx="10"/><rect x="226" y="176" width="68" height="30" rx="10"/><rect x="298" y="176" width="44" height="30" rx="10"/><rect x="346" y="176" width="68" height="30" rx="10"/></g>
    <g fill="#170B38" font-size="10"><text x="54" y="195">fitzroy</text><text x="124" y="195">kew</text><text x="172" y="195">carlton</text><text x="232" y="195">fitzroy</text><text x="304" y="195">kew</text><text x="352" y="195">carlton</text></g>
    <text x="440" y="192" fill="#6B6390">one page per suburb</text><text x="440" y="208" fill="#6B6390">you actually serve</text>
  </g>
</svg>'''

NS.update(ga4_chart=ga4_chart, roas_chart=roas_chart, site_tree=site_tree)

# ------------------------------------------------------------ small markup helpers
def kpi_chip(k):
    v = k["value"]; d = k.get("decimals", 0)
    sign = "+" if v > 0 and k.get("suffix") == "%" else ""
    return f'<span><b>{sign}{v:.{d}f}{E(k.get("suffix", ""))}</b>{E(k["label"])}</span>'

STAR = '<svg class="i-star" aria-hidden="true"><use href="#star"/></svg>'
ARROW = '<svg class="i-arr" viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>'

def title_lines(lines):
    """lines: list of strings; *word* becomes the serif italic accent."""
    out = []
    for t in lines:
        t = re.sub(r'\*(.+?)\*', r'<em>\1</em>', t)
        out.append(f'<span class="tl"><span>{t}</span></span>')
    return ''.join(out)

def head_block(eyebrow, title, lead='', row=False, spine=None):
    t = re.sub(r'\*(.+?)\*', r'<em>\1</em>', title)
    lead_html = f'<p class="lead rv">{lead}</p>' if lead else ''
    return f'<div class="shead{" shead--row" if row else ""}"><div><p class="eyebrow rv">{eyebrow}</p><h2 class="h2 rv">{t}</h2></div>{lead_html}</div>'

def faq_list(items, uid='f'):
    return ''.join(f'<div class="faq__item rv{" is-open" if i == 0 else ""}"><button class="faq__q" aria-expanded="{"true" if i == 0 else "false"}" aria-controls="{uid}{i}"><span>{E(q)}</span><i aria-hidden="true"></i></button>'
                   f'<div class="faq__a" id="{uid}{i}" role="region"><div><p>{E(a)}</p></div></div></div>' for i, (q, a) in enumerate(items))

def faq_ld(items):
    return json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}, ensure_ascii=False)

def crumbs(P, trail):
    parts = []
    for i, (n, p) in enumerate(trail):
        parts.append(f'<span aria-current="page">{E(n)}</span>' if i == len(trail) - 1 else f'<a href="{P}{p}">{E(n)}</a><span aria-hidden="true">/</span>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + ''.join(parts) + '</nav>'

def phero(P, trail, eyebrow, lines, lead, cta='', aside='', spine='Intro'):
    return f'''    <section class="phero" id="top" data-spine="{spine}">
      <div class="container">
        {crumbs(P, trail)}
        <div class="phero__grid">
          <div>
            <p class="eyebrow fade"><i class="pulse"></i>{eyebrow}</p>
            <h1 class="display" aria-label="{E(re.sub(r'[*]', '', ' '.join(lines)))}">{title_lines(lines)}</h1>
            <p class="phero__lead fade">{lead}</p>
            {f'<div class="cta-row fade">{cta}</div>' if cta else ''}
          </div>
          {aside}
        </div>
      </div>
    </section>'''

def write(rel, text):
    full = os.path.join(OUT, rel); os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w').write(text); print('wrote trajectory/' + rel)

# ------------------------------------------------------------ layout
NAV = [('Work', '#work', 'work'), ('Services', 'services/', 'services'), ('Lab', '#lab', 'lab'), ('Blog', 'blog/', 'blog'), ('Contact', 'contact/', 'contact')]

def layout(P, path, title, desc, active, body, scripts=(), ld=(), og_type='website'):
    canon = SITE + path   # the main (red) site is canonical; this design is a candidate
    nav = ''.join(f'<a href="{P}{h}"{" aria-current=page class=is-active" if k == active else ""}>{n}</a>' for n, h, k in NAV)
    menu = ''.join(f'<a href="{P}{h}"><small>0{i + 1}</small>{n}<span>{ARROW}</span></a>' for i, (n, h, k) in enumerate(NAV + [('Book a free call', 'book/', 'book')]))
    lds = ''.join(f'\n  <script type="application/ld+json">{x}</script>' for x in ld)
    scr = ''.join(f'\n  <script src="{P}js/{s}"></script>' for s in scripts)
    return f'''<!DOCTYPE html>
<html lang="en-AU">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{E(title)}</title>
  <meta name="description" content="{E(desc)}">
  <meta name="author" content="Manjil Shrestha">
  <meta name="robots" content="noindex, follow">
  <meta name="theme-color" content="#F5F3FC">
  <link rel="canonical" href="{canon}">
  <meta property="og:type" content="{og_type}">
  <meta property="og:title" content="{E(title)}">
  <meta property="og:description" content="{E(desc)}">
  <meta property="og:image" content="{P}assets/img/og-image.png">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" type="image/svg+xml" href="{P}assets/favicon.svg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wdth,wght@12..96,75..100,200..800&family=Instrument+Serif:ital@0;1&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{P}css/trajectory.css">{lds}
</head>
<body class="no-js">
  <script>document.body.classList.replace('no-js','js');</script>
  <svg width="0" height="0" style="position:absolute" aria-hidden="true">{SYMBOLS}</svg>
  <a class="skip" href="#main">Skip to content</a>
  <div class="cursor" id="cursor" aria-hidden="true"><i></i><span id="cursorLabel"></span></div>
  <div class="progress" id="progress" aria-hidden="true"></div>
  <nav class="spine" id="spine" aria-label="Sections on this page"></nav>
  <div class="toast" id="toast" role="status" aria-live="polite"></div>

  <header class="nav" id="nav">
    <a class="nav__brand" href="{P}" aria-label="Manjil Shrestha, home"><svg viewBox="0 0 1463 317"><use href="#logo"/></svg></a>
    <nav class="nav__links" aria-label="Primary">{nav}</nav>
    <div class="nav__right">
      <span class="nav__status"><i class="pulse"></i><span data-availability>Available</span></span>
      <a class="btn btn--primary btn--sm" href="{P}book/" data-magnetic>Book a call {ARROW}</a>
      <a class="nav__me" href="{P}contact/" aria-label="Contact"><img src="{P}assets/img/avatar.png" alt="" width="36" height="36"></a>
      <button class="nav__burger" id="burger" aria-label="Open menu" aria-expanded="false" aria-controls="menu"><span></span><span></span></button>
    </div>
  </header>
  <div class="menu" id="menu" aria-hidden="true">
    <nav class="menu__links">{menu}</nav>
    <div class="menu__foot" data-socials></div>
  </div>

  <main id="main">
{body}
  </main>

  <footer class="footer" data-spine="Footer">
    <div class="container">
      <div class="footer__grid">
        <div>
          <p class="footer__big">Growth, <em>plotted.</em></p>
          <p class="footer__sub">Data-driven digital marketing for ambitious Melbourne businesses.</p>
          <a class="btn btn--lime" href="{P}book/" data-magnetic>Book a free consultation {ARROW}</a>
        </div>
        <div class="footer__cols">
          <div><h4>Site</h4><a href="{P}">Home</a><a href="{P}services/">Services</a><a href="{P}services/seo/">SEO in Melbourne</a><a href="{P}blog/">Blog</a></div>
          <div><h4>Talk</h4><a href="{P}book/">Book a call</a><a href="{P}contact/">Contact</a><a href="#" data-copy-email>Copy email</a></div>
          <div><h4>Elsewhere</h4><span data-socials class="footer__soc"></span></div>
        </div>
      </div>
      <svg class="footer__logo" viewBox="0 0 1463 317" role="img" aria-label="Manjil"><use href="#logo"/></svg>
      <div class="footer__bar"><span>© <span data-year>2026</span> Manjil Shrestha · Melbourne</span><span class="mono" data-mel-clock>MEL --:--</span><a href="#top">Back to top ↑</a></div>
    </div>
  </footer>

  <script src="{P}js/vendor/gsap.min.js"></script>
  <script src="{P}js/vendor/ScrollTrigger.min.js"></script>
  <script src="{P}js/vendor/lenis.min.js"></script>
  <script src="{P}js/content.js"></script>
  <script src="{P}js/core.js"></script>{scr}
</body>
</html>
'''

# ============================================================ HOME
SVC_VIZ = {
    'seo': '''<ol class="viz-rank" aria-hidden="true"><li><b>#1</b><span></span></li><li><b>#2</b><span></span></li><li><b>#3</b><span></span></li><li class="you"><b>you</b><span>yourbusiness.com.au</span></li></ol>''',
    'paid': '<div class="viz-bars" aria-hidden="true">' + ''.join(f'<i style="--h:{h}%;--d:{i * .08:.2f}s"></i>' for i, h in enumerate([28, 36, 33, 48, 55, 52, 66, 74, 70, 86, 92, 100])) + '<span class="chip-lime">ROAS 3.6x</span></div>',
    'analytics': '''<svg class="viz-donut" viewBox="0 0 120 120" aria-hidden="true"><circle cx="60" cy="60" r="44" pathLength="100" class="d0"/><circle cx="60" cy="60" r="44" pathLength="100" class="d1" style="--a:42;--o:0"/><circle cx="60" cy="60" r="44" pathLength="100" class="d2" style="--a:28;--o:-42"/><circle cx="60" cy="60" r="44" pathLength="100" class="d3" style="--a:18;--o:-70"/><text x="60" y="58" text-anchor="middle">100%</text><text x="60" y="74" text-anchor="middle" class="sm">tracked</text></svg><ul class="viz-legend" aria-hidden="true"><li><i class="d1"></i>Search 42%</li><li><i class="d2"></i>Paid 28%</li><li><i class="d3"></i>Email 18%</li></ul>''',
    'cro': '''<div class="viz-ab" aria-hidden="true"><div><span>A · control</span><b style="--w:41%">1.1%</b></div><div class="win"><span>B · new page</span><b style="--w:100%">2.7%</b></div><span class="chip-lime">+145% MRR</span></div>''',
    'email': '''<svg class="viz-flow" viewBox="0 0 260 90" aria-hidden="true"><path id="fl" d="M24 45 H236" class="fl-line"/><circle cx="24" cy="45" r="13" class="fl-node"/><circle cx="130" cy="45" r="13" class="fl-node"/><circle cx="236" cy="45" r="13" class="fl-node fl-node--end"/><circle r="4" class="fl-dot"><animateMotion dur="2.4s" repeatCount="indefinite" path="M24 45 H236"/></circle><circle r="4" class="fl-dot"><animateMotion dur="2.4s" begin="1.2s" repeatCount="indefinite" path="M24 45 H236"/></circle><text x="24" y="80" text-anchor="middle">signup</text><text x="130" y="80" text-anchor="middle">welcome</text><text x="236" y="80" text-anchor="middle">repeat</text></svg>''',
    'strategy': '''<svg class="viz-radar" viewBox="0 0 140 130" aria-hidden="true"><g class="rd-grid"><polygon points="70,8 128,50 106,118 34,118 12,50"/><polygon points="70,30 107,57 93,100 47,100 33,57"/><polygon points="70,52 86,64 80,82 60,82 54,64"/></g><polygon class="rd-shape" points="70,16 118,53 98,108 44,104 22,56"/></svg>''',
}

def home():
    P = ''
    S = SITE_DATA
    one = ''.join(f'<span>{E(c)}{STAR}</span>' for c in CLIENTS)
    stats = ''.join(f'<div class="stat rv"><p class="stat__v"><span data-count="{n["value"]}" data-decimals="{n.get("decimals", 0)}">0</span><small>{E(n.get("suffix", ""))}</small></p><p class="stat__l">{E(n["label"])}</p></div>' for n in S['numbers'])
    manifesto = re.sub(r'\[(.+?)\]', r'<mark>\1</mark>', E(S['manifesto']))
    bento = ''.join(f'''<a class="bento__tile bento__tile--{s["id"]} rv" href="services/#{s["id"]}" data-cursor="Explore">
          <div class="bento__top"><span class="bento__n mono">0{i + 1}</span><span class="bento__go">{ARROW}</span></div>
          <div class="bento__viz">{SVC_VIZ[s["id"]]}</div>
          <h3>{E(s["title"])}</h3><p>{E(s["short"])}</p>
        </a>''' for i, s in enumerate(SERVICES))
    cases = S['caseStudies']
    steps = ''.join(f'''<article class="story__step" data-step="{i}">
            <p class="mono story__meta">Case {i + 1:02d} · {E(c["industry"])} · {E(c["year"])}</p>
            <h3>{E(c["title"])}</h3>
            <p>{E(c["summary"])}</p>
            <dl class="story__pa"><div><dt>Problem</dt><dd>{E(c["problem"])}</dd></div><div><dt>What I did</dt><dd>{E(c["approach"])}</dd></div><div><dt>Result</dt><dd>{E(c["result"])}</dd></div></dl>
            <div class="story__kpis">{"".join(kpi_chip(k) for k in c["kpis"])}</div>
          </article>''' for i, c in enumerate(cases))
    process = ''.join(f'<li class="pipe__step rv"><span class="pipe__n">0{i + 1}</span><h3>{E(p["title"])}</h3><p>{E(p["text"])}</p></li>' for i, p in enumerate(S['process']))
    stack = ''.join(f'<span class="tool">{E(t)}</span>' for row in S['stack'] for t in row)

    def yrs(period):
        a = re.findall(r'\d{4}', period); start = int(a[0]); end = 2026.9 if 'Now' in period else (int(a[1]) if len(a) > 1 else start + .95)
        return start, end
    lo, hi = 2020, 2027
    gantt = ''.join(f'''<li class="gantt__row rv"><div class="gantt__label"><b>{E(e["role"])}</b><span>{E(e["org"])} · {E(e["period"])}</span></div>
            <div class="gantt__track"><span class="gantt__bar{" is-now" if "Now" in e["period"] else ""}" style="--l:{(yrs(e["period"])[0] - lo) / (hi - lo) * 100:.1f}%;--w:{(yrs(e["period"])[1] - yrs(e["period"])[0]) / (hi - lo) * 100:.1f}%"></span></div>
            <p class="gantt__text">{E(e["text"])}</p></li>''' for e in S['experience'])
    axis = ''.join(f'<span>{y}</span>' for y in range(lo, hi))
    edu = ''.join(f'<li><small class="mono">{E(e["period"])}</small><b>{E(e["title"])}</b><span>{E(e["org"])}</span></li>' for e in S['education'])
    certs = ''.join(f'<li>{E(c)}</li>' for c in S['certifications'])
    quotes = ''.join(f'<figure class="quote rv"><blockquote>“{E(t["quote"])}”</blockquote><figcaption><span class="quote__av">{E(t["name"][0])}</span><span><b>{E(t["name"])}</b>{E(t["org"])} · demo</span></figcaption></figure>' for t in S['testimonials'])
    posts = ''.join(post_card('', p) for p in POSTS[:3])
    faq = [(f['q'], f['a']) for f in S['faq']]

    body = f'''    <section class="hero" id="top" data-spine="Intro">
      <div class="container">
        <div class="hero__head">
          <p class="eyebrow fade"><i class="pulse"></i>Manjil Shrestha · data-driven digital marketer · Melbourne</p>
          <h1 class="display display--hero" aria-label="Digital marketing expert in Melbourne">{title_lines(["Digital marketing", "*expert* in Melbourne."])}</h1>
        </div>
        <div class="hero__grid">
          <div class="hero__copy fade">
            <p class="hero__lead">I turn marketing from a guessing game into a growth curve you can read. SEO, paid media, analytics and CRO, all measured against revenue.</p>
            <div class="cta-row"><a class="btn btn--primary" href="book/" data-magnetic>Book a free consultation {ARROW}</a><a class="btn btn--ghost" href="#work">See the results</a></div>
            <ul class="hero__facts"><li><b>5+</b>years</li><li><b>3.4x</b>avg. ROAS</li><li><b>40+</b>campaigns</li></ul>
          </div>
          <figure class="hero__chart card fade" id="heroChart" data-cursor="Hover the chart">
            <div class="hc__head">
              <div><p class="mono hc__k" id="hcLabel">Organic enquiries / month</p><p class="hc__v"><span id="hcValue">143</span><span class="chip-lime" id="hcDelta">▲ 240%</span></p></div>
              <div class="tabs" role="tablist" aria-label="Chart metric"><button role="tab" aria-selected="true" data-series="leads">Leads</button><button role="tab" aria-selected="false" data-series="roas">ROAS</button><button role="tab" aria-selected="false" data-series="rev">Revenue</button></div>
            </div>
            <div class="hc__plot"><svg id="hcSvg" viewBox="0 0 720 300" preserveAspectRatio="none" aria-hidden="true"></svg><div class="hc__tip" id="hcTip" hidden></div></div>
            <div class="hc__axis mono" aria-hidden="true"><span>Dec</span><span>Feb</span><span>Apr</span><span>Jun</span><span>Aug</span><span>Oct</span><span>Nov</span></div>
            <figcaption class="mono hc__cap">Illustrative 12-month client trend · demo data</figcaption>
          </figure>
          <figure class="hero__me fade">
            <img src="assets/img/portrait.jpg" alt="Manjil Shrestha, digital marketing expert in Melbourne" width="1000" height="1371">
            <figcaption><span class="tagchip"><i class="pulse"></i>Melbourne, AU</span><span class="tagchip tagchip--lime">mastha</span></figcaption>
          </figure>
        </div>
      </div>
      <div class="marquee" aria-label="Clients (demo)"><div class="marquee__track">{one}{one}</div></div>
    </section>

    <section class="section" id="about" data-spine="About">
      <div class="container about">
        <div>
          {head_block("01 · About", "A marketer who reads the *numbers* first.")}
          <p class="statement rv">{manifesto}</p>
          <div class="cta-row rv"><a class="btn btn--ghost" href="contact/">Get in touch {ARROW}</a><a class="link" href="assets/Manjil-Shrestha-CV.pdf">Download CV</a></div>
        </div>
        <div class="stats">{stats}</div>
      </div>
    </section>

    <section class="section" id="services" data-spine="Services">
      <div class="container">
        {head_block("02 · Services", "Six levers. *One* growth curve.", "Pick one, or let me build the mix. Every lever is measured against revenue.", row=True)}
        <div class="bento">{bento}</div>
        <div class="cta-row cta-row--center rv"><a class="btn btn--primary" href="services/">All services &amp; pricing {ARROW}</a><a class="btn btn--ghost" href="services/seo/">SEO in Melbourne</a></div>
      </div>
    </section>

    <section class="section section--night" id="work" data-spine="Work">
      <div class="container">
        {head_block("03 · Selected work", "Results, *plotted.*", "Scroll through four engagements. The chart redraws for each one.", row=True)}
        <div class="story">
          <div class="story__stage">
            <div class="story__card">
              <div class="story__top"><p class="mono" id="stLabel">Case 01</p><p class="story__big" id="stBig">3.6x</p><p class="mono story__sub" id="stSub">ROAS</p></div>
              <svg id="stSvg" viewBox="0 0 600 300" preserveAspectRatio="none" aria-hidden="true"></svg>
              <div class="story__dots" id="stDots" aria-hidden="true"></div>
            </div>
          </div>
          <div class="story__steps">{steps}</div>
        </div>
      </div>
    </section>

    <section class="section" id="lab" data-spine="Lab">
      <div class="container">
        {head_block("04 · Growth lab", "Model your *upside.*", "Move the sliders. This is the back-of-envelope maths I run before every CRO engagement.", row=True)}
        <div class="lab card rv">
          <div class="lab__inputs">
            <label class="range"><span>Monthly visitors <output id="oV"></output></span><input type="range" id="iV" min="1000" max="200000" step="1000" value="{S["calculator"]["visitors"]}"></label>
            <label class="range"><span>Conversion rate <output id="oC"></output></span><input type="range" id="iC" min="0.2" max="10" step="0.1" value="{S["calculator"]["conversion"]}"></label>
            <label class="range"><span>Average order or lead value <output id="oA"></output></span><input type="range" id="iA" min="10" max="2000" step="10" value="{S["calculator"]["value"]}"></label>
            <label class="range"><span>Conversion lift <output id="oL"></output></span><input type="range" id="iL" min="5" max="100" step="5" value="{S["calculator"]["lift"]}"></label>
            <p class="mono small muted">Illustrative model, not a guarantee.</p>
          </div>
          <div class="lab__out">
            <p class="mono hc__k">Extra revenue in 12 months</p>
            <p class="lab__big" id="rY">$0</p>
            <svg id="labSvg" viewBox="0 0 520 220" preserveAspectRatio="none" aria-hidden="true"></svg>
            <div class="lab__legend mono"><span><i class="l1"></i>Today</span><span><i class="l2"></i>Optimised</span><span id="rM"></span></div>
            <a class="btn btn--primary btn--block" href="book/" data-magnetic>Let's make that real {ARROW}</a>
          </div>
        </div>
      </div>
    </section>

    <section class="section" id="process" data-spine="Process">
      <div class="container">
        {head_block("05 · Process", "A loop, *not* a launch.", "Five steps on every engagement. Each lap sharpens the next.", row=True)}
        <ol class="pipe"><span class="pipe__line" aria-hidden="true"><i id="pipeFill"></i></span>{process}</ol>
        <div class="tools rv">{stack}</div>
      </div>
    </section>

    <section class="section" id="experience" data-spine="Experience">
      <div class="container">
        {head_block("06 · Experience", "Where the *data habit* came from.")}
        <div class="exp">
          <div class="gantt card rv"><div class="gantt__axis mono" aria-hidden="true"><span></span><div>{axis}</div></div><ol>{gantt}</ol></div>
          <aside class="exp__side">
            <div class="card rv"><h3 class="card__h">Education</h3><ul class="edu">{edu}</ul></div>
            <div class="card rv"><h3 class="card__h">Certifications</h3><ul class="certs">{certs}</ul></div>
          </aside>
        </div>
      </div>
    </section>

    <section class="section" id="words" data-spine="Clients">
      <div class="container">
        {head_block("07 · Kind words", "What clients *say.*")}
        <div class="quotes">{quotes}</div>
      </div>
    </section>

    <section class="section" id="insights" data-spine="Insights">
      <div class="container">
        {head_block("08 · Insights", "Notes from the *dashboard.*", '<a class="link" href="blog/">All articles →</a>', row=True)}
        <div class="cards3">{posts}</div>
      </div>
    </section>

    <section class="section" id="faq" data-spine="FAQ">
      <div class="container faq">
        {head_block("09 · FAQ", "Questions before we *start.*", "Straight answers about working with a digital marketing expert in Melbourne.")}
        <div class="faq__list">{faq_list(faq)}</div>
      </div>
    </section>

    <section class="section" id="contact" data-spine="Contact">
      <div class="container">
        <div class="contact-band rv">
          <div class="contact-band__copy">
            <p class="eyebrow eyebrow--light"><i class="pulse"></i><span data-availability>Available</span></p>
            <h2 class="h2">Let's plot your <em>next quarter.</em></h2>
            <p>Tell me what you're trying to grow. I reply within one business day with an honest take.</p>
            <button class="email" data-copy-email><span data-email-text>hello@</span><em>Copy</em></button>
            <div class="socials" data-socials></div>
          </div>
          {contact_form("Project enquiry")}
        </div>
      </div>
    </section>'''
    person = json.dumps({"@context": "https://schema.org", "@type": "Person", "name": "Manjil Shrestha", "alternateName": "mastha", "jobTitle": "Digital Marketing Expert", "address": {"@type": "PostalAddress", "addressLocality": "Melbourne", "addressCountry": "AU"}, "url": SITE}, ensure_ascii=False)
    write('index.html', layout(P, '', 'Digital Marketing Expert in Melbourne | Manjil Shrestha', 'Manjil Shrestha is a data-driven digital marketing expert in Melbourne. SEO, paid media, GA4 analytics and CRO measured against revenue.', 'home', body, scripts=['home.js'], ld=[person, faq_ld(faq)]))

def contact_form(subject, P=''):
    return f'''<form class="form js-form" data-subject="{subject}" action="https://formspree.io/f/YOUR_FORM_ID" method="POST" novalidate>
            <div class="form__row"><label class="field"><span>Name</span><input name="name" required autocomplete="name" placeholder="Jane Smith"></label><label class="field"><span>Email</span><input type="email" name="email" required autocomplete="email" placeholder="jane@company.com.au"></label></div>
            <fieldset class="chips"><legend>I need help with</legend>{"".join(f'<label><input type="checkbox" name="needs" value="{v}"><span>{v}</span></label>' for v in ["SEO", "Paid ads", "Analytics", "CRO", "Email", "Full-time role"])}</fieldset>
            <label class="field"><span>Monthly budget</span><select name="budget"><option value="">Not sure yet</option><option>Under $2k</option><option>$2k – $5k</option><option>$5k – $15k</option><option>$15k+</option></select></label>
            <label class="field"><span>What are you trying to grow?</span><textarea name="message" rows="4" required placeholder="A couple of lines about the business, the goal and the timeline."></textarea></label>
            <input type="text" name="_gotcha" tabindex="-1" autocomplete="off" class="hp" aria-hidden="true">
            <div class="form__foot"><button type="submit" class="btn btn--primary btn--lg" data-magnetic><span class="btn__text">Send message</span><span class="btn__sent">Sent. Talk soon ✓</span></button><p class="mono small" data-form-note>No spam. Just a reply.</p></div>
          </form>'''

def post_card(P, p, cls='pcard rv'):
    ex = E(p["dek"][:120].rsplit(" ", 1)[0]) + '…'
    return f'''<a class="{cls}" href="{P}blog/{p["slug"]}/" data-post data-tags="{p["tagkey"]}" data-text="{E((p["title"] + " " + p["dek"] + " " + p["tag"]).lower())}" data-cursor="Read">
          <div class="pcard__cover">{cover_svg(p["seed"], uid="p" + p["slug"][:3])}<span class="tagchip">{E(p["tag"])}</span></div>
          <div class="pcard__body"><p class="mono pcard__meta">{fmt_date(p["date"])} · {p["minutes"]} min</p><h3>{E(p["title"])}</h3><p>{ex}</p><span class="pcard__more">Read article {ARROW}</span></div>
        </a>'''

# ============================================================ SERVICES
SVC_FAQ = [
    ("Do you lock clients into long contracts?", "No. Audits and sprints are fixed-scope. Retainers run month to month after the first 90 days, because that is how long it takes to see a real trend."),
    ("Is ad spend included in the price?", "No. Ad spend is paid directly to Google, Meta or LinkedIn from your own account, so you always own the account and the data."),
    ("Can you work alongside my current agency or team?", "Yes. I often handle analytics, strategy or CRO while an agency or in-house team runs execution, and I write briefs they can act on."),
    ("What do you need from me to start?", "Access to your analytics and ad accounts, your revenue or lead numbers for the last 12 months, and one person who can make decisions."),
    ("How and when do you report?", "A short written update every week and a Looker Studio dashboard you can open any time. Monthly, we review results against the targets we agreed."),
]
PLANS = [
    ("Diagnose", "Growth Audit", "$1,500", "one-off", "A clear, honest picture first.", ["Analytics and tracking audit", "Channel performance review", "Funnel and landing page review", "Prioritised 90-day roadmap", "60-minute walkthrough"], False),
    ("Build", "90-Day Growth Sprint", "$4,500", "/ month · 3 months", "Move one or two numbers, fast.", ["Everything in the audit", "Tracking fixed, dashboard built", "Execution in 1–2 channels", "Weekly tests and optimisation", "Weekly update, monthly review"], True),
    ("Lead", "Fractional CMO", "$3,000", "/ month · ongoing", "Senior marketing leadership.", ["Quarterly growth plan and budget", "Agency and freelancer management", "Hiring support and briefs", "Weekly team check-in", "Monthly board-ready report"], False),
]

def plans_html(P, plans):
    return ''.join(f'''<article class="plan rv{" plan--hot" if hot else ""}">
          {'<span class="plan__badge">Most popular</span>' if hot else ''}
          <p class="mono plan__k">{E(k)}</p><h3>{E(n)}</h3><p class="plan__for">{E(f)}</p>
          <p class="plan__price">{E(pr)}<small>{E(u)}</small></p>
          <ul class="checks">{"".join(f"<li>{E(x)}</li>" for x in items)}</ul>
          <a class="btn {"btn--lime" if hot else "btn--ghost"} btn--block" href="{P}book/">{"Start this plan" if hot else "Start here"} {ARROW}</a>
        </article>''' for k, n, pr, u, f, items, hot in plans)

def services():
    P = '../'
    idx = ''.join(f'<a href="#{s["id"]}"><b class="mono">0{i + 1}</b>{E(s["title"])}</a>' for i, s in enumerate(SERVICES))
    items = ''.join(f'''<article class="svcx__item card rv" id="{s["id"]}">
          <div class="svcx__head"><span class="svcx__icon">{ICONS[s["id"]]}</span><div><p class="mono">0{i + 1} / 06</p><h2>{E(s["title"])}</h2><p class="svcx__short">{E(s["short"])}</p></div>{line_chart(s["spark"], 200, 70, grid=False, cls="svcx__spark")}</div>
          <div class="svcx__body">
            <div><h3 class="mono">What it is</h3><p>{E(s["what"])}</p><h3 class="mono">Who it's for</h3><p>{E(s["who"])}</p></div>
            <div><h3 class="mono">What you get</h3><ul class="checks">{"".join(f"<li>{E(d)}</li>" for d in s["deliver"])}</ul></div>
          </div>
          <div class="svcx__foot"><div class="kpis-inline"><span class="mono">Measured by</span>{"".join(f"<span class=tagchip>{E(k)}</span>" for k in s["kpis"])}</div><div class="facts"><div><span class="mono">First results</span><b>{E(s["first"])}</b></div><div><span class="mono">Investment</span><b>{E(s["price"])}</b></div></div></div>
          {'<a class="btn btn--primary btn--sm" href="seo/">Explore SEO in depth ' + ARROW + '</a>' if s["id"] == "seo" else ''}
        </article>''' for i, s in enumerate(SERVICES))
    aside = f'''<div class="phero__aside card fade"><p class="mono hc__k">Every service, one metric</p><ul class="mini-list">{"".join(f'<li><span>{E(s["title"])}</span><b>{E(s["kpis"][0])}</b></li>' for s in SERVICES)}</ul></div>'''
    compare_rows = [("Tracking & analytics audit", "✓", "✓", "✓"), ("Prioritised roadmap", "✓", "✓", "✓"), ("Hands-on execution", "—", "1–2 channels", "Via your team"), ("Weekly reporting", "—", "✓", "✓"), ("Agency & hiring management", "—", "—", "✓"), ("Commitment", "2 weeks", "3 months", "Month to month")]
    compare = ''.join(f'<tr><th scope="row">{E(r[0])}</th>' + ''.join(f'<td>{E(c)}</td>' for c in r[1:]) + '</tr>' for r in compare_rows)
    body = phero(P, [("Home", ""), ("Services", "services/")], "Services · Melbourne & remote", ["Marketing that", "pays for *itself.*"],
                 "Six services, one rule: if it can't be measured, it doesn't get budget. Pick the one you need, or let me build the right mix.",
                 f'<a class="btn btn--primary" href="{P}book/" data-magnetic>Book a free consultation {ARROW}</a><a class="btn btn--ghost" href="#pricing">See pricing</a>', aside) + f'''

    <section class="section section--tight" data-spine="Services">
      <div class="container svcx">
        <aside class="svcx__index card"><p class="mono">All services</p><nav aria-label="Services">{idx}</nav><a class="btn btn--ghost btn--sm btn--block" href="{P}book/">Not sure? Ask me</a></aside>
        <div class="svcx__list">{items}</div>
      </div>
    </section>

    <section class="section" id="pricing" data-spine="Pricing">
      <div class="container">
        {head_block("Packages", "Three ways to *work* together.", "Start with an audit, run a focused sprint, or bring me in as your part-time head of marketing.", row=True)}
        <div class="plans">{plans_html(P, PLANS)}</div>
        <div class="compare card rv"><table><thead><tr><th></th><th>Audit</th><th>Sprint</th><th>Fractional CMO</th></tr></thead><tbody>{compare}</tbody></table></div>
        <p class="fine mono">Demo pricing in AUD, excluding GST. Final scope confirmed after a free call.</p>
      </div>
    </section>

    <section class="section section--night" data-spine="Process">
      <div class="container">
        {head_block("How it works", "A loop, *not* a launch.")}
        <ol class="pipe pipe--night"><span class="pipe__line" aria-hidden="true"><i></i></span>{"".join(f'<li class="pipe__step rv"><span class="pipe__n">0{i + 1}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate([("Diagnose", "Audit data, funnel and market. Find the leaks."), ("Strategy", "Agree targets and the channels that can hit them."), ("Build", "Tracking, campaigns, pages and flows, instrumented."), ("Measure", "Weekly reporting in a dashboard you own."), ("Scale", "Double down on what the data proves.")]))}</ol>
      </div>
    </section>

    <section class="section section--tight" data-spine="FAQ">
      <div class="container faq">
        {head_block("Services FAQ", "Before you *ask.*")}
        <div class="faq__list">{faq_list(SVC_FAQ)}</div>
      </div>
    </section>
{cta_band(P, "Not sure which service fits? That's what the *free call* is for.", "30 minutes, your numbers, my honest take.")}'''
    write('services/index.html', layout(P, 'services/', 'Digital Marketing Services in Melbourne | Manjil Shrestha', 'SEO, paid media, analytics, CRO, email and fractional CMO services from a data-driven digital marketing expert in Melbourne.', 'services', body, scripts=['pages.js'], ld=[faq_ld(SVC_FAQ)]))

def cta_band(P, title, sub):
    t = re.sub(r'\*(.+?)\*', r'<em>\1</em>', title)
    return f'''    <section class="section section--tight" data-spine="Next step">
      <div class="container"><div class="cta rv"><div><h2 class="h2">{t}</h2><p>{sub}</p></div><a class="btn btn--lime btn--lg" href="{P}book/" data-magnetic>Book a free consultation {ARROW}</a></div></div>
    </section>'''

# ============================================================ SEO SERVICE PAGE
SEO_FAQ = [
    ("How long does SEO take to work in Melbourne?", "Technical fixes and Google Business Profile improvements can move rankings within weeks. Meaningful growth in organic leads usually takes three to six months, and it compounds from there."),
    ("Do you guarantee number one rankings?", "No, and be wary of anyone who does. Nobody controls Google. I commit to the work, the reporting and the leads trend, and you can see every change I make."),
    ("What's the difference between local SEO and regular SEO?", "Local SEO targets searches with a place attached, like a suburb or \"near me\", and leans on your Google Business Profile, reviews and suburb pages. Most Melbourne service businesses need both."),
    ("Do I need to write the content myself?", "No. I write briefs and can produce the content, or work with your writer. You review everything before it goes live."),
    ("How do you report on SEO?", "A monthly report and a live Looker Studio dashboard showing rankings, organic traffic and, most importantly, the enquiries and revenue organic search produced."),
]
SEO_CHECKS = ["Your site loads in under 3 seconds on a phone", "Every key service has its own page", "You have pages for the suburbs you serve", "Your Google Business Profile is complete with recent photos",
              "You got at least two new Google reviews last month", "You track enquiries from organic search in GA4", "Each page has a unique title and meta description", "You published something useful in the last 60 days"]

def seo():
    P = '../../'
    serp = f'''<div class="serp card fade" id="serp">
            <div class="serp__bar"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="7" cy="7" r="5"/><path d="M11 11l3.5 3.5"/></svg><span>emergency plumber fitzroy</span></div>
            <ol class="serp__list">
              <li class="serp__you"><b class="serp__rank" id="serpRank">#9</b><div><small>yourbusiness.com.au › fitzroy</small><strong>Emergency Plumber Fitzroy · 24/7, 60-min Callouts</strong><span>★★★★★ 4.9 · 186 reviews</span></div></li>
              <li><b>#2</b><div><small>competitor-one.com.au</small><strong>Plumbers Melbourne · Call Today</strong></div></li>
              <li><b>#3</b><div><small>directory-site.com.au</small><strong>Top 10 Plumbers in Fitzroy</strong></div></li>
            </ol>
            <p class="serp__foot mono"><span id="serpNote">Month 0</span><span>Illustrative · demo</span></p>
          </div>'''
    roadmap = [("Audit & fix", 0, 1.2, ["Technical audit", "GA4 tracking", "Critical fixes"]), ("Architecture", 0.9, 2.2, ["Keyword map", "Service pages", "First suburb pages"]),
               ("Local & content", 2, 3.4, ["GBP optimised", "Review engine", "Content cadence"]), ("Compound", 3.2, 6, ["More suburbs", "Local PR", "Double down"])]
    gantt = ''.join(f'<li class="gantt__row rv"><div class="gantt__label"><b>{E(n)}</b><span>{" · ".join(E(x) for x in t)}</span></div><div class="gantt__track"><span class="gantt__bar" style="--l:{a / 6 * 100:.1f}%;--w:{(b - a) / 6 * 100:.1f}%"></span></div></li>' for n, a, b, t in roadmap)
    incl = [("seo", "Technical SEO", "Speed, Core Web Vitals, crawlability, indexing, schema and structure."), ("strategy", "Keyword strategy", "A keyword map from real Melbourne demand, matched to pages that can win."),
            ("cro", "Local SEO & GBP", "Google Business Profile, suburb pages, reviews and citations."), ("email", "On-page & content", "Service pages and articles that answer real questions and convert."),
            ("paid", "Links & local PR", "Earned mentions from Melbourne publications and partners. No link farms."), ("analytics", "Tracking & reporting", "Organic enquiries and revenue tracked in GA4, live dashboard.")]
    incl_html = ''.join(f'<article class="feature card rv"><span class="svcx__icon">{ICONS[ic]}</span><h3>{E(t)}</h3><p>{E(d)}</p></article>' for ic, t, d in incl)
    seo_plans = [("One-off", "SEO Audit", "$1,500", "one-off", "A full diagnosis and fix list.", ["Technical and on-page audit", "Keyword and competitor gaps", "Local SEO and GBP review", "Prioritised 90-day plan", "60-minute walkthrough"], False),
                 ("Monthly", "Local SEO", "$1,800", "/ month", "Win in the suburbs you serve.", ["Everything in the audit", "Up to 5 suburb or service pages a month", "GBP management and reviews", "Local citations and PR", "Monthly report and dashboard"], True),
                 ("Monthly", "Growth SEO", "$3,200", "/ month", "eCommerce and multi-location.", ["Everything in Local SEO", "Category and product SEO", "4 long-form articles a month", "Digital PR outreach", "Fortnightly strategy call"], False)]
    checks = ''.join(f'<li><label><input type="checkbox" class="qc"><span>{E(c)}</span></label></li>' for c in SEO_CHECKS)
    body = phero(P, [("Home", ""), ("Services", "services/"), ("SEO", "services/seo/")], "Service · Search & SEO", ["SEO services", "in *Melbourne.*"],
                 "Rank for what your customers actually search, suburb by suburb. Technical fixes, local SEO, content and tracking that ties every ranking to a real enquiry.",
                 f'<a class="btn btn--primary" href="{P}book/" data-magnetic>Get a free SEO audit call {ARROW}</a><a class="btn btn--ghost" href="#pricing">See SEO pricing</a>', serp) + f'''

    <section class="section section--tight" data-spine="Problem">
      <div class="container">
        {head_block("Sound familiar?", "You're paying for every click because *Google* can't find you.")}
        <div class="cards3">
          <div class="pain card rv"><span class="pain__x">✕</span><h3>Invisible in your own suburbs</h3><p>Competitors with worse reviews show up first in the map pack.</p></div>
          <div class="pain card rv"><span class="pain__x">✕</span><h3>Ads do all the work</h3><p>Turn the ads off and the phone stops ringing.</p></div>
          <div class="pain card rv"><span class="pain__x">✕</span><h3>Traffic, no enquiries</h3><p>Ranking reports that nobody could connect to revenue.</p></div>
        </div>
      </div>
    </section>

    <section class="section section--tight" data-spine="Included">
      <div class="container">
        {head_block("What's included", "Six parts, one *system.*", "Every engagement covers all six, weighted to your biggest gaps.", row=True)}
        <div class="cards3">{incl_html}</div>
      </div>
    </section>

    <section class="section section--night" data-spine="Roadmap">
      <div class="container">
        {head_block("The roadmap", "Your first *six months.*")}
        <div class="gantt gantt--night card rv"><div class="gantt__axis mono" aria-hidden="true"><span></span><div>{"".join(f"<span>M{m}</span>" for m in range(1, 7))}</div></div><ol>{gantt}</ol></div>
      </div>
    </section>

    <section class="section section--tight" data-spine="Health check">
      <div class="container qc">
        <div>
          {head_block("Free SEO health check", "How healthy is your *SEO?*", "Tick what's true. Thirty seconds, no email required.")}
          <ul class="qc__list card rv">{checks}</ul>
        </div>
        <aside class="qc__score card rv" aria-live="polite">
          <p class="mono hc__k">Your score</p>
          <p class="qc__num"><span id="qcNum">0</span><small>/{len(SEO_CHECKS)}</small></p>
          <div class="meter"><i id="qcBar"></i></div>
          <h3 id="qcTitle">Start ticking</h3>
          <p id="qcText" class="muted">Your result and the first thing to fix appear here.</p>
          <a class="btn btn--primary btn--block" href="{P}book/">Book a free SEO audit call {ARROW}</a>
        </aside>
      </div>
    </section>

    <section class="section section--tight" data-spine="Case">
      <div class="container">
        <article class="casemini card rv">
          <div class="casemini__body">
            <p class="mono">Case · Home services · demo</p>
            <h2 class="h3">Owning local search across 60+ Melbourne suburbs</h2>
            <p class="muted">Suburb pages, Core Web Vitals fixes and a monthly GBP and content routine took organic search from under 5% of enquiries to the largest lead source.</p>
            <div class="story__kpis story__kpis--light"><span><b>+212%</b>Organic enquiries</span><span><b>63</b>Top-3 keywords</span><span><b>-33%</b>Blended CPL</span></div>
          </div>
          <div class="casemini__chart">{line_chart([4, 5, 5, 7, 9, 12, 15, 17, 21, 24, 27, 31], 520, 260, dots=True)}</div>
        </article>
      </div>
    </section>

    <section class="section" id="pricing" data-spine="Pricing">
      <div class="container">
        {head_block("SEO pricing", "Clear prices, *no* lock-in.", "Start with an audit or go straight to a monthly programme.", row=True)}
        <div class="plans">{plans_html(P, seo_plans)}</div>
        <p class="fine mono">Demo pricing in AUD, excluding GST.</p>
      </div>
    </section>

    <section class="section section--tight" data-spine="FAQ">
      <div class="container faq">
        {head_block("SEO FAQ", "Straight *answers.*", f'Still unsure? <a class="link" href="{P}contact/">Ask me directly.</a>')}
        <div class="faq__list">{faq_list(SEO_FAQ)}</div>
      </div>
    </section>
{cta_band(P, "Find out what's stopping you *ranking.*", "Free 30-minute SEO audit call. Three things I'd fix first.")}'''
    write('services/seo/index.html', layout(P, 'services/seo/', 'SEO Services in Melbourne | Manjil Shrestha', 'SEO services in Melbourne: technical SEO, local SEO, content and tracking that turns rankings into enquiries.', 'services', body, scripts=['pages.js'], ld=[faq_ld(SEO_FAQ)]))

# ============================================================ BOOK
BOOK_FAQ = [("Is the consultation really free?", "Yes. No card, no invoice afterwards, no obligation."), ("What happens in the call?", "We look at your goals and numbers, I point out the two or three biggest opportunities, and you leave with next steps."),
            ("Can I reschedule?", "Of course. Reply to the confirmation email with a better time."), ("Will you sign an NDA?", "Happy to. Send it before the call.")]

def book():
    P = '../'
    body = phero(P, [("Home", ""), ("Book a free consultation", "book/")], "Free consultation · 30 min", ["Book a free", "*consultation.*"],
                 "Your numbers, my honest take. No pitch deck and no obligation. You'll leave with the two or three moves I'd make first.",
                 '<span class="tagchip">30 min · video call</span><span class="tagchip">Free</span><span class="tagchip">Melbourne time</span>') + f'''

    <section class="section section--tight" data-spine="Pick a time" style="padding-top:0">
      <div class="container book">
        <div class="booker card rv" id="booker">
          <ol class="stepper"><li class="is-on"><b>1</b><span>Pick a time</span></li><li><b>2</b><span>Your details</span></li><li><b>3</b><span>Confirmed</span></li></ol>
          <div class="panel-step is-on" data-step="1">
            <div class="picker">
              <div class="cal">
                <div class="cal__head"><h3 id="calMonth">Month</h3><div class="cal__nav"><button type="button" id="calPrev" aria-label="Previous month">←</button><button type="button" id="calNext" aria-label="Next month">→</button></div></div>
                <div class="cal__dow"><span>Mon</span><span>Tue</span><span>Wed</span><span>Thu</span><span>Fri</span><span>Sat</span><span>Sun</span></div>
                <div class="cal__days" id="calDays"></div>
              </div>
              <div class="slots"><h4 id="slotsDay">Day</h4><p class="slots__tz mono" id="slotsTz"></p><div class="slots__list" id="slotsList"></div></div>
            </div>
          </div>
          <div class="panel-step" data-step="2">
            <form class="form form--flat" id="bookForm" action="https://formspree.io/f/YOUR_FORM_ID" method="POST" novalidate>
              <div class="picked"><span id="pickedText"></span><button type="button" data-back>Change</button></div>
              <input type="hidden" name="slot" id="bfSlot">
              <div class="form__row"><label class="field"><span>Name</span><input name="name" required autocomplete="name"></label><label class="field"><span>Email</span><input type="email" name="email" required autocomplete="email"></label></div>
              <label class="field"><span>Website</span><input name="website" placeholder="company.com.au"></label>
              <div class="form__row"><label class="field"><span>Main focus</span><select name="focus"><option value="">Not sure yet</option><option>SEO</option><option>Paid media</option><option>Analytics &amp; tracking</option><option>Conversion (CRO)</option><option>Email &amp; lifecycle</option><option>Overall strategy</option><option>Full-time role</option></select></label>
              <label class="field"><span>Monthly budget</span><select name="budget"><option value="">Prefer not to say</option><option>Under $2k</option><option>$2k – $5k</option><option>$5k – $15k</option><option>$15k+</option></select></label></div>
              <label class="field"><span>What would make this call worth it?</span><textarea name="notes" rows="3"></textarea></label>
              <input type="text" name="_gotcha" tabindex="-1" autocomplete="off" class="hp" aria-hidden="true">
              <div class="form__foot"><button type="button" class="btn btn--ghost" data-back>← Back</button><button type="submit" class="btn btn--primary btn--lg">Request this time {ARROW}</button></div>
              <p class="mono small" data-form-note>I'll confirm by email with a meeting link.</p>
            </form>
          </div>
          <div class="panel-step" data-step="3">
            <div class="confirm"><span class="confirm__icon">✓</span><h3>Your time is requested.</h3><p>I'll confirm by email within one business day with a meeting link.</p>
              <div class="confirm__card"><div><span>When</span><b id="cWhen"></b></div><div><span>Who</span><b id="cWho"></b></div><div><span>Focus</span><b id="cFocus"></b></div></div>
              <div class="cta-row cta-row--center"><a class="btn btn--primary" id="gcalLink" target="_blank" rel="noopener">Add to Google Calendar</a><a class="btn btn--ghost" id="icsLink" download="consultation.ics">Download .ics</a></div></div>
          </div>
          <div class="booker__bar" id="bookBar"><p class="mono" id="bookSum"></p><button type="button" class="btn btn--primary" id="toDetails" disabled>Continue {ARROW}</button></div>
        </div>
        <aside class="side">
          <div class="card rv"><h3 class="card__h">What we'll cover</h3><ol class="agenda"><li><b>01</b><div><strong>Your goal</strong><span>The one number to move.</span></div></li><li><b>02</b><div><strong>Your data</strong><span>Analytics and ad accounts.</span></div></li><li><b>03</b><div><strong>Quick wins</strong><span>The moves I'd make first.</span></div></li><li><b>04</b><div><strong>Next steps</strong><span>With me or without.</span></div></li></ol></div>
          <div class="card rv me-card"><img src="{P}assets/img/avatar.png" alt="Manjil Shrestha" width="64" height="64"><div><strong>Manjil Shrestha</strong><span class="mono">mastha · Melbourne</span><p class="small"><i class="pulse"></i> <span data-availability>Available</span></p></div></div>
        </aside>
      </div>
    </section>

    <section class="section section--tight" data-spine="FAQ">
      <div class="container faq">
        {head_block("Booking FAQ", "Good *questions.*")}
        <div class="faq__list">{faq_list(BOOK_FAQ)}</div>
      </div>
    </section>'''
    write('book/index.html', layout(P, 'book/', 'Book a Free Marketing Consultation in Melbourne | Manjil Shrestha', 'Book a free 30-minute marketing consultation with a data-driven digital marketing expert in Melbourne.', 'book', body, scripts=['book.js'], ld=[faq_ld(BOOK_FAQ)]))

# ============================================================ CONTACT
CONTACT_FAQ = [("Which areas do you work with?", "Melbourne and the rest of Australia. Most work is remote, with in-person workshops around Melbourne."), ("Are you open to full-time roles?", "Yes, for the right team. Choose \"Full-time role\" in the form."), ("How quickly do you reply?", "Within one business day, usually the same day.")]

def contact():
    P = '../'
    days = [("Mon", "9:00 – 18:00"), ("Tue", "9:00 – 18:00"), ("Wed", "9:00 – 18:00"), ("Thu", "9:00 – 18:00"), ("Fri", "9:00 – 17:00"), ("Sat", "Closed"), ("Sun", "Closed")]
    aside = f'''<div class="clockcard card fade"><p class="mono hc__k">Right now in Melbourne</p><p class="clock" id="mClock">--:--</p><p class="status"><i class="pulse"></i><span id="mStatus">Checking…</span></p>
            <svg class="orbit" viewBox="0 0 200 120" aria-hidden="true"><ellipse cx="100" cy="60" rx="90" ry="40"/><ellipse cx="100" cy="60" rx="60" ry="26"/><circle cx="100" cy="60" r="6" class="orbit__c"/><circle r="5" class="orbit__p"><animateMotion dur="6s" repeatCount="indefinite" path="M10,60 a90,40 0 1,0 180,0 a90,40 0 1,0 -180,0"/></circle></svg></div>'''
    methods = [("mail", "Email", '<span data-email-text>hello@</span>', "Copy address", 'button', 'data-copy-email'), ("cal", "Book a call", "Free 30 minutes, pick a time.", "Choose a time", 'a', f'href="{P}book/"'),
               ("in", "LinkedIn", "Connect or message me there.", "Open profile", 'a', 'href="https://www.linkedin.com/in/manjilshrestha" target="_blank" rel="noopener"'), ("brief", "Hiring?", "Open to the right in-house role.", "Download CV", 'a', f'href="{P}assets/Manjil-Shrestha-CV.pdf"')]
    mhtml = ''.join(f'<{tag} class="method card rv" {attr}><span class="svcx__icon">{ICONS[ic]}</span><h3>{t}</h3><p>{d}</p><span class="link">{go} →</span></{tag}>' for ic, t, d, go, tag, attr in methods)
    body = phero(P, [("Home", ""), ("Contact", "contact/")], "Contact", ["Let's make", "your data *talk.*"],
                 "New project, a second opinion on your numbers, a full-time role or a podcast invite. I reply within one business day.", '', aside) + f'''

    <section class="section section--tight" data-spine="Ways in" style="padding-top:0">
      <div class="container"><div class="cards4">{mhtml}</div></div>
    </section>

    <section class="section section--tight" data-spine="Message">
      <div class="container contact2">
        <div class="card form-card rv">{contact_form("Website enquiry", P)}</div>
        <aside class="side">
          <div class="card rv"><h3 class="card__h">Office hours · Melbourne</h3><ul class="hours">{"".join(f'<li data-day="{d}"><span>{d}</span><span>{h}</span></li>' for d, h in days)}</ul></div>
          <div class="card rv"><h3 class="card__h">Elsewhere</h3><div class="socials" data-socials></div></div>
        </aside>
      </div>
    </section>

    <section class="section section--tight" data-spine="FAQ">
      <div class="container faq">
        {head_block("Quick answers", "Good to *know.*")}
        <div class="faq__list">{faq_list(CONTACT_FAQ)}</div>
      </div>
    </section>'''
    write('contact/index.html', layout(P, 'contact/', 'Contact Manjil Shrestha | Digital Marketing Expert in Melbourne', 'Get in touch with Manjil Shrestha, a data-driven digital marketing expert in Melbourne.', 'contact', body, scripts=['pages.js'], ld=[faq_ld(CONTACT_FAQ)]))

# ============================================================ BLOG
def blog_index():
    P = '../'
    feat = POSTS[0]
    soon = ''.join(f'''<div class="pcard post--soon rv" data-post data-tags="{s["tagkey"]}" data-text="{E((s["title"] + " " + s["dek"]).lower())}" aria-disabled="true">
          <div class="pcard__cover">{cover_svg(20 + j, uid="s")}<span class="tagchip">{E(s["tag"])}</span><span class="soon">In the works</span></div>
          <div class="pcard__body"><p class="mono pcard__meta">Coming soon</p><h3>{E(s["title"])}</h3><p>{E(s["dek"])}</p></div></div>''' for j, s in enumerate(SOON))
    newsletter = f'''<form class="newsletter js-form" data-subject="Newsletter signup" action="https://formspree.io/f/YOUR_FORM_ID" method="POST" novalidate><label class="sr" for="nl">Email</label><input id="nl" type="email" name="email" required placeholder="you@company.com.au" autocomplete="email"><input type="text" name="_gotcha" tabindex="-1" autocomplete="off" class="hp" aria-hidden="true"><button class="btn btn--primary" type="submit"><span class="btn__text">Get new posts</span><span class="btn__sent">Subscribed ✓</span></button></form>'''
    aside = f'''<div class="phero__aside card fade"><p class="mono hc__k">The newsletter</p><p class="h3">One email a month. Zero fluff.</p>{newsletter}<p class="mono small muted">Unsubscribe any time.</p></div>'''
    body = phero(P, [("Home", ""), ("Blog", "blog/")], "Blog · notes from the dashboard", ["Notes from", "the *dashboard.*"],
                 "Field notes on analytics, SEO, paid media and CRO for Melbourne businesses. What moved the numbers, and how to do it yourself.", '', aside) + f'''

    <section class="section section--tight" id="articles" data-spine="Articles" style="padding-top:0">
      <div class="container">
        <div class="blog-tools">
          <div class="filters" role="group" aria-label="Filter by topic">{"".join(f'<button class="filter{" is-on" if k == "all" else ""}" data-filter="{k}">{n}</button>' for k, n in [("all", "All"), ("analytics", "Analytics"), ("local-seo", "Local SEO"), ("paid-media", "Paid Media"), ("cro", "CRO"), ("email", "Email")])}</div>
          <label class="search"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="7" cy="7" r="5"/><path d="M11 11l3.5 3.5"/></svg><input type="search" id="postSearch" placeholder="Search articles" aria-label="Search articles"><span class="mono" id="postCount"></span></label>
        </div>
        <a class="feature-post card rv" href="{feat["slug"]}/" data-post data-tags="{feat["tagkey"]}" data-text="{E((feat["title"] + " " + feat["dek"]).lower())}" data-cursor="Read">
          <div class="feature-post__cover">{cover_svg(feat["seed"], 900, 560, uid="f")}</div>
          <div class="feature-post__body"><p><span class="tagchip tagchip--lime">Featured</span> <span class="tagchip">{E(feat["tag"])}</span></p><h2 class="h3">{E(feat["title"])}</h2><p class="muted">{E(feat["dek"])}</p>
            <p class="byline mono"><img src="{P}assets/img/avatar.png" alt="" width="28" height="28">Manjil Shrestha · {fmt_date(feat["date"])} · {feat["minutes"]} min</p><span class="pcard__more">Read the article {ARROW}</span></div>
        </a>
        <div class="cards3">{"".join(post_card(P, p) for p in POSTS[1:])}{soon}</div>
        <p class="empty" id="emptyState">Nothing matches yet. Try another topic, or <a class="link" href="{P}contact/">suggest an article</a>.</p>
      </div>
    </section>

    <section class="section section--tight" data-spine="Topics">
      <div class="container">
        {head_block("Browse by topic", "Pick your *rabbit hole.*")}
        <div class="cards4">{"".join(f'<button class="topic card rv" data-topic="{k}"><h3>{n}</h3><p>{d}</p><span class="mono">{c}</span></button>' for k, n, d, c in [("analytics", "Analytics", "GA4, tracking, attribution, dashboards.", "1 article"), ("local-seo", "Local SEO", "Ranking in Melbourne suburbs.", "1 article"), ("paid-media", "Paid Media", "Budgets, bidding and creative.", "1 article"), ("cro", "CRO", "Tests, landing pages, funnels.", "Coming soon")])}</div>
      </div>
    </section>
{cta_band(P, "Rather have me *look* at your numbers?", "A free 30-minute call with your real data is faster than reading.")}'''
    write('blog/index.html', layout(P, 'blog/', 'Digital Marketing Blog | Analytics, SEO & Ads | Manjil Shrestha', 'Practical articles on GA4, local SEO, paid media and CRO from a digital marketing expert in Melbourne.', 'blog', body, scripts=['blog.js']))

def restyle_body(h):
    h = re.sub(r'<span class="note uv note--margin" data-note><span>(.*?)</span></span>', r'<span class="annot"><b>Side note</b>\1</span>', h, flags=re.S)
    return h.replace('class="num"', 'class="hnum"')

def article(p, i, template=False):
    P = '../../'
    path = f'blog/{p["slug"]}/'
    prev_p = POSTS[i - 1] if i > 0 else None
    next_p = POSTS[i + 1] if i + 1 < len(POSTS) else None
    nav = '' if template else '<nav class="post-nav" aria-label="More articles">' + (f'<a class="card" href="{P}blog/{prev_p["slug"]}/"><span class="mono">← Newer</span><b>{E(prev_p["title"])}</b></a>' if prev_p else '<span></span>') + (f'<a class="card" href="{P}blog/{next_p["slug"]}/"><span class="mono">Older →</span><b>{E(next_p["title"])}</b></a>' if next_p else '<span></span>') + '</nav>'
    related = ''.join(post_card(P, q) for q in POSTS if q is not p)[:]
    body = f'''    <article>
      <header class="phero phero--post" id="top" data-spine="Top">
        <div class="container">
          {crumbs(P, [("Home", ""), ("Blog", "blog/"), (p["tag"], "blog/")])}
          <div class="post-head">
            <p class="fade"><span class="tagchip tagchip--lime">{E(p["tag"])}</span></p>
            <h1 class="post-title fade">{E(p["title"])}</h1>
            <p class="dek fade">{E(p["dek"])}</p>
            <div class="post-meta fade">
              <div class="author"><img src="{P}assets/img/avatar.png" alt="" width="44" height="44"><div><b>Manjil Shrestha</b><span class="mono">Digital marketer · Melbourne</span></div></div>
              <span class="mono">{fmt_date(p["date"])} · {p["minutes"]} min read</span>
              <div class="share"><a data-share="linkedin" target="_blank" rel="noopener" aria-label="Share on LinkedIn">in</a><a data-share="x" target="_blank" rel="noopener" aria-label="Share on X">X</a><button data-copy-link aria-label="Copy link">⧉</button></div>
            </div>
          </div>
        </div>
      </header>
      <div class="container">
        <figure class="post-cover">{cover_svg(p["seed"], 1600, 600, uid="h")}</figure>
        <div class="post-layout">
          <aside class="toc card"><p class="mono">On this page</p><ol id="toc"></ol><div class="toc__progress mono"><span id="tocLeft">{p["minutes"]} min left</span><div class="meter"><i id="tocBar"></i></div></div></aside>
          <div>
            <details class="toc-mobile card"><summary class="mono">On this page</summary><ol id="tocMobile"></ol></details>
            <div class="prose" data-minutes="{p["minutes"]}" data-spine="Article">{restyle_body(p["body"]())}</div>
            <div class="post-end">
              <div class="author-box card"><img src="{P}assets/img/avatar.png" alt="Manjil Shrestha" width="72" height="72"><div><h3>Written by Manjil Shrestha</h3><p class="muted">Data-driven digital marketer in Melbourne, known online as mastha. I help small teams fix their tracking, then grow with SEO, paid media and CRO.</p><p><a class="link" href="{P}services/">Services</a> · <a class="link" href="{P}book/">Book a free call</a></p></div></div>
              {nav}
            </div>
          </div>
        </div>
      </div>
    </article>
    <section class="section section--tight" data-spine="Keep reading">
      <div class="container">
        {head_block("Keep reading", "More from the *dashboard.*", f'<a class="link" href="{P}blog/">All articles →</a>', row=True)}
        <div class="cards3">{related}</div>
      </div>
    </section>'''
    title = p["title"] + ' | Manjil Shrestha'
    write(path + 'index.html', layout(P, path, title, p["dek"], 'blog', body, scripts=['blog.js'], og_type='article'))

# ============================================================ assets + run
def copy_assets():
    for rel in ['js/content.js', 'js/book.js', 'js/blog.js', 'js/pages.js', 'js/vendor/gsap.min.js', 'js/vendor/ScrollTrigger.min.js', 'js/vendor/lenis.min.js', 'js/vendor/LICENSE-lenis.txt', 'assets/img/portrait.jpg']:
        dst = os.path.join(OUT, rel); os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copyfile(os.path.join(ROOT, rel), dst)
    star = re.search(r'<symbol id="star" viewBox="0 0 100 100"><path fill="currentColor" d="([^"]+)"', SYMBOLS).group(1)
    open(os.path.join(OUT, 'assets/favicon.svg'), 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="18" fill="#170B38"/><g transform="translate(9 9) scale(.46)"><path fill="#B79CFF" d="{star}"/></g></svg>\n')
    print('copied shared js, vendor libs and assets')

if __name__ == '__main__':
    copy_assets()
    home(); services(); seo(); book(); contact(); blog_index()
    for i, p in enumerate(POSTS):
        article(p, i)
    article(TEMPLATE, 0, template=True)
