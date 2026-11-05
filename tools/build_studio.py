"""Builds the "Studio" design (editorial Swiss, red) into /studio/.

Run:  python3 tools/build_studio.py

Content is shared with the main site:
  - home content from js/content.js (read through node)
  - services, SEO, booking, contact and blog content from tools/build_pages.py
Only the design is different. Nothing outside /studio/ is touched.
"""
import html, json, math, os, re, shutil, subprocess

TOOLS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(TOOLS)
OUT = os.path.join(ROOT, 'studio')
SITE = 'https://manjilshrestha.online/'
E = html.escape

# ------------------------------------------------------------------ content
S = json.loads(subprocess.check_output(['node', '-e', "global.window={};require(process.argv[1]);process.stdout.write(JSON.stringify(window.SITE))", os.path.join(ROOT, 'js/content.js')]))
_src = open(os.path.join(TOOLS, 'build_pages.py')).read()
_src = _src[:_src.index("exec(open(SC + 'service_seo.py').read())")]
NS = {'__file__': os.path.join(TOOLS, 'build_pages.py'), '__name__': 'pages_data'}
exec(compile(_src, 'build_pages.py', 'exec'), NS)
SERVICES, POSTS, TEMPLATE, SOON, fmt_date = NS['SERVICES'], NS['POSTS'], NS['TEMPLATE'], NS['SOON'], NS['fmt_date']
SYMBOLS = open(os.path.join(TOOLS, 'symbols.txt')).read()
CLIENTS = ["Northside Dental", "Fitzroy Coffee Co.", "Yarra Home Services", "Kinetic SaaS", "Brunswick Bikes", "Southbank Legal", "Ember Skincare", "Laneway Eats"]  # DEMO

RED, INK, STONE, PAPER = '#F83232', '#0D0D0D', '#E7E4DD', '#F6F5F1'
FONT = "Host Grotesk, Helvetica Neue, Arial, sans-serif"
MONOF = 'font-family="Host Grotesk, sans-serif"'

# ------------------------------------------------------------------ charts
def smooth(p):
    d = f"M{p[0][0]:.1f},{p[0][1]:.1f}"
    for i in range(1, len(p)):
        (x0, y0), (x1, y1) = p[i - 1], p[i]; c = (x0 + x1) / 2
        d += f" C{c:.1f},{y0:.1f} {c:.1f},{y1:.1f} {x1:.1f},{y1:.1f}"
    return d

def scale(s, W, H, px, py):
    mx, mn = max(s), min(s); r = (mx - mn) or 1
    return [(px + i / (len(s) - 1) * (W - 2 * px), H - py - (v - mn) / r * (H - 2 * py)) for i, v in enumerate(s)]

def line_chart(series, W=560, H=240, label=None, cls='chart'):
    p = scale(series, W, H, 6, 18); d = smooth(p); lx, ly = p[-1]
    ticks = ''.join(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{H - 4}" y2="{H}" class="c-tick"/>' for x, _ in p)
    lab = f'<text x="{lx - 10:.0f}" y="{ly - 14:.0f}" text-anchor="end" class="c-lab">{E(label)}</text>' if label else ''
    return (f'<svg class="{cls}" viewBox="0 0 {W} {H}" aria-hidden="true">'
            f'<line x1="0" x2="{W}" y1="{H}" y2="{H}" class="c-base"/>{ticks}<path d="{d}" class="c-line" pathLength="1"/>'
            f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="5" class="c-end"/>{lab}</svg>')

def poster(seed, big, small, variant=0, W=600, H=400):
    """Typographic poster used for case previews and article covers."""
    bg, fg, ln = [(RED, INK, INK), (INK, PAPER, RED), (STONE, INK, RED)][variant % 3]
    rnd = lambda n: (lambda x: x - math.floor(x))(math.sin(seed * 91 + n * 5.7) * 9999)
    s = [8 + i * 1.8 + rnd(i) * 7 for i in range(14)]
    p = [(x, y * .55 + H * .08) for x, y in scale(s, W, H, 0, 40)]
    fs = 210 if len(big) <= 4 else (150 if len(big) <= 6 else 110)
    return (f'<svg viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><rect width="{W}" height="{H}" fill="{bg}"/>'
            f'<path d="{smooth(p)}" fill="none" stroke="{ln}" stroke-width="2.5"/><circle cx="{p[-1][0] - 3:.0f}" cy="{p[-1][1]:.0f}" r="7" fill="{ln}"/>'
            f'<text x="26" y="40" font-family="{FONT}" font-size="15" font-weight="500" fill="{fg}">{E(small)}</text>'
            f'<text x="{W - 26}" y="40" text-anchor="end" font-family="{FONT}" font-size="15" fill="{fg}" opacity=".7">Fig. {seed:02d}</text>'
            f'<text x="20" y="{H - 28}" font-family="{FONT}" font-size="{fs}" font-weight="700" letter-spacing="-8" fill="{fg}">{E(big)}</text></svg>')

def ga4_chart():
    ga = [148, 156, 151, 162, 159, 121, 118, 124, 122, 127]; real = [112, 116, 114, 119, 117, 117, 115, 121, 120, 125]
    bars = ''.join(f'<rect x="{34 + i * 59}" y="{230 - g * 1.1:.0f}" width="20" height="{g * 1.1:.0f}" fill="{RED}"/><rect x="{56 + i * 59}" y="{230 - r * 1.1:.0f}" width="20" height="{r * 1.1:.0f}" fill="{INK}"/>'
                   f'<text x="{42 + i * 59}" y="250" {MONOF} font-size="11" fill="#6E6B66">W{i + 1}</text>' for i, (g, r) in enumerate(zip(ga, real)))
    return f'''<svg viewBox="0 0 640 260" role="img" aria-label="Bar chart: purchases in GA4 compared with real orders, before and after the fixes">
  <text x="20" y="22" {MONOF} font-size="12" font-weight="600" fill="{INK}">Weekly purchases, GA4 vs real orders</text>
  <rect x="452" y="12" width="10" height="10" fill="{RED}"/><text x="468" y="21" {MONOF} font-size="11">GA4</text><rect x="512" y="12" width="10" height="10" fill="{INK}"/><text x="528" y="21" {MONOF} font-size="11">Real orders</text>
  <line x1="20" x2="620" y1="230" y2="230" stroke="{INK}"/>{bars}
  <line x1="330" x2="330" y1="42" y2="236" stroke="{INK}" stroke-dasharray="2 4"/><text x="338" y="54" {MONOF} font-size="11" fill="{INK}">Fixes shipped</text>
</svg>'''

def roas_chart():
    pts = [(0, 0), (5, 20), (10, 34), (15, 43), (20, 48)]
    X = lambda v: 50 + v * 27; Y = lambda v: 220 - v * 3.6
    xy = [(X(a), Y(b)) for a, b in pts]
    dots = ''.join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="4.5" fill="{RED}"/><text x="{x + 9:.0f}" y="{y - 9:.0f}" {MONOF} font-size="12">${b}k</text>' for (x, y), (_, b) in list(zip(xy, pts))[1:])
    ticks = ''.join(f'<text x="{X(a) - 12:.0f}" y="242" {MONOF} font-size="11" fill="#6E6B66">${a}k</text>' for a, _ in pts)
    return f'''<svg viewBox="0 0 640 260" role="img" aria-label="Line chart: revenue flattens as ad spend rises and drops below the breakeven line">
  <text x="20" y="22" {MONOF} font-size="12" font-weight="600">Revenue vs monthly ad spend, breakeven at 2.5x</text>
  <line x1="50" x2="620" y1="220" y2="220" stroke="{INK}"/>
  <path d="M{X(0)},{Y(0)} L{X(20)},{Y(50)}" stroke="#6E6B66" stroke-dasharray="2 4" fill="none"/><text x="{X(14.2):.0f}" y="{Y(40.5):.0f}" {MONOF} font-size="11" fill="#6E6B66">Breakeven</text>
  <path d="{smooth(xy)}" stroke="{INK}" stroke-width="2.5" fill="none"/>{dots}{ticks}
  <text x="{X(13.5):.0f}" y="{Y(54):.0f}" {MONOF} font-size="11" fill="{RED}">The last $10k lost money</text>
</svg>'''

def site_tree():
    return f'''<svg viewBox="0 0 640 230" role="img" aria-label="Site architecture: home links to service pages, which link to suburb pages">
  <g fill="none" stroke="{INK}"><path d="M320 52 V80 M140 80 H500 M140 80 V100 M320 80 V100 M500 80 V100"/><path d="M140 136 V160 M80 160 H200 M80 160 V176 M140 160 V176 M200 160 V176"/><path d="M320 136 V160 M260 160 H380 M260 160 V176 M320 160 V176 M380 160 V176"/></g>
  <g {MONOF} font-size="12">
    <rect x="260" y="20" width="120" height="32" fill="{RED}"/><text x="302" y="41" fill="{INK}" font-weight="600">Home</text>
    <g fill="#fff" stroke="{INK}"><rect x="80" y="100" width="120" height="36"/><rect x="260" y="100" width="120" height="36"/><rect x="440" y="100" width="120" height="36"/></g>
    <g fill="{INK}" font-size="11"><text x="96" y="123">/plumbing/</text><text x="276" y="123">/hot-water/</text><text x="447" y="123">/blocked-drains/</text></g>
    <g fill="{STONE}"><rect x="46" y="176" width="68" height="30"/><rect x="118" y="176" width="44" height="30"/><rect x="166" y="176" width="68" height="30"/><rect x="226" y="176" width="68" height="30"/><rect x="298" y="176" width="44" height="30"/><rect x="346" y="176" width="68" height="30"/></g>
    <g fill="{INK}" font-size="11"><text x="54" y="196">fitzroy</text><text x="124" y="196">kew</text><text x="172" y="196">carlton</text><text x="232" y="196">fitzroy</text><text x="304" y="196">kew</text><text x="352" y="196">carlton</text></g>
    <text x="440" y="192" fill="#6E6B66">One page per suburb</text><text x="440" y="208" fill="#6E6B66">you actually serve</text>
  </g>
</svg>'''

NS.update(ga4_chart=ga4_chart, roas_chart=roas_chart, site_tree=site_tree)

# ------------------------------------------------------------------ helpers
ARR = '<span class="arr" aria-hidden="true">→</span>'
NE = '<span class="arr" aria-hidden="true">↗</span>'

def kfmt(k):
    v = k["value"]; d = k.get("decimals", 0)
    return ('+' if v > 0 and k.get("suffix") == '%' else '') + f'{v:.{d}f}' + k.get('suffix', '')

def sec_head(no, label, title, aside=''):
    return (f'<header class="sh"><p class="sh__no">({no:02d})</p><p class="sh__label">{label}</p>'
            f'<h2 class="sh__title rv">{title}</h2>{f"<div class=sh__aside>{aside}</div>" if aside else ""}</header>')

def faq(items, uid='q'):
    return '<div class="faq__list">' + ''.join(
        f'<div class="faq__item"><button class="faq__q" aria-expanded="false" aria-controls="{uid}{i}"><span class="faq__n">{i + 1:02d}</span><span>{E(q)}</span><i aria-hidden="true"></i></button>'
        f'<div class="faq__a" id="{uid}{i}" role="region"><div><p>{E(a)}</p></div></div></div>' for i, (q, a) in enumerate(items)) + '</div>'

def faq_ld(items):
    return json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}, ensure_ascii=False)

def crumbs(P, trail):
    out = []
    for i, (n, p) in enumerate(trail):
        out.append(f'<span aria-current="page">{E(n)}</span>' if i == len(trail) - 1 else f'<a href="{P}{p}">{E(n)}</a><span aria-hidden="true">/</span>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + ''.join(out) + '</nav>'

def phero(P, trail, meta, title, lead, actions='', aside=''):
    meta_html = ''.join(f'<li>{m}</li>' for m in meta)
    return f'''    <section class="ph" id="top">
      <div class="wrap">
        {crumbs(P, trail)}
        <div class="ph__grid">
          <ul class="ph__meta">{meta_html}</ul>
          <div class="ph__main">
            <h1 class="ph__title"><span class="ln"><span>{title}</span></span></h1>
            <p class="ph__lead in">{lead}</p>
            {f'<div class="actions in">{actions}</div>' if actions else ''}
          </div>
          {f'<div class="ph__aside in">{aside}</div>' if aside else ''}
        </div>
      </div>
    </section>'''

def cta(P, line='Have a number you want to move?', sub='A free 30-minute call with your real data. You will leave with the three things I would do first.'):
    return f'''    <section class="cta">
      <div class="wrap cta__grid">
        <p class="cta__line">{line}</p>
        <div class="cta__side"><p>{sub}</p><a class="btn btn--ink" href="{P}book/">Book a free consultation {ARR}</a></div>
      </div>
    </section>'''

def write(rel, text):
    full = os.path.join(OUT, rel); os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w').write(text); print('wrote studio/' + rel)

# ------------------------------------------------------------------ layout
NAV = [('Work', '#work', 'work'), ('Services', 'services/', 'services'), ('Journal', 'blog/', 'blog'), ('Contact', 'contact/', 'contact')]

def layout(P, path, title, desc, active, body, scripts=(), ld=()):
    nav = ''.join(f'<a href="{P}{h}"{" aria-current=page" if k == active else ""}>{n}</a>' for n, h, k in NAV)
    menu = ''.join(f'<a href="{P}{h}"><span>{i + 1:02d}</span>{n}</a>' for i, (n, h, k) in enumerate([('Home', '', ''), *NAV, ('Book a call', 'book/', '')]))
    lds = ''.join(f'\n  <script type="application/ld+json">{x}</script>' for x in ld)
    scr = ''.join(f'\n  <script src="{P}js/{s}"></script>' for s in scripts)
    return f'''<!DOCTYPE html>
<html lang="en-AU">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{E(title)}</title>
  <meta name="description" content="{E(desc)}">
  <meta name="robots" content="noindex, follow">
  <meta name="theme-color" content="#F6F5F1">
  <link rel="canonical" href="{SITE}{path}">
  <link rel="icon" type="image/svg+xml" href="{P}assets/favicon.svg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Host+Grotesk:ital,wght@0,300..800;1,300..800&family=Newsreader:ital,opsz,wght@0,6..72,300..600;1,6..72,300..500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{P}css/studio.css">{lds}
</head>
<body class="no-js">
  <script>document.body.classList.replace('no-js','js');</script>
  <svg width="0" height="0" style="position:absolute" aria-hidden="true">{SYMBOLS}</svg>
  <a class="skip" href="#main">Skip to content</a>
  <div class="gridlines" aria-hidden="true"><div class="wrap"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div></div>
  <div class="preview" id="preview" aria-hidden="true"></div>
  <div class="toast" id="toast" role="status" aria-live="polite"></div>

  <header class="hd" id="nav">
    <div class="wrap hd__in">
      <a class="hd__brand" href="{P}" aria-label="Manjil Shrestha, home"><svg viewBox="0 0 1463 317"><use href="#logo"/></svg></a>
      <p class="hd__role">Digital marketing<br>Melbourne, AU</p>
      <nav class="hd__nav" aria-label="Primary">{nav}</nav>
      <p class="hd__time"><span data-mel-clock>--:--</span> AEDT<br><span class="avail"><i></i>Available for work</span></p>
      <a class="hd__cta" href="{P}book/">Book a call {ARR}</a>
      <button class="hd__menu" id="burger" aria-label="Open menu" aria-expanded="false" aria-controls="menu">Menu</button>
    </div>
  </header>
  <div class="menu" id="menu" aria-hidden="true">
    <div class="wrap menu__in"><nav class="menu__links">{menu}</nav><div class="menu__foot"><a href="#" data-copy-email data-email-text>hello@</a><div data-socials class="menu__soc"></div></div></div>
  </div>

  <main id="main">
{body}
  </main>

  <footer class="ft">
    <div class="wrap">
      <div class="ft__grid">
        <div class="ft__col ft__col--lead"><p class="ft__big">Manjil Shrestha is an independent digital marketer in Melbourne. SEO, paid media, analytics and CRO, judged on revenue.</p></div>
        <div class="ft__col"><h4>Site</h4><a href="{P}">Home</a><a href="{P}services/">Services</a><a href="{P}services/seo/">SEO in Melbourne</a><a href="{P}blog/">Journal</a></div>
        <div class="ft__col"><h4>Contact</h4><a href="#" data-copy-email data-email-text>hello@</a><a href="{P}book/">Book a call</a><a href="{P}contact/">Contact page</a></div>
        <div class="ft__col"><h4>Elsewhere</h4><div data-socials class="ft__soc"></div></div>
      </div>
      <p class="ft__name" data-fit>Manjil Shrestha</p>
      <div class="ft__bar"><span>© <span data-year>2026</span></span><span>Set in Host Grotesk &amp; Newsreader</span><button type="button" class="ft__grid-toggle" id="gridToggle">Show grid (G)</button><a href="#top">Back to top ↑</a></div>
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

# ------------------------------------------------------------------ shared blocks
def contact_form(subject):
    needs = ''.join(f'<label><input type="checkbox" name="needs" value="{v}"><span>{v}</span></label>' for v in ["SEO", "Paid media", "Analytics", "CRO", "Email", "Full-time role"])
    return f'''<form class="form js-form" data-subject="{subject}" action="https://formspree.io/f/YOUR_FORM_ID" method="POST" novalidate>
          <label class="field"><span>Your name</span><input name="name" required autocomplete="name"></label>
          <label class="field"><span>Email</span><input type="email" name="email" required autocomplete="email"></label>
          <fieldset class="chips"><legend>Interested in</legend>{needs}</fieldset>
          <label class="field"><span>Monthly budget</span><select name="budget"><option value="">Not sure yet</option><option>Under $2k</option><option>$2k to $5k</option><option>$5k to $15k</option><option>$15k+</option></select></label>
          <label class="field"><span>What are you trying to grow?</span><textarea name="message" rows="3" required></textarea></label>
          <input type="text" name="_gotcha" tabindex="-1" autocomplete="off" class="hp" aria-hidden="true">
          <div class="form__foot"><button type="submit" class="btn btn--ink"><span class="btn__text">Send enquiry {ARR}</span><span class="btn__sent">Sent. Talk soon.</span></button><p class="small" data-form-note>Reply within one business day.</p></div>
        </form>'''

def journal_rows(P, posts, soon=()):
    rows = []
    for i, p in enumerate(posts):
        big = {'analytics': 'GA4', 'local-seo': 'SEO', 'paid-media': 'ROAS'}.get(p['tagkey'], p['tag'][:4])
        rows.append(f'''<li class="jr" data-post data-tags="{p["tagkey"]}" data-text="{E((p["title"] + " " + p["dek"] + " " + p["tag"]).lower())}">
            <a href="{P}blog/{p["slug"]}/" data-preview>
              <span class="jr__date">{fmt_date(p["date"])}</span><span class="jr__title">{E(p["title"])}</span><span class="jr__tag">{E(p["tag"])}</span><span class="jr__min">{p["minutes"]} min {ARR}</span>
              <template>{poster(p["seed"], big, p["tag"], i)}</template>
            </a></li>''')
    for s in soon:
        rows.append(f'<li class="jr jr--soon" data-post data-tags="{s["tagkey"]}" data-text="{E((s["title"] + " " + s["dek"]).lower())}"><div><span class="jr__date">In progress</span><span class="jr__title">{E(s["title"])}</span><span class="jr__tag">{E(s["tag"])}</span><span class="jr__min">Soon</span></div></li>')
    return '<ol class="journal">' + ''.join(rows) + '</ol>'

# ================================================================== HOME
def home():
    P = ''
    cases = S['caseStudies']
    figs = ''.join(f'<div class="fig rv"><p class="fig__v"><span data-count="{n["value"]}" data-decimals="{n.get("decimals", 0)}">0</span>{E(n.get("suffix", ""))}</p><p class="fig__l">{E(n["label"])}</p></div>' for n in S['numbers'])
    work = ''.join(f'''<li class="wk">
            <button class="wk__head" aria-expanded="false" aria-controls="wk{i}" data-preview>
              <span class="wk__no">{i + 1:02d}</span><span class="wk__title">{E(c["title"])}</span><span class="wk__sector">{E(c["industry"])}</span><span class="wk__disc">{E(", ".join(c["services"]))}</span><span class="wk__year">{E(c["year"])}</span><span class="wk__res">{kfmt(c["kpis"][0])} {E(c["kpis"][0]["label"])}</span><i class="wk__plus" aria-hidden="true"></i>
              <template>{poster(i + 1, kfmt(c["kpis"][0]), c["client"], i)}</template>
            </button>
            <div class="wk__body" id="wk{i}" role="region"><div><div class="wk__detail">
              <p class="wk__client">{E(c["client"])}</p>
              <div class="wk__text"><h3>The problem</h3><p>{E(c["problem"])}</p><h3>What I did</h3><p>{E(c["approach"])}</p><h3>The result</h3><p>{E(c["result"])}</p></div>
              <div class="wk__data">{line_chart(c["series"], 520, 220, kfmt(c["kpis"][0]))}<dl class="kpis">{"".join(f"<div><dt>{E(k['label'])}</dt><dd>{kfmt(k)}</dd></div>" for k in c["kpis"])}</dl></div>
            </div></div></div>
          </li>''' for i, c in enumerate(cases))
    groups = [("Acquisition", ["seo", "paid"]), ("Conversion", ["cro", "email"]), ("Measurement & strategy", ["analytics", "strategy"])]
    by = {s['id']: s for s in SERVICES}
    caps = ''.join(f'<div class="cap rv"><h3>{g}</h3><ul>' + ''.join(f'<li><a href="services/#{k}"><span class="cap__t">{E(by[k]["title"])}</span><span class="cap__d">{E(by[k]["short"])}</span>{ARR}</a></li>' for k in ks) + '</ul></div>' for g, ks in groups)
    steps = ''.join(f'<li class="step rv"><span class="step__n">{i + 1:02d}</span><h3>{E(p["title"])}</h3><p>{E(p["text"])}</p></li>' for i, p in enumerate(S['process']))
    tools = ', '.join(E(t) for row in S['stack'] for t in row)
    cv = ''.join(f'<li class="cv__row rv"><span class="cv__yr">{E(e["period"])}</span><span class="cv__role">{E(e["role"])}</span><span class="cv__org">{E(e["org"])}</span><span class="cv__txt">{E(e["text"])}</span></li>' for e in S['experience'])
    edu = ''.join(f'<li><span>{E(e["period"])}</span>{E(e["title"])}, {E(e["org"])}</li>' for e in S['education'])
    certs = ''.join(f'<li>{E(c)}</li>' for c in S['certifications'])
    quotes = ''.join(f'<figure class="qt__item{" is-on" if i == 0 else ""}"><blockquote>{E(t["quote"])}</blockquote><figcaption>{E(t["name"])}, {E(t["org"])} <span>(demo)</span></figcaption></figure>' for i, t in enumerate(S['testimonials']))
    clients = ''.join(f'<li>{E(c)}</li>' for c in CLIENTS)
    statement = re.sub(r'\[(.+?)\]', r'<em>\1</em>', E(S['manifesto']))
    fq = [(f['q'], f['a']) for f in S['faq']]
    calc = S['calculator']
    body = f'''    <section class="hero" id="top">
      <div class="wrap hero__grid">
        <ul class="hero__meta in">
          <li><span>Practice</span>Independent digital marketing</li>
          <li><span>Based</span>Melbourne, Australia</li>
          <li><span>Since</span>2020</li>
          <li><span>Focus</span>SEO, paid media, analytics, CRO</li>
        </ul>
        <div class="hero__main">
          <h1 class="hero__h1"><span class="ln"><span>Digital marketing</span></span><span class="ln"><span>expert in Melbourne<b>.</b></span></span></h1>
          <p class="hero__lead in">I help ambitious Melbourne businesses grow with search, paid media and analytics, and I report on one thing: revenue. No vanity metrics, no black boxes.</p>
          <div class="actions in"><a class="btn btn--red" href="book/">Book a free consultation {ARR}</a><a class="tlink" href="#work">Selected work</a></div>
        </div>
        <figure class="hero__img in">
          <img src="assets/img/portrait.jpg" alt="Portrait of Manjil Shrestha" width="1000" height="1371">
          <figcaption><span>Manjil Shrestha</span><span>Melbourne, 2026</span></figcaption>
        </figure>
      </div>
      <div class="wrap"><p class="bigname" data-fit aria-hidden="true">Manjil Shrestha</p></div>
    </section>

    <section class="sec sec--tight clients" aria-label="Clients (demo)">
      <div class="wrap clients__grid"><p class="clients__label">Clients and collaborators (demo)</p><ul class="clients__list">{clients}</ul></div>
    </section>

    <section class="sec" id="about">
      <div class="wrap">
        {sec_head(1, "About", "A marketer who reads the numbers before the headlines.")}
        <div class="about">
          <p class="statement rv">{statement}</p>
          <div class="about__side rv"><p>I started in content and kept asking one question: what did it actually do? Today I build the tracking, campaigns and experiments that answer it. I work with founders and small teams as an independent consultant, and I am open to the right in-house role.</p><a class="tlink" href="contact/">Get in touch</a></div>
        </div>
        <div class="figs">{figs}</div>
      </div>
    </section>

    <section class="sec" id="work">
      <div class="wrap">
        {sec_head(2, "Selected work", "Four engagements where the numbers moved.", '<p>Demo case studies. Open a row for the full story.</p>')}
        <div class="wk__cols" aria-hidden="true"><span>No.</span><span>Project</span><span>Sector</span><span>Discipline</span><span>Year</span><span>Outcome</span></div>
        <ol class="work">{work}</ol>
      </div>
    </section>

    <section class="sec sec--stone" id="services">
      <div class="wrap">
        {sec_head(3, "Capabilities", "Six disciplines, one rule: if it can't be measured, it doesn't get budget.", f'<a class="tlink" href="services/">Services and pricing</a>')}
        <div class="caps">{caps}</div>
      </div>
    </section>

    <section class="sec" id="approach">
      <div class="wrap">
        {sec_head(4, "Approach", "A loop, not a launch.")}
        <ol class="steps">{steps}</ol>
        <p class="toolsline rv"><b>Tools</b><span>{tools}.</span></p>
      </div>
    </section>

    <section class="sec sec--ink" id="lab">
      <div class="wrap">
        {sec_head(5, "Growth model", "What would a better funnel be worth to you?", '<p>The same back-of-envelope maths I run before every CRO engagement. Illustrative only.</p>')}
        <div class="lab">
          <div class="lab__in">
            <label class="rg"><span>Monthly visitors</span><output id="oV"></output><input type="range" id="iV" min="1000" max="200000" step="1000" value="{calc["visitors"]}"></label>
            <label class="rg"><span>Conversion rate</span><output id="oC"></output><input type="range" id="iC" min="0.2" max="10" step="0.1" value="{calc["conversion"]}"></label>
            <label class="rg"><span>Average order or lead value</span><output id="oA"></output><input type="range" id="iA" min="10" max="2000" step="10" value="{calc["value"]}"></label>
            <label class="rg"><span>Expected conversion lift</span><output id="oL"></output><input type="range" id="iL" min="5" max="100" step="5" value="{calc["lift"]}"></label>
          </div>
          <div class="lab__out">
            <p class="lab__k">Extra revenue, first 12 months</p>
            <p class="lab__v" id="rY">$0</p>
            <svg id="labSvg" viewBox="0 0 520 160" preserveAspectRatio="none" aria-hidden="true"></svg>
            <p class="lab__note" id="rM"></p>
            <a class="btn btn--red" href="book/">Make it real {ARR}</a>
          </div>
        </div>
      </div>
    </section>

    <section class="sec" id="experience">
      <div class="wrap">
        {sec_head(6, "Experience", "Where the data habit came from.", '<a class="tlink" href="assets/Manjil-Shrestha-CV.pdf">Download CV</a>')}
        <ol class="cv">{cv}</ol>
        <div class="cv__extra rv"><div><h3>Education</h3><ul>{edu}</ul></div><div><h3>Certifications</h3><ul>{certs}</ul></div></div>
      </div>
    </section>

    <section class="sec sec--tight qt" aria-label="Testimonials">
      <div class="wrap qt__grid">
        <p class="sh__no">(07)</p>
        <div class="qt__stage">{quotes}</div>
        <div class="qt__nav"><button type="button" id="qPrev" aria-label="Previous quote">←</button><span id="qCount">1 / {len(S["testimonials"])}</span><button type="button" id="qNext" aria-label="Next quote">→</button></div>
      </div>
    </section>

    <section class="sec" id="journal">
      <div class="wrap">
        {sec_head(8, "Journal", "Notes from the dashboard.", '<a class="tlink" href="blog/">All articles</a>')}
        {journal_rows(P, POSTS)}
      </div>
    </section>

    <section class="sec" id="faq">
      <div class="wrap faq">
        {sec_head(9, "FAQ", "Before we start.")}
        {faq(fq)}
      </div>
    </section>

    <section class="contact" id="contact">
      <div class="wrap">
        <p class="contact__big"><span class="ln"><span>Let's talk.</span></span></p>
        <div class="contact__grid">
          <div class="contact__info">
            <p>Tell me what you are trying to grow. I reply within one business day with an honest take on whether I can help.</p>
            <button type="button" class="contact__email" data-copy-email><span data-email-text>hello@</span><small>Copy</small></button>
            <dl class="contact__dl"><div><dt>Based</dt><dd>Melbourne, Australia</dd></div><div><dt>Status</dt><dd data-availability>Available</dd></div><div><dt>Elsewhere</dt><dd data-socials class="contact__soc"></dd></div></dl>
          </div>
          {contact_form("Project enquiry")}
        </div>
      </div>
    </section>'''
    person = json.dumps({"@context": "https://schema.org", "@type": "Person", "name": "Manjil Shrestha", "jobTitle": "Digital Marketing Expert", "address": {"@type": "PostalAddress", "addressLocality": "Melbourne", "addressCountry": "AU"}, "url": SITE}, ensure_ascii=False)
    write('index.html', layout(P, '', 'Digital Marketing Expert in Melbourne | Manjil Shrestha', 'Manjil Shrestha is an independent, data-driven digital marketing expert in Melbourne. SEO, paid media, analytics and CRO, judged on revenue.', 'home', body, ['home.js'], [person, faq_ld(fq)]))

# ================================================================== SERVICES
SVC_FAQ = NS.get('SVC_FAQ') or [
    ("Do you lock clients into long contracts?", "No. Audits and sprints are fixed-scope. Retainers run month to month after the first 90 days, because that is how long it takes to see a real trend."),
    ("Is ad spend included in the price?", "No. Ad spend is paid directly to Google, Meta or LinkedIn from your own account, so you always own the account and the data."),
    ("Can you work alongside my current agency or team?", "Yes. I often handle analytics, strategy or CRO while an agency or in-house team runs execution, and I write briefs they can act on."),
    ("What do you need from me to start?", "Access to your analytics and ad accounts, your revenue or lead numbers for the last 12 months, and one person who can make decisions."),
    ("How and when do you report?", "A short written update every week and a Looker Studio dashboard you can open any time. Monthly, we review results against the targets we agreed."),
]
PLANS = [
    ("Growth Audit", "$1,500", "One-off, 2 weeks", "A clear, honest picture first.", ["Analytics and tracking audit", "Channel-by-channel review", "Funnel and landing page review", "Prioritised 90-day roadmap", "60-minute walkthrough"], False),
    ("90-Day Growth Sprint", "$4,500", "Per month, 3 months", "Move one or two numbers, fast.", ["Everything in the audit", "Tracking fixed, dashboard built", "Execution in one or two channels", "Weekly tests and optimisation", "Weekly update, monthly review"], True),
    ("Fractional CMO", "$3,000", "Per month, ongoing", "Senior marketing leadership.", ["Quarterly growth plan and budget", "Agency and freelancer management", "Hiring support and briefs", "Weekly team check-in", "Monthly board-ready report"], False),
]

def plans_html(P, plans):
    return '<div class="plans">' + ''.join(f'''<article class="plan{" plan--hot" if hot else ""} rv">
          <header><h3>{E(n)}</h3>{'<span class="plan__tag">Most chosen</span>' if hot else ''}</header>
          <p class="plan__price">{E(pr)}</p><p class="plan__unit">{E(u)}</p><p class="plan__for">{E(f)}</p>
          <ul>{"".join(f"<li>{E(x)}</li>" for x in items)}</ul>
          <a class="{"btn btn--red" if hot else "tlink"}" href="{P}book/">{"Start with a call " + ARR if hot else "Start with a call"}</a>
        </article>''' for n, pr, u, f, items, hot in plans) + '</div>'

def services():
    P = '../'
    jump = ''.join(f'<a href="#{s["id"]}"><span>{i + 1:02d}</span>{E(s["title"])}</a>' for i, s in enumerate(SERVICES))
    items = ''.join(f'''<article class="sv rv" id="{s["id"]}">
          <div class="sv__a"><p class="sv__no">{i + 1:02d}</p><h2>{E(s["title"])}</h2><p class="sv__short">{E(s["short"])}</p>
            <dl class="sv__facts"><div><dt>First results</dt><dd>{E(s["first"])}</dd></div><div><dt>Investment</dt><dd>{E(s["price"])}</dd></div></dl>
            {f'<a class="tlink" href="seo/">SEO in depth</a>' if s["id"] == "seo" else ''}</div>
          <div class="sv__b"><h3>What it is</h3><p>{E(s["what"])}</p><h3>Who it's for</h3><p>{E(s["who"])}</p></div>
          <div class="sv__c"><h3>What you get</h3><ul class="ticks">{"".join(f"<li>{E(d)}</li>" for d in s["deliver"])}</ul><h3>Measured by</h3><p class="sv__kpis">{", ".join(E(k) for k in s["kpis"])}</p></div>
        </article>''' for i, s in enumerate(SERVICES))
    rows = [("Tracking and analytics audit", "Yes", "Yes", "Yes"), ("Prioritised roadmap", "Yes", "Yes", "Yes"), ("Hands-on execution", "No", "One or two channels", "Through your team"), ("Weekly reporting", "No", "Yes", "Yes"), ("Agency and hiring management", "No", "No", "Yes"), ("Commitment", "2 weeks", "3 months", "Month to month")]
    table = ''.join(f'<tr><th scope="row">{E(r[0])}</th>' + ''.join(f'<td>{E(c)}</td>' for c in r[1:]) + '</tr>' for r in rows)
    steps = ''.join(f'<li class="step rv"><span class="step__n">{i + 1:02d}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate([("Diagnose", "Audit data, funnel and market. Find where revenue leaks."), ("Strategy", "Agree targets and the channels that can hit them."), ("Build", "Tracking, campaigns, pages and flows, instrumented."), ("Measure", "Weekly reporting in a dashboard you own."), ("Scale", "Double down on what the data proves.")]))
    body = phero(P, [("Home", ""), ("Services", "services/")], ["<span>Services</span>Six disciplines", "<span>Where</span>Melbourne and remote", "<span>Terms</span>No lock-in"],
                 "Marketing that pays for itself.", "Pick the one service you need, or let me build the right mix for your stage and budget. Every engagement is measured against revenue.",
                 f'<a class="btn btn--red" href="{P}book/">Book a free consultation {ARR}</a><a class="tlink" href="#pricing">Packages and pricing</a>') + f'''

    <section class="sec sec--tight">
      <div class="wrap">
        <nav class="jump rv" aria-label="Services on this page">{jump}</nav>
        <div class="svs">{items}</div>
      </div>
    </section>

    <section class="sec sec--stone" id="pricing">
      <div class="wrap">
        {sec_head(1, "Packages", "Three ways to work together.", '<p>Demo pricing in AUD, excluding GST. Final scope confirmed after a free call.</p>')}
        {plans_html(P, PLANS)}
        <div class="tablewrap rv"><table class="cmp"><thead><tr><th></th><th>Audit</th><th>Sprint</th><th>Fractional CMO</th></tr></thead><tbody>{table}</tbody></table></div>
      </div>
    </section>

    <section class="sec">
      <div class="wrap">
        {sec_head(2, "How it works", "A loop, not a launch.")}
        <ol class="steps">{steps}</ol>
      </div>
    </section>

    <section class="sec">
      <div class="wrap faq">
        {sec_head(3, "Questions", "Before you ask.")}
        {faq(SVC_FAQ)}
      </div>
    </section>
{cta(P, "Not sure which service fits?")}'''
    write('services/index.html', layout(P, 'services/', 'Digital Marketing Services in Melbourne | Manjil Shrestha', 'SEO, paid media, analytics, CRO, email and fractional CMO services from an independent digital marketing expert in Melbourne.', 'services', body, ['pages.js'], [faq_ld(SVC_FAQ)]))

# ================================================================== SEO
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
    serp = f'''<div class="serp" id="serp">
            <p class="serp__q"><span>Search</span>emergency plumber fitzroy</p>
            <ol class="serp__list">
              <li class="serp__you"><b class="serp__rank" id="serpRank">9</b><div><small>yourbusiness.com.au › fitzroy</small><strong>Emergency Plumber Fitzroy, 24/7 callouts</strong></div></li>
              <li><b>2</b><div><small>competitor-one.com.au</small><strong>Plumbers Melbourne, call today</strong></div></li>
              <li><b>3</b><div><small>directory-site.com.au</small><strong>Top 10 plumbers in Fitzroy</strong></div></li>
            </ol>
            <p class="serp__foot"><span id="serpNote">Month 0</span><span>Illustrative</span></p>
          </div>'''
    incl = [("Technical SEO", "Speed, Core Web Vitals, crawlability, indexing, schema and site structure, fixed first."), ("Keyword strategy", "A keyword map built from real Melbourne demand, matched to pages that can win."), ("Local SEO", "Google Business Profile, suburb pages, reviews and local citations for the map pack."),
            ("On-page and content", "Service pages and articles that answer real questions, written to rank and convert."), ("Links and local PR", "Earned mentions from Melbourne publications and partners. No link farms."), ("Tracking and reporting", "Organic enquiries and revenue tracked in GA4, with a live dashboard.")]
    incl_html = ''.join(f'<li class="rv"><span>{i + 1:02d}</span><h3>{E(t)}</h3><p>{E(d)}</p></li>' for i, (t, d) in enumerate(incl))
    road = [("Month 1", "Audit and fix", "Technical audit, GA4 tracking, critical fixes shipped."), ("Month 2", "Architecture", "Keyword map, service pages rebuilt, first suburb pages."), ("Month 3", "Local and content", "Business Profile optimised, review engine, content cadence."), ("Months 4 to 6", "Compound", "More suburbs and topics, local PR, double down on winners.")]
    road_html = ''.join(f'<li class="rv"><span class="rd__when">{w}</span><h3>{t}</h3><p>{d}</p></li>' for w, t, d in road)
    checks = ''.join(f'<li><label><input type="checkbox" class="qc"><span>{E(c)}</span></label></li>' for c in SEO_CHECKS)
    seo_plans = [("SEO Audit", "$1,500", "One-off", "A full diagnosis and a prioritised fix list.", ["Technical and on-page audit", "Keyword and competitor gaps", "Local SEO and Business Profile review", "Prioritised 90-day plan", "60-minute walkthrough"], False),
                 ("Local SEO", "$1,800", "Per month", "For service businesses winning in their suburbs.", ["Everything in the audit", "Up to 5 suburb or service pages a month", "Business Profile management and reviews", "Local citations and PR", "Monthly report and live dashboard"], True),
                 ("Growth SEO", "$3,200", "Per month", "For eCommerce and multi-location brands.", ["Everything in Local SEO", "Category and product page SEO", "4 long-form articles a month", "Digital PR outreach", "Fortnightly strategy call"], False)]
    body = phero(P, [("Home", ""), ("Services", "services/"), ("SEO", "services/seo/")], ["<span>Service</span>Search and SEO", "<span>Results</span>3 to 6 months", "<span>From</span>$1,800 a month"],
                 "SEO services in Melbourne.", "Rank for what your customers actually search, suburb by suburb. Technical fixes, local SEO, content and the tracking that ties every ranking to a real enquiry.",
                 f'<a class="btn btn--red" href="{P}book/">Get a free SEO audit call {ARR}</a><a class="tlink" href="#pricing">SEO pricing</a>', serp) + f'''

    <section class="sec">
      <div class="wrap">
        {sec_head(1, "The problem", "You are paying for every click because Google can't find you.")}
        <ol class="pains"><li class="rv"><span>a.</span><p><strong>Invisible in your own suburbs.</strong> Competitors with worse reviews show up first in the map pack.</p></li><li class="rv"><span>b.</span><p><strong>Ads do all the work.</strong> Turn them off and the phone stops ringing.</p></li><li class="rv"><span>c.</span><p><strong>Traffic, but no enquiries.</strong> Ranking reports nobody could connect to revenue.</p></li></ol>
      </div>
    </section>

    <section class="sec sec--stone">
      <div class="wrap">
        {sec_head(2, "What's included", "Six parts, one system.", '<p>Every engagement covers all six, weighted to where your biggest gaps are.</p>')}
        <ol class="incl">{incl_html}</ol>
      </div>
    </section>

    <section class="sec">
      <div class="wrap">
        {sec_head(3, "Roadmap", "Your first six months.")}
        <ol class="road">{road_html}</ol>
      </div>
    </section>

    <section class="sec sec--ink">
      <div class="wrap">
        {sec_head(4, "Health check", "How healthy is your SEO?", '<p>Tick what is true. Thirty seconds, no email required.</p>')}
        <div class="qcx">
          <ul class="qcx__list">{checks}</ul>
          <div class="qcx__score" aria-live="polite"><p class="lab__k">Your score</p><p class="qcx__num"><span id="qcNum">0</span>/{len(SEO_CHECKS)}</p><div class="meter"><i id="qcBar"></i></div><h3 id="qcTitle">Start ticking</h3><p id="qcText">Your result and the first thing to fix appear here.</p><a class="btn btn--red" href="{P}book/">Book a free SEO audit call {ARR}</a></div>
        </div>
      </div>
    </section>

    <section class="sec">
      <div class="wrap">
        {sec_head(5, "Case study", "Owning local search across 60+ Melbourne suburbs.", '<p>Home services, 12 months. Demo.</p>')}
        <div class="casex rv"><div class="casex__chart">{line_chart([4, 5, 5, 7, 9, 12, 15, 17, 21, 24, 27, 31], 720, 280, "+212%")}</div>
          <dl class="kpis kpis--row"><div><dt>Organic enquiries</dt><dd>+212%</dd></div><div><dt>Top-3 keywords</dt><dd>63</dd></div><div><dt>Blended cost per lead</dt><dd>-33%</dd></div><div><dt>Programme</dt><dd>12 mo</dd></div></dl></div>
      </div>
    </section>

    <section class="sec sec--stone" id="pricing">
      <div class="wrap">
        {sec_head(6, "SEO pricing", "Clear prices, no lock-in.", '<p>Demo pricing in AUD, excluding GST.</p>')}
        {plans_html(P, seo_plans)}
      </div>
    </section>

    <section class="sec">
      <div class="wrap faq">
        {sec_head(7, "SEO questions", "Straight answers.")}
        {faq(SEO_FAQ)}
      </div>
    </section>
{cta(P, "Find out what's stopping you ranking.", "Free 30-minute SEO audit call. I will look at your site and Business Profile live and tell you the three things I would fix first.")}'''
    write('services/seo/index.html', layout(P, 'services/seo/', 'SEO Services in Melbourne | Manjil Shrestha', 'SEO services in Melbourne: technical SEO, local SEO, content and tracking that turns rankings into enquiries.', 'services', body, ['pages.js'], [faq_ld(SEO_FAQ)]))

# ================================================================== BOOK
BOOK_FAQ = [("Is the consultation really free?", "Yes. No card, no invoice afterwards, no obligation."), ("What happens in the call?", "We look at your goals and numbers, I point out the two or three biggest opportunities, and you leave with next steps."), ("Can I reschedule?", "Of course. Reply to the confirmation email with a better time."), ("Will you sign an NDA?", "Happy to. Send it before the call.")]

def book():
    P = '../'
    body = phero(P, [("Home", ""), ("Book a call", "book/")], ["<span>Length</span>30 minutes", "<span>Format</span>Video call", "<span>Cost</span>Free"],
                 "Book a free consultation.", "Your numbers, my honest take. No pitch deck and no obligation. You will leave with the two or three moves I would make first.") + f'''

    <section class="sec sec--tight" style="padding-top:0">
      <div class="wrap book">
        <div class="booker" id="booker">
          <ol class="stepper"><li class="is-on"><b>1</b><span>Pick a time</span></li><li><b>2</b><span>Your details</span></li><li><b>3</b><span>Confirmed</span></li></ol>
          <div class="panel-step is-on" data-step="1">
            <div class="picker">
              <div class="cal">
                <div class="cal__head"><h3 id="calMonth">Month</h3><div class="cal__nav"><button type="button" id="calPrev" aria-label="Previous month">←</button><button type="button" id="calNext" aria-label="Next month">→</button></div></div>
                <div class="cal__dow"><span>M</span><span>T</span><span>W</span><span>T</span><span>F</span><span>S</span><span>S</span></div>
                <div class="cal__days" id="calDays"></div>
              </div>
              <div class="slots"><h4 id="slotsDay">Day</h4><p class="slots__tz" id="slotsTz"></p><div class="slots__list" id="slotsList"></div></div>
            </div>
          </div>
          <div class="panel-step" data-step="2">
            <form class="form form--book" id="bookForm" action="https://formspree.io/f/YOUR_FORM_ID" method="POST" novalidate>
              <div class="picked"><span id="pickedText"></span><button type="button" data-back>Change</button></div>
              <input type="hidden" name="slot" id="bfSlot">
              <label class="field"><span>Your name</span><input name="name" required autocomplete="name"></label>
              <label class="field"><span>Email</span><input type="email" name="email" required autocomplete="email"></label>
              <label class="field"><span>Website</span><input name="website"></label>
              <label class="field"><span>Main focus</span><select name="focus"><option value="">Not sure yet</option><option>SEO</option><option>Paid media</option><option>Analytics and tracking</option><option>Conversion (CRO)</option><option>Email and lifecycle</option><option>Overall strategy</option><option>Full-time role</option></select></label>
              <label class="field"><span>Monthly budget</span><select name="budget"><option value="">Prefer not to say</option><option>Under $2k</option><option>$2k to $5k</option><option>$5k to $15k</option><option>$15k+</option></select></label>
              <label class="field"><span>What would make this call worth it?</span><textarea name="notes" rows="3"></textarea></label>
              <input type="text" name="_gotcha" tabindex="-1" autocomplete="off" class="hp" aria-hidden="true">
              <div class="form__foot"><button type="button" class="tlink" data-back>Back</button><button type="submit" class="btn btn--red">Request this time {ARR}</button></div>
              <p class="small" data-form-note>I will confirm by email with a meeting link.</p>
            </form>
          </div>
          <div class="panel-step" data-step="3">
            <div class="confirm"><span class="confirm__icon" aria-hidden="true"></span><h3>Requested.</h3><p>I will confirm by email within one business day with a meeting link.</p>
              <dl class="kpis kpis--list"><div><dt>When</dt><dd id="cWhen"></dd></div><div><dt>Who</dt><dd id="cWho"></dd></div><div><dt>Focus</dt><dd id="cFocus"></dd></div></dl>
              <div class="actions"><a class="btn btn--red" id="gcalLink" target="_blank" rel="noopener">Add to Google Calendar</a><a class="tlink" id="icsLink" download="consultation.ics">Download .ics</a></div></div>
          </div>
          <div class="booker__bar" id="bookBar"><p id="bookSum"></p><button type="button" class="btn btn--ink" id="toDetails" disabled>Continue {ARR}</button></div>
        </div>
        <aside class="book__side">
          <h3>What we will cover</h3>
          <ol class="agenda"><li><span>01</span>Your goal. The one number you most want to move.</li><li><span>02</span>Your data. A quick look at analytics and ad accounts.</li><li><span>03</span>Quick wins. The moves I would make first.</li><li><span>04</span>Next steps. With me, someone else, or on your own.</li></ol>
          <div class="who"><img src="{P}assets/img/avatar.png" alt="" width="56" height="56"><p><strong>Manjil Shrestha</strong><span data-availability>Available</span></p></div>
        </aside>
      </div>
    </section>

    <section class="sec">
      <div class="wrap faq">
        {sec_head(1, "Booking", "Good questions.")}
        {faq(BOOK_FAQ)}
      </div>
    </section>'''
    write('book/index.html', layout(P, 'book/', 'Book a Free Marketing Consultation in Melbourne | Manjil Shrestha', 'Book a free 30-minute marketing consultation with an independent digital marketing expert in Melbourne.', 'book', body, ['book.js'], [faq_ld(BOOK_FAQ)]))

# ================================================================== CONTACT
CONTACT_FAQ = [("Which areas do you work with?", "Melbourne and the rest of Australia. Most work is remote, with in-person workshops around Melbourne."), ("Are you open to full-time roles?", "Yes, for the right team. Choose \"Full-time role\" in the form and include the job link."), ("How quickly do you reply?", "Within one business day, usually the same day.")]

def contact():
    P = '../'
    days = [("Mon", "9:00 to 18:00"), ("Tue", "9:00 to 18:00"), ("Wed", "9:00 to 18:00"), ("Thu", "9:00 to 18:00"), ("Fri", "9:00 to 17:00"), ("Sat", "Closed"), ("Sun", "Closed")]
    aside = '<div class="clockbox"><p class="lab__k">Melbourne, now</p><p class="clock" id="mClock">--:--</p><p id="mStatus">Checking…</p></div>'
    body = phero(P, [("Home", ""), ("Contact", "contact/")], ["<span>Reply</span>Within one business day", "<span>Based</span>Melbourne, Australia", "<span>Open to</span>Projects and full-time roles"],
                 "Let's make your data talk.", "A new project, a second opinion on your numbers, a full-time role or a podcast invite. Write a few lines and I will get back to you.", '', aside) + f'''

    <section class="sec sec--tight" style="padding-top:0">
      <div class="wrap">
        <ul class="ways">
          <li class="rv"><span>Email</span><button type="button" data-copy-email data-email-text>hello@</button></li>
          <li class="rv"><span>Call</span><a href="{P}book/">Book a free 30-minute call {ARR}</a></li>
          <li class="rv"><span>LinkedIn</span><a href="https://www.linkedin.com/in/manjilshrestha" target="_blank" rel="noopener">/in/manjilshrestha {NE}</a></li>
          <li class="rv"><span>Hiring</span><a href="{P}assets/Manjil-Shrestha-CV.pdf">Download CV {ARR}</a></li>
        </ul>
      </div>
    </section>

    <section class="sec">
      <div class="wrap contact2">
        <div>{sec_head(1, "Write to me", "Tell me what you're working on.")}{contact_form("Website enquiry")}</div>
        <aside class="contact2__side"><h3>Office hours, Melbourne</h3><ul class="hours">{"".join(f'<li data-day="{d}"><span>{d}</span><span>{h}</span></li>' for d, h in days)}</ul><h3>Elsewhere</h3><div data-socials class="side__soc"></div></aside>
      </div>
    </section>

    <section class="sec">
      <div class="wrap faq">
        {sec_head(2, "Quick answers", "Good to know.")}
        {faq(CONTACT_FAQ)}
      </div>
    </section>'''
    write('contact/index.html', layout(P, 'contact/', 'Contact Manjil Shrestha | Digital Marketing Expert in Melbourne', 'Get in touch with Manjil Shrestha, an independent digital marketing expert in Melbourne.', 'contact', body, ['pages.js'], [faq_ld(CONTACT_FAQ)]))

# ================================================================== JOURNAL
def blog_index():
    P = '../'
    feat = POSTS[0]
    filt = ''.join(f'<button class="filter{" is-on" if k == "all" else ""}" data-filter="{k}">{n}</button>' for k, n in [("all", "All"), ("analytics", "Analytics"), ("local-seo", "Local SEO"), ("paid-media", "Paid media"), ("cro", "CRO"), ("email", "Email")])
    nl = '<form class="nl js-form" data-subject="Newsletter signup" action="https://formspree.io/f/YOUR_FORM_ID" method="POST" novalidate><label class="field"><span>One email a month</span><input type="email" name="email" required placeholder="you@company.com.au" autocomplete="email"></label><input type="text" name="_gotcha" tabindex="-1" autocomplete="off" class="hp" aria-hidden="true"><button class="btn btn--ink" type="submit"><span class="btn__text">Subscribe</span><span class="btn__sent">Subscribed</span></button></form>'
    body = phero(P, [("Home", ""), ("Journal", "blog/")], ["<span>Journal</span>Field notes", "<span>Topics</span>Analytics, SEO, paid, CRO", "<span>Cadence</span>Monthly"],
                 "Notes from the dashboard.", "What moved the numbers for Melbourne businesses, and how to do it yourself. Practical, specific, no fluff.", '', nl) + f'''

    <section class="sec sec--tight" style="padding-top:0">
      <div class="wrap">
        <a class="feat rv" href="{feat["slug"]}/" data-post data-tags="{feat["tagkey"]}" data-text="{E((feat["title"] + " " + feat["dek"]).lower())}">
          <div class="feat__img">{poster(feat["seed"], "GA4", "Analytics", 0, 900, 560)}</div>
          <div class="feat__txt"><p class="feat__k">Featured, {fmt_date(feat["date"])}, {feat["minutes"]} min</p><h2>{E(feat["title"])}</h2><p>{E(feat["dek"])}</p><span class="tlink">Read the article</span></div>
        </a>
        <div class="blog-tools rv"><div class="filters" role="group" aria-label="Filter by topic">{filt}</div><label class="search"><span class="sr">Search articles</span><input type="search" id="postSearch" placeholder="Search"><span id="postCount"></span></label></div>
        {journal_rows(P, POSTS, SOON)}
        <p class="empty" id="emptyState">Nothing matches that yet. <a class="tlink" href="{P}contact/">Suggest an article</a></p>
      </div>
    </section>
{cta(P, "Rather have me look at your numbers?", "A free 30-minute call with your real data is faster than reading.")}'''
    write('blog/index.html', layout(P, 'blog/', 'Journal: Analytics, SEO and Paid Media Notes | Manjil Shrestha', 'Practical articles on GA4, local SEO, paid media and CRO from an independent digital marketing expert in Melbourne.', 'blog', body, ['blog.js']))

def restyle(h):
    h = re.sub(r'<span class="note uv note--margin" data-note><span>(.*?)</span></span>', r'<span class="side">\1</span>', h, flags=re.S)
    return h

def article(p, i, template=False):
    P = '../../'
    path = f'blog/{p["slug"]}/'
    prev_p = POSTS[i - 1] if i > 0 else None
    next_p = POSTS[i + 1] if i + 1 < len(POSTS) else None
    pn = '' if template else '<nav class="pn" aria-label="More articles">' + (f'<a href="{P}blog/{prev_p["slug"]}/"><span>Newer</span>{E(prev_p["title"])}</a>' if prev_p else '<span></span>') + (f'<a href="{P}blog/{next_p["slug"]}/"><span>Older</span>{E(next_p["title"])}</a>' if next_p else '<span></span>') + '</nav>'
    big = {'analytics': 'GA4', 'local-seo': 'SEO', 'paid-media': 'ROAS'}.get(p['tagkey'], 'Note')
    body = f'''    <article class="art">
      <header class="art__head" id="top">
        <div class="wrap">
          {crumbs(P, [("Home", ""), ("Journal", "blog/"), (p["tag"], "blog/")])}
          <div class="art__grid">
            <ul class="ph__meta"><li><span>Topic</span>{E(p["tag"])}</li><li><span>Published</span>{fmt_date(p["date"])}</li><li><span>Reading time</span>{p["minutes"]} minutes</li><li><span>Author</span>Manjil Shrestha</li></ul>
            <div><h1 class="art__title"><span class="ln"><span>{E(p["title"])}</span></span></h1><p class="art__dek in">{E(p["dek"])}</p>
              <div class="share in"><a data-share="linkedin" target="_blank" rel="noopener">LinkedIn {NE}</a><a data-share="x" target="_blank" rel="noopener">X {NE}</a><button type="button" data-copy-link>Copy link</button></div></div>
          </div>
        </div>
      </header>
      <div class="wrap"><figure class="art__cover in">{poster(p["seed"], big, p["tag"], i % 3, 1600, 640)}</figure></div>
      <div class="wrap art__body">
        <aside class="toc"><p>Contents</p><ol id="toc"></ol><p class="toc__p"><span id="tocLeft">{p["minutes"]} min left</span></p><div class="meter"><i id="tocBar"></i></div></aside>
        <div class="art__col">
          <details class="toc-m"><summary>Contents</summary><ol id="tocMobile"></ol></details>
          <div class="prose" data-minutes="{p["minutes"]}">{restyle(p["body"]())}</div>
          <footer class="art__end">
            <div class="byline"><img src="{P}assets/img/avatar.png" alt="" width="64" height="64"><p><strong>Manjil Shrestha</strong> is an independent digital marketer in Melbourne. He fixes tracking first, then grows businesses with SEO, paid media and CRO. <a class="tlink" href="{P}book/">Book a free call</a></p></div>
            {pn}
          </footer>
        </div>
      </div>
    </article>
    <section class="sec">
      <div class="wrap">{sec_head(1, "Keep reading", "More from the journal.", f'<a class="tlink" href="{P}blog/">All articles</a>')}{journal_rows(P, [q for q in POSTS if q is not p])}</div>
    </section>'''
    write(path + 'index.html', layout(P, path, p["title"] + ' | Manjil Shrestha', p["dek"], 'blog', body, ['blog.js']))

# ================================================================== run
def copy_assets():
    for rel in ['js/content.js', 'js/book.js', 'js/blog.js', 'js/pages.js', 'js/vendor/gsap.min.js', 'js/vendor/ScrollTrigger.min.js', 'js/vendor/lenis.min.js', 'js/vendor/LICENSE-lenis.txt', 'assets/img/portrait.jpg', 'assets/img/avatar.png']:
        dst = os.path.join(OUT, rel); os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copyfile(os.path.join(ROOT, rel), dst)
    star = re.search(r'<symbol id="star" viewBox="0 0 100 100"><path fill="currentColor" d="([^"]+)"', SYMBOLS).group(1)
    open(os.path.join(OUT, 'assets/favicon.svg'), 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" fill="{RED}"/><g transform="translate(10 10) scale(.44)"><path fill="{INK}" d="{star}"/></g></svg>\n')

if __name__ == '__main__':
    copy_assets()
    home(); services(); seo(); book(); contact(); blog_index()
    for i, p in enumerate(POSTS):
        article(p, i)
    article(TEMPLATE, 0, template=True)
