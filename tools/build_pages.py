"""Generates the inner pages of the mastha site. Run: python3 tools/build_pages.py"""
import os
import math, os, html
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SC = os.path.dirname(os.path.abspath(__file__)) + '/'
SITE = 'https://manjilshrestha.online/'
SYM = open(SC + 'symbols.txt').read()
E = html.escape

# ---------------------------------------------------------------- helpers
def cover_svg(seed, W=400, H=225, uid=''):
    def rnd(n):
        x = math.sin(seed * 99 + n * 7.13) * 10000
        return x - math.floor(x)
    k = W / 400
    s = []
    for i in range(9):
        s.append(f'<circle cx="{(280 + rnd(i) * 60) * k:.1f}" cy="{(90 + rnd(i + 3) * 40) * (H / 225):.1f}" r="{(20 + i * 22) * k:.1f}" fill="none" stroke="rgba(181,150,255,{0.5 - i * 0.05:.2f})" stroke-width="1"/>')
    n = int(14 * k)
    for i in range(n):
        h = (20 + rnd(i + 20) * 90 + (i % 14) * 4) * (H / 225)
        s.append(f'<rect x="{(20 + i * 17):.1f}" y="{H * 0.8 - h:.1f}" width="9" height="{h:.1f}" rx="2" fill="url(#cg{uid}{seed})" opacity="{0.35 + (i % 14) * 0.045:.2f}"/>')
    return (f'<svg viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><defs>'
            f'<linearGradient id="cg{uid}{seed}" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#B596FF"/><stop offset="1" stop-color="#2A1566"/></linearGradient>'
            f'<radialGradient id="cr{uid}{seed}" cx=".75" cy=".3" r=".7"><stop offset="0" stop-color="#7844E9" stop-opacity=".45"/><stop offset="1" stop-color="#7844E9" stop-opacity="0"/></radialGradient></defs>'
            f'<rect width="{W}" height="{H}" fill="url(#cr{uid}{seed})"/>{"".join(s)}</svg>')

def spark_svg(series, W=150, H=46):
    mx, mn = max(series), min(series); r = (mx - mn) or 1
    pts = [(4 + i / (len(series) - 1) * (W - 8), H - 4 - (v - mn) / r * (H - 8)) for i, v in enumerate(series)]
    d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f}" + "".join(f" L{x:.1f},{y:.1f}" for x, y in pts[1:])
    lx, ly = pts[-1]
    return f'<svg class="svcx__spark" viewBox="0 0 {W} {H}" aria-hidden="true"><path d="{d}" fill="none" stroke="#B596FF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" filter="url(#uvglow)"/><circle cx="{lx:.1f}" cy="{ly:.1f}" r="3.5" fill="#DCCBFF"/></svg>'

ICONS = {
    'seo': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5L21 21"/></svg>',
    'paid': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 18l6-6 4 4 8-9"/><path d="M15 7h6v6"/></svg>',
    'analytics': '<svg viewBox="0 0 24 24" fill="currentColor"><rect x="3" y="12" width="4" height="9" rx="1"/><rect x="10" y="6" width="4" height="15" rx="1"/><rect x="17" y="2" width="4" height="19" rx="1"/></svg>',
    'cro': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 4h18l-7 9v6l-4 2v-8z"/></svg>',
    'email': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>',
    'strategy': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5" fill="currentColor"/></svg>',
    'mail': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>',
    'cal': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/></svg>',
    'in': '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M4 9h4v12H4zM6 3a2 2 0 110 4 2 2 0 010-4zM10 9h4v1.8c.6-1.1 2-2.1 4-2.1 4 0 4.5 2.6 4.5 6V21h-4v-5.5c0-1.4 0-3.2-2-3.2s-2.3 1.5-2.3 3.1V21H10z"/></svg>',
    'brief': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5a2 2 0 012-2h4a2 2 0 012 2v2M3 13h18"/></svg>',
}
SPARK = '<svg aria-hidden="true"><use href="#spark"/></svg>'

def faq_block(items, open_first=True):
    out = []
    for i, (q, a) in enumerate(items):
        o = ' is-open' if (i == 0 and open_first) else ''
        out.append(f'<div class="faq__item reveal{o}"><button class="faq__q" aria-expanded="{"true" if o else "false"}" aria-controls="pfq{i}"><span>{E(q)}</span>{SPARK}</button><div class="faq__a" id="pfq{i}" role="region"><div><p>{E(a)}</p></div></div></div>')
    return '\n'.join(out)

def faq_ld(items):
    import json
    return json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}, ensure_ascii=False)

def crumbs_ld(trail):
    import json
    return json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + p} for i, (n, p) in enumerate(trail)]}, ensure_ascii=False)

def crumbs_html(P, trail):
    parts = []
    for i, (n, p) in enumerate(trail):
        if i == len(trail) - 1:
            parts.append(f'<span aria-current="page">{E(n)}</span>')
        else:
            parts.append(f'<a href="{P}{p}">{E(n)}</a><span aria-hidden="true">/</span>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + ''.join(parts) + '</nav>'

# ---------------------------------------------------------------- layout
NAV = [('About', '#about', None), ('Services', 'services/', 'services'), ('Work', '#work', None), ('Growth Lab', '#lab', None), ('Blog', 'blog/', 'blog'), ('Contact', 'contact/', 'contact')]

def layout(P, path, title, desc, active, body, scripts=(), ld=(), og_type='website', noindex=False, og_image='assets/img/og-image.png'):
    canon = SITE + path
    nav = '\n      '.join(f'<a href="{P}{h}"{" class=\"is-active\" aria-current=\"page\"" if k == active else ""}>{n}</a>' for n, h, k in NAV)
    menu = '\n      '.join(f'<a href="{P}{h}"><small>0{i + 1}</small>{n}</a>' for i, (n, h, k) in enumerate(NAV + [('Book a free call', 'book/', 'book')]))
    lds = '\n'.join(f'  <script type="application/ld+json">{x}</script>' for x in ld)
    scr = '\n'.join(f'  <script src="{P}js/{s}"></script>' for s in scripts)
    robots = 'noindex, follow' if noindex else 'index, follow, max-image-preview:large'
    return f'''<!DOCTYPE html>
<html lang="en-AU">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{E(title)}</title>
  <meta name="description" content="{E(desc)}">
  <meta name="author" content="Manjil Shrestha">
  <meta name="robots" content="{robots}">
  <meta name="theme-color" content="#141317">
  <meta name="color-scheme" content="dark">
  <link rel="canonical" href="{canon}">
  <meta property="og:type" content="{og_type}">
  <meta property="og:locale" content="en_AU">
  <meta property="og:site_name" content="mastha — Manjil Shrestha">
  <meta property="og:title" content="{E(title)}">
  <meta property="og:description" content="{E(desc)}">
  <meta property="og:url" content="{canon}">
  <meta property="og:image" content="{SITE}{og_image}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{E(title)}">
  <meta name="twitter:description" content="{E(desc)}">
  <meta name="twitter:image" content="{SITE}{og_image}">
  <link rel="icon" type="image/png" sizes="32x32" href="{P}assets/favicon-32.png">
  <link rel="apple-touch-icon" href="{P}assets/apple-touch-icon.png">
  <link rel="manifest" href="{P}site.webmanifest">
  <link rel="alternate" type="application/rss+xml" title="mastha — Notes from the dashboard" href="{P}blog/feed.xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Geist:wght@300..800&family=Geist+Mono:wght@400;500&family=Pirata+One&family=Caveat:wght@600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{P}css/styles.css">
  <link rel="stylesheet" href="{P}css/pages.css">
{lds}
</head>

<body class="no-js">
  <script>document.body.classList.replace('no-js','js');</script>
  <svg width="0" height="0" style="position:absolute" aria-hidden="true">
    {SYM}
    <symbol id="spark" viewBox="0 0 100 100"><path fill="currentColor" d="M50 0C53 36 64 47 100 50C64 53 53 64 50 100C47 64 36 53 0 50C36 47 47 36 50 0Z"/></symbol>
    <filter id="uvglow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </svg>

  <div class="torch" aria-hidden="true"></div>
  <div class="cursor" id="cursor" aria-hidden="true"><i class="cursor__dot"></i><i class="cursor__ring"></i><span class="cursor__label" id="cursorLabel"></span></div>
  <div class="grain" aria-hidden="true"></div>
  <div class="progress" id="progress" aria-hidden="true"></div>
  <div class="hud" id="hud">
    <button class="hud__count" id="hudCount" aria-label="Hidden notes found"><svg><use href="#spark"/></svg><span><b id="foundN">0</b>/<span id="foundT">0</span> UV notes</span></button>
    <button class="hud__btn" id="revealAll" aria-pressed="false">Reveal all</button>
  </div>
  <div class="toast" id="toast" role="status" aria-live="polite"></div>

  <header class="nav" id="nav">
    <a href="{P}" class="nav__brand" aria-label="mastha, home"><svg viewBox="0 0 1911 515"><use href="#mastha"/></svg></a>
    <nav class="nav__links" aria-label="Primary">
      {nav}
    </nav>
    <div class="nav__right">
      <a href="{P}contact/" class="nav__me" aria-label="Contact Manjil"><img src="{P}assets/img/avatar.png" alt="" width="34" height="34"><i class="online"></i></a>
      <a href="{P}book/" class="btn btn--violet btn--sm" data-magnetic>Book a call</a>
      <button class="nav__burger" id="burger" aria-label="Open menu" aria-expanded="false" aria-controls="menu"><span></span><span></span></button>
    </div>
  </header>
  <div class="menu" id="menu" aria-hidden="true">
    <nav class="menu__links">
      {menu}
    </nav>
    <div class="menu__foot" data-socials></div>
  </div>

  <main>
{body}
  </main>

  <footer class="footer">
    <div class="container">
      <div class="footer__top">
        <p class="footer__line">Digital marketing expert in Melbourne.<br><span class="muted">Measured, not guessed.</span></p>
        <nav class="footer__links" aria-label="Footer"><a href="{P}services/">Services</a><a href="{P}#work">Work</a><a href="{P}blog/">Blog</a><a href="{P}book/">Book a call</a><a href="{P}contact/">Contact</a><a href="{P}blog/feed.xml">RSS</a></nav>
      </div>
      <div class="footer__logo">
        <svg viewBox="0 0 1911 515" class="footer__logo-dim" role="img" aria-label="mastha"><use href="#mastha"/></svg>
        <svg viewBox="0 0 1911 515" class="footer__logo-lit uv" aria-hidden="true"><use href="#mastha"/></svg>
        <div class="note uv" data-note style="--nx:66%;--ny:-22%;--rot:4deg"><span>you made it to the very end.<br>that's analyst energy. let's talk.</span></div>
      </div>
      <div class="footer__bar mono">
        <span>© <span data-year>2026</span> Manjil Shrestha · mastha</span>
        <span class="hide-sm">Made in Melbourne under UV light</span>
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

def write(path, text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w').write(text)
    print('wrote', path)

def phero_title(lines):
    return '\n'.join(f'          <span class="line{" line--goth" if g else ""}"><span{" class=\"goth glow\"" if g else ""}>{t}</span></span>' for t, g in lines)

# ================================================================= SERVICES
SERVICES = [
    dict(id='seo', title='Search & SEO', short='Rank for what Melbourne actually searches.',
         what='Technical fixes, keyword architecture, local SEO and content that compounds. I build the pages Google wants to rank and the tracking to prove they produce leads, not just traffic.',
         who='Local service businesses, eCommerce stores and B2B companies that want consistent inbound enquiries without paying for every click.',
         deliver=['Technical SEO audit and fix list', 'Keyword map and site architecture', 'Suburb and service landing pages', 'Google Business Profile optimisation', 'Monthly content plan and briefs', 'Ranking and lead reporting'],
         kpis=['Organic leads', 'Top-3 rankings', 'Organic revenue', 'Core Web Vitals'], first='3–6 months', price='From $1,800/mo', spark=[3, 4, 4, 6, 8, 7, 11, 13, 14, 18, 21, 25]),
    dict(id='paid', title='Paid Media', short='Ads judged on revenue, not clicks.',
         what='Google, Meta and LinkedIn campaigns built on clean conversion tracking, tight structure and a weekly budget rule based on marginal return. Creative testing is built in, not bolted on.',
         who='Businesses spending $2k or more a month on ads, or ready to, who want to know exactly what each dollar returns.',
         deliver=['Account audit and restructure', 'Search, Performance Max and Shopping', 'Meta prospecting and retargeting', 'Weekly creative and copy tests', 'Budget allocation by marginal ROAS', 'Weekly performance notes'],
         kpis=['ROAS', 'CPA', 'Conversion value', 'MER'], first='4–8 weeks', price='From $1,500/mo + ad spend', spark=[10, 12, 9, 14, 16, 15, 19, 21, 24, 23, 27, 30]),
    dict(id='analytics', title='Analytics & Tracking', short='Every dollar traced to an outcome.',
         what='GA4, Google Tag Manager, server-side tagging, consent mode and Looker Studio dashboards. The foundation every other channel depends on, set up so your whole team can read it.',
         who='Anyone who has ever asked "are these numbers right?" and not liked the answer.',
         deliver=['GA4 and GTM audit', 'Event and key event tracking plan', 'eCommerce and lead tracking', 'Consent mode and server-side setup', 'Looker Studio dashboard', 'Team walkthrough and docs'],
         kpis=['Data accuracy', 'Attribution coverage', 'Hours saved on reporting'], first='2–4 weeks', price='From $1,200 one-off', spark=[8, 6, 9, 7, 11, 10, 13, 12, 15, 14, 17, 19]),
    dict(id='cro', title='Conversion (CRO)', short='More revenue from the same traffic.',
         what='Funnel analysis, session recordings, customer research and A/B tests prioritised by expected impact. I ship the tests and the landing pages, then report on revenue, not clicks.',
         who='Sites with at least 5,000 monthly visitors that convert below where they should.',
         deliver=['Funnel and UX audit', 'Research: recordings, surveys, interviews', 'Prioritised test roadmap', 'Landing page and checkout design', 'Test build and QA', 'Experiment reports'],
         kpis=['Conversion rate', 'Revenue per visitor', 'Average order value'], first='6–10 weeks', price='From $2,500 per sprint', spark=[11, 12, 11, 14, 16, 15, 19, 21, 23, 24, 26, 27]),
    dict(id='email', title='Email & Lifecycle', short='Turn one-time buyers into regulars.',
         what='Automated flows and segmented campaigns in Klaviyo or HubSpot. Welcome, browse and cart abandonment, post-purchase, win-back, all tested and tracked to revenue.',
         who='eCommerce and subscription brands with a list that is bigger than the revenue it produces.',
         deliver=['Account and deliverability audit', 'Core flow build (5–7 flows)', 'Behaviour-based segments', 'Monthly campaign calendar', 'Subject line and offer testing', 'Revenue attribution report'],
         kpis=['Revenue from email', 'Repeat purchase rate', 'List growth'], first='4–8 weeks', price='From $1,500 setup', spark=[6, 7, 9, 12, 14, 18, 21, 23, 26, 28, 30, 31]),
    dict(id='strategy', title='Strategy & Fractional CMO', short='A senior marketer without the full-time cost.',
         what='Quarterly growth plans, channel mix, budget setting, agency and freelancer briefs, and a reporting rhythm your board will actually read. Part-time, embedded, accountable.',
         who='Founders and small teams who need marketing leadership before they can justify a full-time hire.',
         deliver=['90-day growth plan', 'Channel mix and budget model', 'Agency and hiring briefs', 'Weekly team check-in', 'Monthly board-ready report', 'Quarterly strategy review'],
         kpis=['Blended CAC', 'MER', 'Pipeline value'], first='Ongoing', price='From $3,000/mo', spark=[2, 3, 3, 5, 6, 8, 9, 12, 13, 16, 19, 22]),
]

def services_page():
    P = '../'
    idx = '\n'.join(f'<a href="#{s["id"]}"><b>0{i + 1}</b>{E(s["title"])}</a>' for i, s in enumerate(SERVICES))
    items = []
    for i, s in enumerate(SERVICES):
        items.append(f'''        <article class="svcx__item reveal" id="{s["id"]}">
          {spark_svg(s["spark"])}
          <div class="svcx__head"><span class="svcx__icon">{ICONS[s["id"]]}</span><div><span class="svcx__n">0{i + 1} / 06</span><h2>{E(s["title"])}</h2><p class="svcx__short">{E(s["short"])}</p></div></div>
          <div class="svcx__body">
            <div><h3>What it is</h3><p>{E(s["what"])}</p><h3>Who it's for</h3><p>{E(s["who"])}</p></div>
            <div><h3>What you get</h3><ul class="ticks">{"".join(f"<li>{E(d)}</li>" for d in s["deliver"])}</ul></div>
          </div>
          <div class="svcx__foot">
            <div class="kpi-chips"><small>Measured by</small>{"".join(f"<span>{E(k)}</span>" for k in s["kpis"])}</div>
            <div class="svcx__facts"><div>First results<b>{E(s["first"])}</b></div><div>Investment<b>{E(s["price"])}</b></div></div>
          </div>
          {'<a class="btn btn--violet btn--sm svcx__deep" href="seo/" data-magnetic>Explore SEO in depth →</a>' if s["id"] == "seo" else ''}
        </article>''')
    faqs = [
        ("Do you lock clients into long contracts?", "No. Audits and sprints are fixed-scope. Retainers run month to month after the first 90 days, because that is how long it takes to see a real trend."),
        ("Is ad spend included in the price?", "No. Ad spend is paid directly to Google, Meta or LinkedIn from your own account, so you always own the account and the data."),
        ("Can you work alongside my current agency or team?", "Yes. I often handle analytics, strategy or CRO while an agency or in-house team runs execution, and I write briefs they can act on."),
        ("What do you need from me to start?", "Access to your analytics and ad accounts, your revenue or lead numbers for the last 12 months, and one person who can make decisions."),
        ("How and when do you report?", "A short written update every week and a Looker Studio dashboard you can open any time. Monthly, we review results against the targets we agreed."),
    ]
    body = f'''    <section class="phero" id="top">
      <div class="container">
        {crumbs_html(P, [("Home", ""), ("Services", "services/")])}
        <div class="phero__grid">
          <div>
            <p class="label fade">Services · Melbourne &amp; remote</p>
            <h1 class="phero__title" aria-label="Marketing services that pay for themselves">
{phero_title([("Marketing services", False), ("that pay for", False), ("themselves.", True)])}
            </h1>
            <p class="phero__lead fade">Six services, one operating rule: if it can't be measured, it doesn't get budget. Pick the one you need, or let me build the right mix for your stage and budget.</p>
            <div class="phero__cta fade"><a href="{P}book/" class="btn btn--violet" data-magnetic>Book a free consultation <span class="arr">→</span></a><a href="#packages" class="btn btn--ghost">See packages &amp; pricing</a></div>
          </div>
          <div class="phero__chips fade">
            <span class="chip chip--uv">Free 30-min audit call</span><span class="chip">Fixed-price sprints</span><span class="chip">No lock-in contracts</span><span class="chip">You own every account</span><span class="chip">Weekly reporting</span>
          </div>
        </div>
        <div class="note uv" data-note style="--nx:52%;--ny:38%;--rot:-6deg"><span>every service here has a KPI attached.<br>no exceptions. no vibes.</span></div>
      </div>
      <div class="phero__ink uv" aria-hidden="true">ROI ↗</div>
    </section>

    <section class="section section--tight">
      <div class="container svcx__grid">
        <aside class="svcx__index">
          <h4>All services</h4>
          <nav aria-label="Services">{idx}</nav>
          <a href="{P}book/" class="btn btn--ghost btn--sm">Not sure? Ask me →</a>
        </aside>
        <div>
{chr(10).join(items)}
        </div>
      </div>
    </section>

    <section class="section" id="packages">
      <div class="container">
        <div class="head head--row">
          <div><p class="label reveal">Packages</p><h2 class="h2 reveal">Three ways to <span class="goth glow">work</span> together.</h2></div>
          <p class="lead reveal">Start small with an audit, run a focused 90-day sprint, or bring me in as your part-time head of marketing.</p>
        </div>
        <div class="plans" style="position:relative">
          <article class="plan reveal">
            <p class="plan__h">01 · Diagnose</p><h3>Growth Audit</h3><p class="plan__for">For businesses that want a clear, honest picture first.</p>
            <p class="plan__price">$1,500 <small>one-off</small></p>
            <div class="plan__meta"><span class="chip">2 weeks</span><span class="chip">Fixed price</span></div>
            <ul class="ticks"><li>Analytics and tracking audit</li><li>Channel-by-channel performance review</li><li>Funnel and landing page review</li><li>Prioritised 90-day roadmap</li><li>60-minute walkthrough call</li></ul>
            <a href="{P}book/" class="btn btn--ghost btn--block">Start with an audit</a>
          </article>
          <article class="plan plan--hot reveal">
            <span class="plan__badge">Most popular</span>
            <p class="plan__h">02 · Build</p><h3>90-Day Growth Sprint</h3><p class="plan__for">For teams ready to move one or two numbers, fast.</p>
            <p class="plan__price">$4,500 <small>/ month · 3 months</small></p>
            <div class="plan__meta"><span class="chip chip--uv">1–2 channels</span><span class="chip">Weekly reporting</span></div>
            <ul class="ticks"><li>Everything in the Growth Audit</li><li>Tracking fixed and dashboard built</li><li>Strategy and execution in 1–2 channels</li><li>Weekly tests and optimisation</li><li>Weekly update and monthly review</li></ul>
            <a href="{P}book/" class="btn btn--violet btn--block" data-magnetic>Book a sprint call →</a>
          </article>
          <article class="plan reveal">
            <p class="plan__h">03 · Lead</p><h3>Fractional CMO</h3><p class="plan__for">For founders who need senior marketing leadership.</p>
            <p class="plan__price">$3,000 <small>/ month · ongoing</small></p>
            <div class="plan__meta"><span class="chip">2 days a month+</span><span class="chip">Month to month</span></div>
            <ul class="ticks"><li>Quarterly growth plan and budget</li><li>Agency and freelancer management</li><li>Hiring support and briefs</li><li>Weekly team check-in</li><li>Monthly board-ready report</li></ul>
            <a href="{P}book/" class="btn btn--ghost btn--block">Talk about leadership</a>
          </article>
          <div class="note uv" data-note style="--nx:38%;--ny:-7%;--rot:4deg"><span>psst: it's always the middle one.</span></div>
        </div>
        <p class="fine-print">Demo pricing in AUD, excluding GST. Final scope and price confirmed after a free call.</p>
      </div>
    </section>

    <section class="section section--tight">
      <div class="container">
        <div class="head"><p class="label reveal">How it works</p><h2 class="h2 reveal">A loop, <span class="goth glow">not</span> a launch.</h2></div>
        <ol class="flow">
          <li class="reveal"><b>01</b><strong>Diagnose</strong><p>Audit data, funnel and market. Find the leaks.</p></li>
          <li class="reveal"><b>02</b><strong>Strategy</strong><p>Agree targets and the channels that can hit them.</p></li>
          <li class="reveal"><b>03</b><strong>Build</strong><p>Tracking, campaigns, pages and flows, instrumented.</p></li>
          <li class="reveal"><b>04</b><strong>Measure</strong><p>Weekly reporting in a dashboard you own.</p></li>
          <li class="reveal"><b>05</b><strong>Scale</strong><p>Double down on what the data proves.</p></li>
        </ol>
      </div>
    </section>

    <section class="section section--tight">
      <div class="container">
        <div class="head"><p class="label reveal">Industries</p><h2 class="h2 reveal">Who I <span class="goth glow">work</span> with.</h2></div>
        <div class="cloud reveal"><span>eCommerce &amp; DTC</span><span>Local &amp; home services</span><span>B2B SaaS</span><span>Health &amp; wellness</span><span>Hospitality</span><span>Professional services</span><span>Education</span><span>Not-for-profit</span><span>Startups</span></div>
      </div>
    </section>

    <section class="section section--tight">
      <div class="container faq__grid">
        <div><p class="label reveal">Services FAQ</p><h2 class="h2 reveal">Before you <span class="goth glow">ask</span>.</h2></div>
        <div class="faq__list">
{faq_block(faqs)}
        </div>
      </div>
    </section>

    <section class="section section--tight">
      <div class="container">
        <div class="cta-band reveal">
          <div><h2>Not sure which service fits? That's what the <span class="goth glow">free call</span> is for.</h2><p>30 minutes, your numbers, my honest take. If I'm not the right fit, I'll tell you who is.</p></div>
          <div class="cta-band__actions"><a href="{P}book/" class="btn btn--violet btn--lg" data-magnetic>Book a free consultation →</a></div>
        </div>
      </div>
    </section>'''
    import json
    catalog = json.dumps({"@context": "https://schema.org", "@type": "ProfessionalService", "@id": SITE + "#service", "name": "mastha — Digital Marketing Expert in Melbourne", "url": SITE + "services/",
                          "areaServed": {"@type": "City", "name": "Melbourne"},
                          "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Digital marketing services", "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["title"], "description": s["what"]}} for s in SERVICES]}}, ensure_ascii=False)
    write('services/index.html', layout(P, 'services/', 'Digital Marketing Services in Melbourne | SEO, Ads, Analytics & CRO | mastha',
                                        'SEO, paid media, GA4 analytics, CRO, email and fractional CMO services from Manjil Shrestha, a data-driven digital marketing expert in Melbourne. Clear pricing, no lock-in.',
                                        'services', body, scripts=['pages.js'], ld=[catalog, faq_ld(faqs), crumbs_ld([("Home", ""), ("Services", "services/")])]))

# ================================================================= BOOK
def book_page():
    P = '../'
    faqs = [
        ("Is the consultation really free?", "Yes. No card, no invoice afterwards, no obligation. It's how I find out whether I can genuinely help."),
        ("What happens in the call?", "We look at your goals and your numbers, I point out the two or three biggest opportunities I can see, and you leave with next steps whether or not we work together."),
        ("Can I reschedule?", "Of course. Reply to the confirmation email with a better time and I'll move it."),
        ("Will you sign an NDA?", "Happy to. Send it through before the call and I'll sign it before we look at anything sensitive."),
    ]
    body = f'''    <section class="phero" id="top">
      <div class="container">
        {crumbs_html(P, [("Home", ""), ("Book a free consultation", "book/")])}
        <div class="phero__grid">
          <div>
            <p class="label fade">Free consultation</p>
            <h1 class="phero__title" aria-label="Book a free consultation">
{phero_title([("Book a free", False), ("consultation.", True)])}
            </h1>
            <p class="phero__lead fade">30 minutes. Your numbers, my honest take. No pitch deck and no obligation. You'll leave with the two or three moves I'd make first.</p>
            <div class="phero__chips fade"><span class="chip chip--uv">30 min · video call</span><span class="chip">Free, no obligation</span><span class="chip">Melbourne time</span><span class="chip">Reply within 24h</span></div>
          </div>
        </div>
        <div class="note uv" data-note style="--nx:56%;--ny:30%;--rot:-5deg"><span>yes, actually free.<br>no surprise "discovery fee" invoice.</span></div>
      </div>
    </section>

    <section class="section section--tight" style="padding-top:0">
      <div class="container book__grid">
        <div class="booker reveal" id="booker">
          <ol class="stepper"><li class="is-on"><b>1</b><span>Pick a time</span></li><li><b>2</b><span>Your details</span></li><li><b>3</b><span>Confirmed</span></li></ol>

          <div class="panel-step is-on" data-step="1">
            <div class="picker">
              <div class="cal">
                <div class="cal__head"><h3 id="calMonth">Month</h3><div class="cal__nav"><button type="button" id="calPrev" aria-label="Previous month">←</button><button type="button" id="calNext" aria-label="Next month">→</button></div></div>
                <div class="cal__dow"><span>Mon</span><span>Tue</span><span>Wed</span><span>Thu</span><span>Fri</span><span>Sat</span><span>Sun</span></div>
                <div class="cal__days" id="calDays"></div>
              </div>
              <div class="slots">
                <h4 id="slotsDay">Day</h4>
                <p class="slots__tz" id="slotsTz"></p>
                <div class="slots__list" id="slotsList"></div>
              </div>
            </div>
          </div>

          <div class="panel-step" data-step="2">
            <form class="form form--flat" id="bookForm" action="https://formspree.io/f/YOUR_FORM_ID" method="POST" novalidate>
              <div class="picked"><span id="pickedText"></span><button type="button" data-back>Change</button></div>
              <input type="hidden" name="slot" id="bfSlot">
              <div class="form__row">
                <label class="field"><span>Name</span><input type="text" name="name" required autocomplete="name" placeholder="Jane Smith"></label>
                <label class="field"><span>Email</span><input type="email" name="email" required autocomplete="email" placeholder="jane@company.com.au"></label>
              </div>
              <label class="field"><span>Website</span><input type="text" name="website" placeholder="company.com.au"></label>
              <div class="form__row">
                <label class="field"><span>Main focus</span><select name="focus"><option value="">Not sure yet</option><option>SEO</option><option>Paid media</option><option>Analytics &amp; tracking</option><option>Conversion (CRO)</option><option>Email &amp; lifecycle</option><option>Overall strategy</option><option>Full-time role</option></select></label>
                <label class="field"><span>Monthly marketing budget</span><select name="budget"><option value="">Prefer not to say</option><option>Under $2k</option><option>$2k – $5k</option><option>$5k – $15k</option><option>$15k+</option></select></label>
              </div>
              <label class="field"><span>What would make this call worth it?</span><textarea name="notes" rows="3" placeholder="e.g. Our Google Ads spend doubled but leads didn't. I want to know why."></textarea></label>
              <input type="text" name="_gotcha" tabindex="-1" autocomplete="off" class="hp" aria-hidden="true">
              <div class="form__foot"><button type="button" class="btn btn--ghost" data-back>← Back</button><button type="submit" class="btn btn--violet btn--lg" data-magnetic>Request this time →</button></div>
              <p class="mono muted small" data-form-note>I'll confirm by email with a meeting link.</p>
            </form>
          </div>

          <div class="panel-step" data-step="3">
            <div class="confirm">
              <svg class="confirm__icon"><use href="#spark"/></svg>
              <h3>Your time is requested.</h3>
              <p>I'll confirm by email within one business day with a meeting link. Add it to your calendar now so it doesn't get lost.</p>
              <div class="confirm__card"><div><span>When · </span><b id="cWhen"></b></div><div><span>Who · </span><b id="cWho"></b></div><div><span>Focus · </span><b id="cFocus"></b></div></div>
              <div class="confirm__actions"><a class="btn btn--violet" id="gcalLink" target="_blank" rel="noopener">Add to Google Calendar</a><a class="btn btn--ghost" id="icsLink" download="mastha-consultation.ics">Download .ics</a></div>
              <a href="{P}blog/" class="link">While you wait, read the blog →</a>
            </div>
          </div>

          <div class="booker__bar" id="bookBar"><p class="booker__sum" id="bookSum"></p><button type="button" class="btn btn--violet" id="toDetails" disabled>Continue →</button></div>
          <div class="note uv" data-note style="--nx:6%;--ny:-6%;--rot:-4deg"><span>tuesdays are my favourite. just saying.</span></div>
        </div>

        <aside class="side">
          <div class="side-card reveal">
            <h3>What we'll cover</h3>
            <ol class="agenda">
              <li><b>01</b><div><strong>Your goal</strong><span>The one number you most want to move.</span></div></li>
              <li><b>02</b><div><strong>Your data</strong><span>A quick look at analytics and ad accounts.</span></div></li>
              <li><b>03</b><div><strong>Quick wins</strong><span>The 2–3 moves I'd make first.</span></div></li>
              <li><b>04</b><div><strong>Next steps</strong><span>With me, someone else, or on your own.</span></div></li>
            </ol>
          </div>
          <div class="side-card mini-quote reveal">
            <p>"Thirty minutes with Manjil gave us a clearer plan than three months with our old agency."</p>
            <footer>Daniel P. · Managing Director (demo)</footer>
          </div>
          <div class="side-card reveal">
            <div class="me me--sm"><img src="{P}assets/img/avatar.png" alt="Manjil Shrestha" width="52" height="52"><div><strong>Manjil Shrestha</strong><span class="mono">mastha · Melbourne</span></div></div>
            <p class="me__status"><i class="online"></i><span data-availability>Available</span></p>
            <p class="muted small">Prefer email? <a class="link" href="{P}contact/">Send a message</a></p>
          </div>
        </aside>
      </div>
    </section>

    <section class="section section--tight">
      <div class="container">
        <div class="head"><p class="label reveal">Before the call</p><h2 class="h2 reveal">Get the most from <span class="goth glow">30 minutes</span>.</h2></div>
        <div class="prep">
          <div class="reveal"><b>01</b><h3>Analytics access</h3><p>Viewer access to GA4 or a screenshot of the last 90 days.</p></div>
          <div class="reveal"><b>02</b><h3>One target</h3><p>The number that matters most: leads, sales, ROAS or CAC.</p></div>
          <div class="reveal"><b>03</b><h3>Rough budget</h3><p>What you spend on marketing per month, roughly. Ranges are fine.</p></div>
          <div class="reveal"><b>04</b><h3>Your questions</h3><p>The thing you've been arguing about internally. Bring it.</p></div>
        </div>
      </div>
    </section>

    <section class="section section--tight">
      <div class="container faq__grid">
        <div><p class="label reveal">Booking FAQ</p><h2 class="h2 reveal">Good <span class="goth glow">questions</span>.</h2></div>
        <div class="faq__list">
{faq_block(faqs)}
        </div>
      </div>
    </section>'''
    write('book/index.html', layout(P, 'book/', 'Book a Free Marketing Consultation in Melbourne | mastha',
                                    'Book a free 30-minute marketing consultation with Manjil Shrestha, a data-driven digital marketing expert in Melbourne. Pick a time that suits you.',
                                    'book', body, scripts=['book.js'], ld=[faq_ld(faqs), crumbs_ld([("Home", ""), ("Book a free consultation", "book/")])]))

# ================================================================= CONTACT
def contact_page():
    P = '../'
    faqs = [
        ("Which areas do you work with?", "I'm based in Melbourne and work with businesses across Victoria and Australia. Most work is remote, with in-person workshops around Melbourne."),
        ("Are you open to full-time roles?", "Yes, for the right team. Choose \"Full-time role\" in the form and include the job link."),
        ("How quickly do you reply?", "Within one business day, usually the same day during Melbourne working hours."),
    ]
    days = [("Mon", "9:00 – 18:00"), ("Tue", "9:00 – 18:00"), ("Wed", "9:00 – 18:00"), ("Thu", "9:00 – 18:00"), ("Fri", "9:00 – 17:00"), ("Sat", "Closed"), ("Sun", "Closed")]
    hours = ''.join(f'<li data-day="{d}"><span>{d}</span><span>{h}</span></li>' for d, h in days)
    radar = '''<svg class="radar" viewBox="0 0 320 160" aria-hidden="true">
              <defs><radialGradient id="rg" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#7844E9" stop-opacity=".35"/><stop offset="1" stop-color="#7844E9" stop-opacity="0"/></radialGradient><linearGradient id="sw" x1="0" x2="1"><stop offset="0" stop-color="#B596FF" stop-opacity="0"/><stop offset="1" stop-color="#B596FF" stop-opacity=".5"/></linearGradient></defs>
              <circle cx="160" cy="80" r="76" fill="url(#rg)"/>
              <g fill="none" stroke="rgba(236,232,244,.12)"><circle cx="160" cy="80" r="26"/><circle cx="160" cy="80" r="50"/><circle cx="160" cy="80" r="74"/><path d="M84 80h152M160 6v148"/></g>
              <path class="sweep" d="M160 80 L234 80 A74 74 0 0 0 212 28 Z" fill="url(#sw)"/>
              <circle cx="160" cy="80" r="5" fill="#DCCBFF"><animate attributeName="r" values="4;7;4" dur="2s" repeatCount="indefinite"/></circle>
              <text x="172" y="72" fill="#B596FF" font-family="Geist Mono, monospace" font-size="10">MELBOURNE</text>
              <text x="172" y="98" fill="#8F8B9A" font-family="Geist Mono, monospace" font-size="9">-37.81°, 144.96°</text>
            </svg>'''
    body = f'''    <section class="phero" id="top">
      <div class="container">
        {crumbs_html(P, [("Home", ""), ("Contact", "contact/")])}
        <div class="phero__grid">
          <div>
            <p class="label fade">Contact</p>
            <h1 class="phero__title" aria-label="Let's make your data talk">
{phero_title([("Let's make", False), ("your data", False), ("talk.", True)])}
            </h1>
            <p class="phero__lead fade">New project, a second opinion on your numbers, a full-time role or a podcast invite. Send a message and I'll reply within one business day.</p>
          </div>
          <div class="status-card fade">
            <p class="label-sm">Right now in Melbourne</p>
            <p class="clock" id="mClock">--:--</p>
            <p class="status-line"><i class="online"></i><span id="mStatus">Checking…</span></p>
            {radar}
            <div class="note uv" data-note style="--nx:-30%;--ny:8%;--rot:-6deg"><span>if it's 2am and I reply,<br>please tell me to sleep.</span></div>
          </div>
        </div>
      </div>
    </section>

    <section class="section section--tight" style="padding-top:0">
      <div class="container">
        <div class="methods">
          <button class="method reveal" data-copy-email data-cursor="Copy"><span class="method__icon">{ICONS["mail"]}</span><h3>Email</h3><p data-email-text>hello@</p><span class="method__go">Copy address →</span></button>
          <a class="method reveal" href="{P}book/"><span class="method__icon">{ICONS["cal"]}</span><h3>Book a call</h3><p>Free 30-minute consultation, pick a time that suits.</p><span class="method__go">Choose a time →</span></a>
          <a class="method reveal" href="https://www.linkedin.com/in/manjilshrestha" target="_blank" rel="noopener"><span class="method__icon">{ICONS["in"]}</span><h3>LinkedIn</h3><p>Connect, or send a quick message there.</p><span class="method__go">Open profile ↗</span></a>
          <a class="method reveal" href="{P}assets/Manjil-Shrestha-CV.pdf"><span class="method__icon">{ICONS["brief"]}</span><h3>Hiring?</h3><p>Open to the right in-house role in Melbourne.</p><span class="method__go">Download CV ↓</span></a>
        </div>
      </div>
    </section>

    <section class="section section--tight">
      <div class="container contact2">
        <form class="form js-form reveal" data-subject="Website enquiry" action="https://formspree.io/f/YOUR_FORM_ID" method="POST" novalidate style="position:relative">
          <div class="form__row">
            <label class="field"><span>Name</span><input type="text" name="name" required autocomplete="name" placeholder="Jane Smith"></label>
            <label class="field"><span>Email</span><input type="email" name="email" required autocomplete="email" placeholder="jane@company.com.au"></label>
          </div>
          <div class="form__row">
            <label class="field"><span>Company / website</span><input type="text" name="company" placeholder="company.com.au"></label>
            <label class="field"><span>Phone (optional)</span><input type="tel" name="phone" autocomplete="tel" placeholder="04xx xxx xxx"></label>
          </div>
          <fieldset class="chips">
            <legend>What's this about?</legend>
            <label><input type="radio" name="topic" value="New project" checked><span>New project</span></label>
            <label><input type="radio" name="topic" value="Audit / second opinion"><span>Audit / second opinion</span></label>
            <label><input type="radio" name="topic" value="Full-time role"><span>Full-time role</span></label>
            <label><input type="radio" name="topic" value="Speaking / podcast"><span>Speaking / podcast</span></label>
            <label><input type="radio" name="topic" value="Just saying hi"><span>Just saying hi</span></label>
          </fieldset>
          <div class="form__row">
            <label class="field"><span>Monthly budget</span><select name="budget"><option value="">Not sure yet</option><option>Under $2k</option><option>$2k – $5k</option><option>$5k – $15k</option><option>$15k+</option><option>Not applicable</option></select></label>
            <label class="field"><span>How did you find me?</span><select name="source"><option value="">Select one</option><option>Google search</option><option>LinkedIn</option><option>Referral</option><option>The blog</option><option>Other</option></select></label>
          </div>
          <label class="field"><span>Message</span><textarea name="message" rows="5" required placeholder="What are you trying to grow, and by when?"></textarea></label>
          <input type="text" name="_gotcha" tabindex="-1" autocomplete="off" class="hp" aria-hidden="true">
          <div class="form__foot">
            <button type="submit" class="btn btn--violet btn--lg" data-magnetic><span class="btn__text">Send message →</span><span class="btn__sent">Sent. Talk soon ✓</span></button>
            <p class="mono muted small" data-form-note>No spam. Just a reply.</p>
          </div>
          <div class="note uv" data-note style="--nx:50%;--ny:-5%;--rot:5deg"><span>longer messages get better answers.</span></div>
        </form>

        <aside class="side">
          <div class="side-card reveal">
            <h3>After you hit send</h3>
            <ol class="agenda">
              <li><b>01</b><div><strong>I read it properly</strong><span>Usually the same day.</span></div></li>
              <li><b>02</b><div><strong>I reply with questions</strong><span>Or a straight answer if it's simple.</span></div></li>
              <li><b>03</b><div><strong>We book a call</strong><span>If it makes sense for both of us.</span></div></li>
            </ol>
          </div>
          <div class="side-card reveal">
            <h3>Office hours · Melbourne</h3>
            <ul class="hours">{hours}</ul>
          </div>
          <div class="side-card reveal">
            <h3>Elsewhere</h3>
            <div class="socials" data-socials></div>
          </div>
        </aside>
      </div>
    </section>

    <section class="section section--tight">
      <div class="container faq__grid">
        <div><p class="label reveal">Quick answers</p><h2 class="h2 reveal">Good to <span class="goth glow">know</span>.</h2></div>
        <div class="faq__list">
{faq_block(faqs)}
        </div>
      </div>
    </section>'''
    import json
    cp = json.dumps({"@context": "https://schema.org", "@type": "ContactPage", "name": "Contact Manjil Shrestha", "url": SITE + "contact/", "about": {"@id": SITE + "#person"}}, ensure_ascii=False)
    write('contact/index.html', layout(P, 'contact/', 'Contact Manjil Shrestha | Digital Marketing Expert in Melbourne',
                                       'Get in touch with Manjil Shrestha (mastha), a data-driven digital marketing expert in Melbourne. Projects, audits, full-time roles and speaking.',
                                       'contact', body, scripts=['pages.js'], ld=[cp, faq_ld(faqs), crumbs_ld([("Home", ""), ("Contact", "contact/")])]))

# ================================================================= BLOG POSTS
GA4_CHART = '''<svg viewBox="0 0 640 260" role="img" aria-label="Bar chart: reported purchases in GA4 compared with real orders, before and after the fixes">
  <g font-family="Geist Mono, monospace" font-size="11" fill="#8F8B9A">
    <text x="20" y="22">Weekly purchases · GA4 vs real orders</text>
    <text x="474" y="22" fill="#B596FF">■ GA4</text><text x="534" y="22" fill="#ECE8F4">■ Real orders</text>
  </g>
  <g stroke="rgba(236,232,244,.07)"><line x1="20" x2="620" y1="60" y2="60"/><line x1="20" x2="620" y1="120" y2="120"/><line x1="20" x2="620" y1="180" y2="180"/><line x1="20" x2="620" y1="230" y2="230" stroke="rgba(236,232,244,.2)"/></g>
  BARS
  <line x1="330" x2="330" y1="40" y2="236" stroke="#B596FF" stroke-dasharray="4 5"/>
  <text x="338" y="52" font-family="Caveat, cursive" font-size="20" fill="#DCCBFF">fixes shipped →</text>
  <g font-family="Geist Mono, monospace" font-size="10" fill="#8F8B9A">LABELS</g>
</svg>'''
def ga4_chart():
    ga = [148, 156, 151, 162, 159, 121, 118, 124, 122, 127]
    real = [112, 116, 114, 119, 117, 117, 115, 121, 120, 125]
    bars, labels = [], []
    for i, (g, r) in enumerate(zip(ga, real)):
        x = 34 + i * 59
        gh, rh = g * 1.1, r * 1.1
        bars.append(f'<rect x="{x}" y="{230 - gh:.0f}" width="20" height="{gh:.0f}" rx="3" fill="#7844E9" opacity=".9"/><rect x="{x + 22}" y="{230 - rh:.0f}" width="20" height="{rh:.0f}" rx="3" fill="#ECE8F4" opacity=".75"/>')
        labels.append(f'<text x="{x + 6}" y="250">W{i + 1}</text>')
    return GA4_CHART.replace('BARS', ''.join(bars)).replace('LABELS', ''.join(labels))

def roas_chart():
    pts = [(0, 0), (5, 20), (10, 34), (15, 43), (20, 48)]
    X = lambda v: 50 + v * 27; Y = lambda v: 220 - v * 3.6
    d = 'M' + ' L'.join(f'{X(a):.0f},{Y(b):.0f}' for a, b in pts)
    be = f'M{X(0)},{Y(0)} L{X(20)},{Y(50)}'
    dots = ''.join(f'<circle cx="{X(a):.0f}" cy="{Y(b):.0f}" r="5" fill="#DCCBFF"/><text x="{X(a) + 8:.0f}" y="{Y(b) - 8:.0f}" font-family="Geist Mono, monospace" font-size="10" fill="#ECE8F4">${b}k</text>' for a, b in pts[1:])
    ticks = ''.join(f'<text x="{X(a) - 10:.0f}" y="240" font-family="Geist Mono, monospace" font-size="10" fill="#8F8B9A">${a}k</text>' for a, _ in pts)
    return f'''<svg viewBox="0 0 640 260" role="img" aria-label="Line chart: revenue flattens as ad spend rises, crossing below the breakeven line">
  <text x="20" y="22" font-family="Geist Mono, monospace" font-size="11" fill="#8F8B9A">Revenue vs monthly ad spend · breakeven at 2.5x ROAS</text>
  <g stroke="rgba(236,232,244,.07)"><line x1="50" x2="620" y1="40" y2="40"/><line x1="50" x2="620" y1="130" y2="130"/><line x1="50" x2="620" y1="220" y2="220" stroke="rgba(236,232,244,.2)"/></g>
  <path d="{be}" stroke="#F6C453" stroke-width="2" stroke-dasharray="6 6" fill="none"/>
  <text x="{X(14):.0f}" y="{Y(38):.0f}" font-family="Caveat, cursive" font-size="20" fill="#F6C453">breakeven line</text>
  <path d="{d}" stroke="#B596FF" stroke-width="3" fill="none" filter="url(#uvglow)"/>
  {dots}{ticks}
  <text x="{X(15.5):.0f}" y="{Y(52):.0f}" font-family="Caveat, cursive" font-size="20" fill="#DCCBFF">the last $10k lost money ↓</text>
</svg>'''

def site_tree():
    return '''<svg viewBox="0 0 640 230" role="img" aria-label="Site architecture: home links to service pages, which link to suburb pages">
  <g font-family="Geist Mono, monospace" font-size="11">
    <g stroke="#B596FF" stroke-opacity=".5" fill="none"><path d="M320 52 V80 M140 80 H500 M140 80 V100 M320 80 V100 M500 80 V100"/><path d="M140 136 V160 M80 160 H200 M80 160 V176 M140 160 V176 M200 160 V176"/><path d="M320 136 V160 M260 160 H380 M260 160 V176 M320 160 V176 M380 160 V176"/></g>
    <rect x="260" y="20" width="120" height="32" rx="10" fill="#7844E9"/><text x="300" y="40" fill="#fff">Home</text>
    <g fill="#1E1C24" stroke="rgba(236,232,244,.25)"><rect x="80" y="100" width="120" height="36" rx="10"/><rect x="260" y="100" width="120" height="36" rx="10"/><rect x="440" y="100" width="120" height="36" rx="10"/></g>
    <g fill="#ECE8F4"><text x="98" y="122">/plumbing/</text><text x="282" y="122">/hot-water/</text><text x="462" y="122">/blocked-drains/</text></g>
    <g fill="rgba(120,68,233,.18)" stroke="rgba(181,150,255,.5)"><rect x="46" y="176" width="68" height="30" rx="8"/><rect x="118" y="176" width="44" height="30" rx="8"/><rect x="166" y="176" width="68" height="30" rx="8"/><rect x="226" y="176" width="68" height="30" rx="8"/><rect x="298" y="176" width="44" height="30" rx="8"/><rect x="346" y="176" width="68" height="30" rx="8"/></g>
    <g fill="#DCCBFF" font-size="10"><text x="54" y="195">fitzroy</text><text x="124" y="195">kew</text><text x="172" y="195">carlton</text><text x="232" y="195">fitzroy</text><text x="304" y="195">kew</text><text x="352" y="195">carlton</text></g>
    <text x="440" y="190" fill="#8F8B9A">one page per suburb</text><text x="440" y="206" fill="#8F8B9A">you actually serve</text>
  </g>
</svg>'''

POSTS = [
    dict(slug='ga4-setups-lie-to-you', tag='Analytics', tagkey='analytics', date='2026-10-14', minutes=7, seed=1,
         title='Why most GA4 setups lie to you (and five fixes)',
         dek='Your dashboard says sales are up. Your bank account disagrees. Here are the five GA4 settings behind most of the gap, and how to fix each in under an hour.',
         body=lambda: f'''
<div class="tldr"><h4>TL;DR</h4><ul>
<li>In the audits I run, most GA4 properties miscount conversions somewhere between "a bit" and "wildly".</li>
<li>Five settings cause most of it: duplicate purchases, the wrong key events, internal traffic, payment-gateway referrals and short data retention.</li>
<li>All five are quick to fix. There's a checklist at the end.</li></ul></div>

<p>Every week someone shows me a GA4 report that looks great and a revenue number that doesn't. Nobody lied on purpose. GA4 just does exactly what it's told, and most properties were told the wrong things during a rushed setup two years ago.</p>

<h2 id="the-problem"><span class="num">00</span>The quiet problem</h2>
<p class="has-note">Bad tracking rarely breaks loudly. It drifts. A thank-you page that fires twice, a payment provider that steals the credit for a sale, your own team browsing the site all day. Each one nudges the numbers a little, and every budget decision you make sits on top of them. <span class="note uv note--margin" data-note><span>true story: one client's "record month" was a thank-you page firing twice.</span></span></p>
<div class="stat-row"><div><b>5</b><span>settings cause most of the damage</span></div><div><b>&lt;1 hr</b><span>to fix all of them</span></div><div><b>14 mo</b><span>of history you should be keeping</span></div></div>

<h2 id="duplicate-purchases" data-toc="Fix duplicate purchases"><span class="num">01</span>Fix duplicate purchases</h2>
<p>If a customer reloads the order confirmation page, or comes back to it from an email, many setups send a second <code>purchase</code> event. Your revenue in GA4 creeps above your real revenue, and your ROAS looks better than it is.</p>
<p>The fix is to always send a unique <code>transaction_id</code> with every purchase. GA4 uses it to recognise repeat purchase events for the same order.</p>
<pre><code><span class="c">// Push this once, on the order confirmation page</span>
dataLayer.push({{ ecommerce: null }});
dataLayer.push({{
  <span class="k">event</span>: <span class="s">"purchase"</span>,
  <span class="k">ecommerce</span>: {{
    <span class="k">transaction_id</span>: <span class="s">"ORD-10482"</span>,   <span class="c">// unique per order</span>
    <span class="k">value</span>: 189.00,
    <span class="k">currency</span>: <span class="s">"AUD"</span>
  }}
}});</code></pre>
<div class="callout"><span class="callout__i">✦</span><p><strong>Quick test:</strong> in GA4, compare purchases per week with orders from Shopify or your CRM. If GA4 is consistently higher, duplicates are the first suspect.</p></div>
<figure class="figure"><div class="figure__box">{ga4_chart()}</div><figcaption>Fig. 1 · Illustrative data. After deduplication, GA4 purchases track real orders closely.</figcaption></figure>

<h2 id="key-events" data-toc="Mark the right key events"><span class="num">02</span>Mark the right key events</h2>
<p>In 2024 Google renamed GA4 "conversions" to <strong>key events</strong>. Whatever you call them, they should be the handful of actions that mean money: a purchase, a qualified lead, a booked call. I regularly find properties where page views or scrolls are marked as key events, which makes every channel look like a winner.</p>
<div class="table-wrap"><table><thead><tr><th>Event</th><th>Key event?</th><th>Why</th></tr></thead><tbody>
<tr><td><code>purchase</code></td><td>Yes</td><td>Direct revenue</td></tr>
<tr><td><code>generate_lead</code></td><td>Yes</td><td>A real enquiry, once spam is filtered</td></tr>
<tr><td><code>book_call</code></td><td>Yes</td><td>Strongest B2B intent signal</td></tr>
<tr><td><code>scroll</code></td><td>No</td><td>Engagement, not an outcome</td></tr>
<tr><td><code>page_view</code></td><td>No</td><td>Inflates every report it touches</td></tr>
</tbody></table></div>

<h2 id="internal-traffic" data-toc="Filter out your own traffic"><span class="num">03</span>Filter out your own traffic</h2>
<p>Your team, your developers and your agency visit the site constantly. In a small business that can be a noticeable share of sessions and test conversions.</p>
<ol>
<li>In Admin, open your web data stream and choose <strong>Configure tag settings</strong>, then <strong>Define internal traffic</strong>. Add your office and home IP addresses.</li>
<li>In Admin, open <strong>Data filters</strong>. The internal traffic filter is created in a <em>Testing</em> state.</li>
<li>Check it in reports for a few days, then switch it to <strong>Active</strong>.</li>
</ol>
<div class="callout callout--warn"><span class="callout__i">!</span><p><strong>Watch out:</strong> filters only apply from the moment they're active. They don't clean historical data, so do this early.</p></div>

<h2 id="referrals" data-toc="Stop gateways stealing credit"><span class="num">04</span>Stop payment gateways stealing credit</h2>
<p class="has-note">When a customer pays through PayPal, Afterpay or a hosted checkout and returns to your site, GA4 can start a new session and credit the sale to that payment domain as a "referral". Your Google Ads campaign did the work and PayPal gets the trophy. <span class="note uv note--margin" data-note><span>PayPal has never once run your ads. stop thanking it.</span></span></p>
<p>Open your web stream's tag settings and use <strong>List unwanted referrals</strong> to add the payment domains you use, for example <code>paypal.com</code>, <code>afterpay.com</code> or <code>checkout.stripe.com</code>.</p>
<blockquote>You can't optimise what you can't trust. Fix the measurement first, then argue about the strategy.<cite>— Manjil Shrestha</cite></blockquote>

<h2 id="retention" data-toc="Keep 14 months of data"><span class="num">05</span>Keep 14 months of data, not 2</h2>
<p>GA4 standard properties default to keeping event-level data for <strong>2 months</strong>. That limit applies to explorations, the custom reports you use for deeper analysis. Change it to <strong>14 months</strong> under Admin, <strong>Data retention</strong>, so you can compare this season with last year's.</p>
<p>It takes a minute and it isn't retroactive, so the sooner the better.</p>

<h2 id="checklist" data-toc="The one-hour checklist"><span class="num">✓</span>The one-hour checklist</h2>
<ul class="checklist">
<li><label><input type="checkbox"><span>Every <code>purchase</code> sends a unique <code>transaction_id</code></span></label></li>
<li><label><input type="checkbox"><span>GA4 weekly purchases match your store or CRM within a few percent</span></label></li>
<li><label><input type="checkbox"><span>Only money-related actions are marked as key events</span></label></li>
<li><label><input type="checkbox"><span>Internal traffic is defined and the filter is Active</span></label></li>
<li><label><input type="checkbox"><span>Payment domains are listed as unwanted referrals</span></label></li>
<li><label><input type="checkbox"><span>Event data retention is set to 14 months</span></label></li>
<li><label><input type="checkbox"><span>Someone owns tracking, and checks it monthly</span></label></li>
</ul>

<h2 id="next" data-toc="What to do next">What to do next</h2>
<p>Run the checklist this week. If more than two boxes stay unticked, your reports are probably steering budget in the wrong direction. If you'd like a second pair of eyes, <a href="../../book/">book a free 30-minute audit call</a> and we'll go through your property together.</p>
'''),
    dict(slug='melbourne-local-seo-playbook', tag='Local SEO', tagkey='local-seo', date='2026-09-22', minutes=8, seed=2,
         title='A suburb-by-suburb playbook for ranking in Melbourne',
         dek='Melbourne customers search by suburb. Here is how to build pages, profiles and proof that rank in the suburbs you actually serve, without creating thin doorway pages.',
         body=lambda: f'''
<div class="tldr"><h4>TL;DR</h4><ul>
<li>People search "plumber Fitzroy", not "plumber Melbourne". Build for the suburbs you really serve.</li>
<li>One genuinely useful page per suburb beats fifty copy-pasted ones. Google's spam policies call out doorway pages.</li>
<li>Your Google Business Profile and reviews do as much work as your website. Measure leads by suburb.</li></ul></div>

<p>Melbourne is a city of suburbs, and its search behaviour follows. Local searchers add a suburb, a postcode or "near me", and Google answers with the map pack plus a handful of local pages. Here's the playbook I use for service businesses.</p>

<h2 id="architecture" data-toc="Build a suburb architecture"><span class="num">01</span>Build a suburb architecture</h2>
<p>Start with your services, then add a page for each suburb you genuinely serve and want more work in. Link them in a clear tree so both people and Google understand the structure.</p>
<figure class="figure"><div class="figure__box">{site_tree()}</div><figcaption>Fig. 1 · Service pages first, then suburb pages under each service.</figcaption></figure>
<div class="callout callout--warn"><span class="callout__i">!</span><p><strong>Avoid doorway pages.</strong> Pages that swap only the suburb name are exactly what Google's spam policies warn about. Each page needs something real and local.</p></div>
<p class="has-note">What makes a suburb page real: photos of jobs done there, the problems common to that area's housing or businesses, travel time and availability, local reviews and a short FAQ. <span class="note uv note--margin" data-note><span>if you can't write 5 true sentences about a suburb, don't make the page.</span></span></p>

<h2 id="gbp" data-toc="Make Google Business Profile work"><span class="num">02</span>Make your Google Business Profile do the heavy lifting</h2>
<ul>
<li>Choose the most specific primary category, then add relevant secondary ones.</li>
<li>Set accurate service areas, opening hours and services with descriptions.</li>
<li>Upload real photos regularly, especially of completed work.</li>
<li>Use posts for offers, seasonal reminders and new projects.</li>
</ul>

<h2 id="reviews" data-toc="Earn reviews and local proof"><span class="num">03</span>Earn reviews and local proof</h2>
<p>Ask every happy customer, every time, with a direct link. Reply to every review. When customers naturally mention the suburb or the job, that detail helps people choosing between you and a competitor down the road.</p>
<p>Local links matter too: suburb business associations, sponsorships of local clubs and events, and genuine partnerships with nearby businesses.</p>

<h2 id="content" data-toc="Write for problem-aware searches"><span class="num">04</span>Write for problem-aware searches</h2>
<p>Many searches happen before someone knows which service they need: "why is my hot water lukewarm", "cost to fix a blocked drain Melbourne". Answer those questions plainly, with prices or ranges where you can, and link to the relevant service and suburb pages.</p>

<h2 id="measure" data-toc="Measure leads by suburb"><span class="num">05</span>Measure leads by suburb</h2>
<p>Rankings are a means, not the goal. Track enquiries by landing page, and you'll see which suburbs earn their keep.</p>
<div class="table-wrap"><table><thead><tr><th>Suburb page</th><th>Top query</th><th>Avg. position</th><th>Leads / mo</th></tr></thead><tbody>
<tr><td>/plumbing/fitzroy/</td><td>plumber fitzroy</td><td>2.4</td><td>14</td></tr>
<tr><td>/plumbing/kew/</td><td>emergency plumber kew</td><td>4.1</td><td>9</td></tr>
<tr><td>/plumbing/carlton/</td><td>blocked drain carlton</td><td>7.8</td><td>3</td></tr>
</tbody></table></div>
<p><small class="muted">Illustrative data.</small></p>
<p>Want this built for your business? <a href="../../services/#seo">See the SEO service</a> or <a href="../../book/">book a free call</a>.</p>
'''),
    dict(slug='marginal-roas-budget-rule', tag='Paid Media', tagkey='paid-media', date='2026-08-18', minutes=5, seed=3,
         title='Marginal ROAS: the only budget rule you need',
         dek='Average ROAS tells you how your ads did. Marginal ROAS tells you what your next dollar will do. Only one of those should decide your budget.',
         body=lambda: f'''
<div class="tldr"><h4>TL;DR</h4><ul>
<li>Average ROAS hides diminishing returns. The last dollars you spend usually return far less than the first.</li>
<li>Your breakeven ROAS is 1 ÷ gross margin. At a 40% margin, that's 2.5x.</li>
<li>Keep adding budget while marginal ROAS beats breakeven. Move money from the channel with the lowest marginal ROAS to the highest.</li></ul></div>

<p>"Our ROAS is 2.4x, so let's spend more." It sounds sensible, and it's how a lot of good businesses quietly lose money on ads. The problem is the word <em>average</em>.</p>

<h2 id="average-vs-marginal" data-toc="Average vs marginal"><span class="num">01</span>Average vs marginal, in one table</h2>
<div class="table-wrap"><table><thead><tr><th>Monthly spend</th><th>Revenue</th><th>Average ROAS</th><th>Extra revenue from last $5k</th><th>Marginal ROAS</th></tr></thead><tbody>
<tr><td>$5,000</td><td>$20,000</td><td>4.0x</td><td>$20,000</td><td>4.0x</td></tr>
<tr><td>$10,000</td><td>$34,000</td><td>3.4x</td><td>$14,000</td><td>2.8x</td></tr>
<tr><td>$15,000</td><td>$43,000</td><td>2.9x</td><td>$9,000</td><td>1.8x</td></tr>
<tr><td>$20,000</td><td>$48,000</td><td>2.4x</td><td>$5,000</td><td>1.0x</td></tr>
</tbody></table></div>
<p class="has-note">At $20k a month, the average ROAS of 2.4x looks close to fine. But the last $5,000 brought in just $5,000. That's a marginal ROAS of 1.0x, which loses money for almost any business. <span class="note uv note--margin" data-note><span>the average is a polite liar.</span></span></p>
<figure class="figure"><div class="figure__box">{roas_chart()}</div><figcaption>Fig. 1 · Illustrative data. Revenue flattens as spend rises and drops below breakeven.</figcaption></figure>

<h2 id="breakeven" data-toc="Find your breakeven"><span class="num">02</span>Find your breakeven ROAS</h2>
<p>Breakeven ROAS = 1 ÷ gross margin. With a 40% gross margin, every dollar of ad spend needs $2.50 of revenue to pay for itself. In the table above, the third and fourth $5k blocks both fall below 2.5x.</p>
<div class="stat-row"><div><b>40%</b><span>gross margin</span></div><div><b>2.5x</b><span>breakeven ROAS</span></div><div><b>$10k</b><span>the spend level to stop at</span></div></div>

<h2 id="estimate" data-toc="Estimate it without a data team"><span class="num">03</span>Estimate it without a data team</h2>
<ul>
<li><strong>Step tests:</strong> change one campaign's budget by about 20% for two weeks and compare the extra revenue to the extra spend.</li>
<li><strong>Platform planners:</strong> Google Ads' budget simulators and Performance Planner estimate the curve for you. Treat them as a starting point, not gospel.</li>
<li><strong>Blended view:</strong> check total revenue against total spend (MER) so channels can't all claim the same sale.</li>
</ul>

<h2 id="the-rule" data-toc="The rule"><span class="num">04</span>The rule</h2>
<blockquote>Spend the next dollar where it earns the most, and stop when it earns less than it costs.<cite>— The whole strategy, really</cite></blockquote>
<p>Review it monthly. Curves shift with seasonality, creative fatigue and competition. If you want help building the model for your account, <a href="../../book/">book a free call</a>.</p>
'''),
]

def fmt_date(iso):
    return datetime.strptime(iso, '%Y-%m-%d').strftime('%-d %B %Y')

def post_card(P, p, cls='bcard paper reveal'):
    return f'''<a class="{cls}" href="{P}blog/{p["slug"]}/" data-post data-tags="{p["tagkey"]}" data-text="{E((p["title"] + " " + p["dek"] + " " + p["tag"]).lower())}" data-cursor="Read">
            <div class="post__cover">{cover_svg(p["seed"], uid="c")}</div>
            <div class="post__body"><div class="post__meta"><b>{E(p["tag"])}</b><span>{fmt_date(p["date"])} · {p["minutes"]} min</span></div><h3>{E(p["title"])}</h3><p class="post__ex">{E(p["dek"][:140].rsplit(" ", 1)[0])}…</p><span class="post__more">Read article →</span></div>
          </a>'''

def article_page(p, i, template=False):
    P = '../../'
    path = f'blog/{p["slug"]}/'
    prev_p = POSTS[i - 1] if i > 0 else None
    next_p = POSTS[i + 1] if i + 1 < len(POSTS) else None
    related = [q for q in POSTS if q is not p][:2]
    nav = ''
    if not template:
        nav = '<nav class="post-nav" aria-label="More articles">' + \
            (f'<a href="{P}blog/{prev_p["slug"]}/"><small>← Newer</small><strong>{E(prev_p["title"])}</strong></a>' if prev_p else '<span></span>') + \
            (f'<a href="{P}blog/{next_p["slug"]}/"><small>Older →</small><strong>{E(next_p["title"])}</strong></a>' if next_p else '<span></span>') + '</nav>'
    body = f'''    <article>
      <header class="phero phero--post" id="top">
        <div class="container">
          {crumbs_html(P, [("Home", ""), ("Blog", "blog/"), (p["tag"], "blog/")])}
          <div class="post-head">
            <p class="fade"><span class="chip chip--uv">{E(p["tag"])}</span></p>
            <h1 class="post-title fade" style="margin-top:18px">{E(p["title"])}</h1>
            <p class="dek fade">{E(p["dek"])}</p>
            <div class="post-meta fade">
              <div class="author"><img src="{P}assets/img/avatar.png" alt="" width="42" height="42"><div><strong>Manjil Shrestha</strong><small>Digital marketer · Melbourne</small></div></div>
              <div class="meta-bits"><time datetime="{p["date"]}">{fmt_date(p["date"])}</time><span>{p["minutes"]} min read</span></div>
              <div class="share" aria-label="Share"><a data-share="linkedin" target="_blank" rel="noopener" aria-label="Share on LinkedIn">in</a><a data-share="x" target="_blank" rel="noopener" aria-label="Share on X">X</a><button data-copy-link aria-label="Copy link">⧉</button></div>
            </div>
          </div>
        </div>
      </header>

      <div class="container">
        <figure>
          <div class="post-cover">{cover_svg(p["seed"], 1600, 610, uid="hero")}</div>
          <figcaption class="post-cover-cap">Cover · generated chart art. Replace with your own image if you like.</figcaption>
        </figure>
        <div class="post-layout">
          <aside class="toc" aria-label="On this page">
            <h4>On this page</h4>
            <ol id="toc"></ol>
            <div class="toc__progress"><span id="tocLeft">{p["minutes"]} min left</span><div class="toc__bar"><i id="tocBar"></i></div></div>
          </aside>
          <div>
            <details class="toc-mobile"><summary>On this page</summary><ol id="tocMobile"></ol></details>
            <div class="prose" data-minutes="{p["minutes"]}">
{p["body"]()}
            </div>
          </div>
        </div>

        <div class="post-end">
          <div class="post-tags"><span class="chip chip--uv">{E(p["tag"])}</span><span class="chip">Melbourne</span><span class="chip">Data-driven marketing</span></div>
          <div class="author-box">
            <img src="{P}assets/img/avatar.png" alt="Manjil Shrestha" width="76" height="76">
            <div><h3>Written by Manjil Shrestha</h3><p>Data-driven digital marketer in Melbourne, known online as mastha. I help small teams fix their tracking, then grow with SEO, paid media and CRO.</p>
            <div class="row"><a href="{P}services/">Services</a><a href="{P}book/">Book a free call</a><a href="https://www.linkedin.com/in/manjilshrestha" target="_blank" rel="noopener">LinkedIn ↗</a></div></div>
          </div>
          <div class="cta-band">
            <div><h2 style="font-size:clamp(1.5rem,3vw,2.2rem)">One email a month. <span class="goth glow">Zero</span> fluff.</h2><p>New articles and the occasional teardown, straight to your inbox.</p></div>
            <form class="newsletter js-form" data-subject="Newsletter signup" action="https://formspree.io/f/YOUR_FORM_ID" method="POST" novalidate style="margin-top:0">
              <label class="sr" style="position:absolute;left:-9999px" for="nl-{p["slug"]}">Email</label>
              <input id="nl-{p["slug"]}" type="email" name="email" required placeholder="you@company.com.au" autocomplete="email">
              <input type="text" name="_gotcha" tabindex="-1" autocomplete="off" class="hp" aria-hidden="true">
              <button class="btn btn--violet" type="submit"><span class="btn__text">Subscribe</span><span class="btn__sent">Subscribed ✓</span></button>
            </form>
          </div>
          {nav}
        </div>
      </div>
    </article>

    <section class="section section--tight">
      <div class="container">
        <div class="head head--row"><div><p class="label reveal">Keep reading</p><h2 class="h2 reveal">More from the <span class="goth glow">dashboard</span>.</h2></div><a href="{P}blog/" class="link reveal">All articles →</a></div>
        <div class="card-grid" style="grid-template-columns:repeat(auto-fit,minmax(280px,1fr))">
          {"".join(post_card(P, q) for q in related)}
        </div>
      </div>
    </section>'''
    import json
    ld = json.dumps({"@context": "https://schema.org", "@type": "BlogPosting", "headline": p["title"], "description": p["dek"], "datePublished": p["date"], "dateModified": p["date"],
                     "author": {"@type": "Person", "name": "Manjil Shrestha", "url": SITE}, "publisher": {"@type": "Person", "name": "Manjil Shrestha"},
                     "mainEntityOfPage": SITE + path, "image": SITE + "assets/img/og-image.png", "articleSection": p["tag"], "inLanguage": "en-AU"}, ensure_ascii=False)
    write(path + 'index.html', layout(P, path, f'{p["title"]} | mastha blog', p["dek"], 'blog', body, scripts=['blog.js'],
                                      ld=[ld, crumbs_ld([("Home", ""), ("Blog", "blog/"), (p["title"], path)])], og_type='article', noindex=template))

# ================================================================= TEMPLATE POST
TEMPLATE = dict(slug='_template', tag='Category', tagkey='analytics', date='2026-11-04', minutes=4, seed=7,
    title='Your article title goes here (keep it under 65 characters)',
    dek='The dek: one or two sentences that tell the reader what they will learn and why it matters. This also becomes the meta description.',
    body=lambda: '''
<!-- ============================================================
     BLOG POST TEMPLATE
     1. Copy this folder to /blog/your-slug/ and edit this file.
     2. Update <title>, meta description, canonical, og:url and the
        BlogPosting JSON-LD in <head> (search for "_template").
     3. Remove the noindex robots tag in <head>.
     4. Add a card for the post to /blog/index.html, a <url> to
        /sitemap.xml and an <item> to /blog/feed.xml.
     Every h2 needs an id. The table of contents builds itself.
     ============================================================ -->

<div class="tldr"><h4>TL;DR</h4><ul>
<li>Key takeaway one, in a single sentence.</li>
<li>Key takeaway two.</li>
<li>Key takeaway three. Readers who stop here should still get value.</li></ul></div>

<p>Intro paragraph. Hook the reader with the problem in two or three sentences. Say who this is for.</p>

<h2 id="section-one" data-toc="Short TOC label"><span class="num">01</span>A section heading</h2>
<p>Body text. Keep paragraphs short. Use <strong>bold</strong> for the one phrase you want skimmers to catch, and <a href="#">links</a> to related posts or services.</p>
<p class="has-note">A paragraph with a hidden margin note. The note only appears under the UV torch. <span class="note uv note--margin" data-note><span>a hidden aside, in handwriting.</span></span></p>

<h2 id="section-two"><span class="num">02</span>Components you can use</h2>
<div class="callout"><span class="callout__i">✦</span><p><strong>Tip callout:</strong> for a practical tip or quick test.</p></div>
<div class="callout callout--warn"><span class="callout__i">!</span><p><strong>Warning callout:</strong> for a common mistake.</p></div>
<div class="stat-row"><div><b>42%</b><span>a headline number</span></div><div><b>3x</b><span>another number</span></div><div><b>14 d</b><span>a third number</span></div></div>
<blockquote>A pull quote that sums up the argument.<cite>— Source or your name</cite></blockquote>
<pre><code><span class="c">// code block</span>
<span class="k">const</span> roas = revenue / spend;</code></pre>
<div class="table-wrap"><table><thead><tr><th>Column</th><th>Column</th><th>Column</th></tr></thead><tbody><tr><td>Row</td><td>Value</td><td>Value</td></tr><tr><td>Row</td><td>Value</td><td>Value</td></tr></tbody></table></div>
<ul class="checklist"><li><label><input type="checkbox"><span>An interactive checklist item</span></label></li><li><label><input type="checkbox"><span>Another one</span></label></li></ul>

<h2 id="wrap-up"><span class="num">03</span>Wrap-up and next step</h2>
<p>Summarise, then give one clear next step, such as booking a call or reading a related post.</p>
''')

# ================================================================= BLOG INDEX
SOON = [
    dict(tag='CRO', tagkey='cro', title='The pricing page test that more than doubled trials', dek='What we changed, what we expected, and the result nobody predicted.'),
    dict(tag='Email', tagkey='email', title='Five Klaviyo flows every Shopify store needs', dek='The automations that quietly earn while you sleep, in order of priority.'),
]

def blog_index():
    P = '../'
    feat = POSTS[0]
    soon_cards = ''.join(f'''<div class="bcard paper post--soon reveal" data-post data-tags="{s["tagkey"]}" data-text="{E((s["title"] + " " + s["dek"]).lower())}" aria-disabled="true">
            <div class="bcard__cover">{cover_svg(10 + j, uid="s")}<span class="bcard__tag">{E(s["tag"])}</span></div>
            <div class="bcard__body"><p class="bcard__meta">Coming soon</p><h3>{E(s["title"])}</h3><p>{E(s["dek"])}</p><span class="bcard__more">In the works <b aria-hidden="true">…</b></span></div>
          </div>''' for j, s in enumerate(SOON))
    counts = {}
    for p in POSTS: counts[p['tagkey']] = counts.get(p['tagkey'], 0) + 1
    body = f'''    <section class="phero" id="top">
      <div class="container">
        {crumbs_html(P, [("Home", ""), ("Blog", "blog/")])}
        <div class="phero__grid">
          <div>
            <p class="label fade">Blog · Notes from the dashboard</p>
            <h1 class="phero__title" aria-label="Notes from the dashboard">
{phero_title([("Notes from", False), ("the", False), ("dashboard.", True)])}
            </h1>
            <p class="phero__lead fade">Field notes on analytics, SEO, paid media and CRO for Melbourne businesses. No fluff, just what moved the numbers and how to do it yourself.</p>
            <form class="newsletter js-form fade" data-subject="Newsletter signup" action="https://formspree.io/f/YOUR_FORM_ID" method="POST" novalidate>
              <label for="nl-top" style="position:absolute;left:-9999px">Email</label>
              <input id="nl-top" type="email" name="email" required placeholder="you@company.com.au" autocomplete="email">
              <input type="text" name="_gotcha" tabindex="-1" autocomplete="off" class="hp" aria-hidden="true">
              <button class="btn btn--violet" type="submit" data-magnetic><span class="btn__text">Get new posts</span><span class="btn__sent">Subscribed ✓</span></button>
            </form>
            <p class="mono muted small" style="margin-top:10px">One email a month · unsubscribe any time · <a class="link" href="feed.xml">RSS</a></p>
          </div>
        </div>
        <div class="note uv" data-note style="--nx:58%;--ny:58%;--rot:-5deg"><span>the newsletter is one email a month.<br>pinky promise.</span></div>
      </div>
      <div class="phero__ink uv" aria-hidden="true">read me</div>
    </section>

    <section class="section section--tight" id="articles" style="padding-top:0">
      <div class="container">
        <div class="blog-tools">
          <div class="filters" role="group" aria-label="Filter by topic">
            <button class="filter is-on" data-filter="all">All</button>
            <button class="filter" data-filter="analytics">Analytics</button>
            <button class="filter" data-filter="local-seo">Local SEO</button>
            <button class="filter" data-filter="paid-media">Paid Media</button>
            <button class="filter" data-filter="cro">CRO</button>
            <button class="filter" data-filter="email">Email</button>
          </div>
          <label class="search"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="7" cy="7" r="5"/><path d="M11 11l3.5 3.5"/></svg><input type="search" id="postSearch" placeholder="Search articles" aria-label="Search articles"><span class="mono small" id="postCount"></span></label>
        </div>

        <a class="feature reveal" href="{feat["slug"]}/" data-post data-tags="{feat["tagkey"]}" data-text="{E((feat["title"] + " " + feat["dek"]).lower())}" data-cursor="Read" style="position:relative">
          <div class="feature__cover">{cover_svg(feat["seed"], 640, 420, uid="f")}</div>
          <div class="feature__body">
            <p><span class="chip chip--uv">Featured</span> <span class="chip">{E(feat["tag"])}</span></p>
            <h2>{E(feat["title"])}</h2>
            <p>{E(feat["dek"])}</p>
            <div class="byline"><img src="{P}assets/img/avatar.png" alt="" width="26" height="26"><span>Manjil Shrestha · {fmt_date(feat["date"])} · {feat["minutes"]} min read</span></div>
            <span class="bcard__more">Read the article <b aria-hidden="true">→</b></span>
          </div>
          <div class="note uv" data-note style="--nx:4%;--ny:-7%;--rot:-4deg"><span>start with this one. it saves the most money.</span></div>
        </a>

        <div class="card-grid">
          {"".join(post_card(P, p) for p in POSTS[1:])}
          {soon_cards}
        </div>
        <p class="empty" id="emptyState">Nothing matches that yet. Try another topic, or <a class="link" href="{P}contact/">suggest an article</a>.</p>
      </div>
    </section>

    <section class="section section--tight">
      <div class="container">
        <div class="head"><p class="label reveal">Browse by topic</p><h2 class="h2 reveal">Pick your <span class="goth glow">rabbit hole</span>.</h2></div>
        <div class="topics">
          <button class="topic reveal" data-topic="analytics"><h3>Analytics</h3><p>GA4, tracking, attribution and dashboards.</p><small>{counts.get("analytics", 0)} article · more soon</small></button>
          <button class="topic reveal" data-topic="local-seo"><h3>Local SEO</h3><p>Ranking in Melbourne suburbs and the map pack.</p><small>{counts.get("local-seo", 0)} article</small></button>
          <button class="topic reveal" data-topic="paid-media"><h3>Paid Media</h3><p>Google and Meta, budgets and creative.</p><small>{counts.get("paid-media", 0)} article</small></button>
          <button class="topic reveal" data-topic="cro"><h3>CRO</h3><p>Tests, landing pages and funnels.</p><small>Coming soon</small></button>
        </div>
      </div>
    </section>

    <section class="section section--tight">
      <div class="container">
        <div class="cta-band reveal">
          <div><h2>Rather have me <span class="goth glow">look</span> at your numbers?</h2><p>Reading is good. A free 30-minute call with your actual data is faster.</p></div>
          <div class="cta-band__actions"><a href="{P}book/" class="btn btn--violet btn--lg" data-magnetic>Book a free consultation →</a></div>
        </div>
      </div>
    </section>'''
    import json
    ld = json.dumps({"@context": "https://schema.org", "@type": "Blog", "name": "mastha — Notes from the dashboard", "url": SITE + "blog/", "author": {"@type": "Person", "name": "Manjil Shrestha"},
                     "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "url": SITE + f'blog/{p["slug"]}/', "datePublished": p["date"]} for p in POSTS]}, ensure_ascii=False)
    write('blog/index.html', layout(P, 'blog/', 'Digital Marketing Blog | Analytics, SEO & Ads Tips from Melbourne | mastha',
                                    'Practical articles on GA4, local SEO, paid media and CRO from Manjil Shrestha, a data-driven digital marketing expert in Melbourne.',
                                    'blog', body, scripts=['blog.js'], ld=[ld, crumbs_ld([("Home", ""), ("Blog", "blog/")])]))

def feed():
    items = ''.join(f'''
    <item>
      <title>{E(p["title"])}</title>
      <link>{SITE}blog/{p["slug"]}/</link>
      <guid isPermaLink="true">{SITE}blog/{p["slug"]}/</guid>
      <pubDate>{datetime.strptime(p["date"], "%Y-%m-%d").strftime("%a, %d %b %Y")} 09:00:00 +1000</pubDate>
      <category>{E(p["tag"])}</category>
      <description>{E(p["dek"])}</description>
    </item>''' for p in POSTS)
    write('blog/feed.xml', f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>mastha — Notes from the dashboard</title>
    <link>{SITE}blog/</link>
    <atom:link href="{SITE}blog/feed.xml" rel="self" type="application/rss+xml"/>
    <description>Analytics, SEO, paid media and CRO notes from Manjil Shrestha, a digital marketing expert in Melbourne.</description>
    <language>en-au</language>{items}
  </channel>
</rss>
''')

def sitemap():
    urls = [('', '1.0', '2026-11-04'), ('services/', '0.9', '2026-11-04'), ('services/seo/', '0.9', '2026-11-05'),('book/', '0.8', '2026-11-04'), ('contact/', '0.7', '2026-11-04'), ('blog/', '0.8', POSTS[0]['date'])] + \
           [(f'blog/{p["slug"]}/', '0.7', p['date']) for p in POSTS]
    body = ''.join(f'\n  <url>\n    <loc>{SITE}{u}</loc>\n    <lastmod>{d}</lastmod>\n    <priority>{pr}</priority>\n  </url>' for u, pr, d in urls)
    write('sitemap.xml', f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{body}\n</urlset>\n')

exec(open(SC + 'service_seo.py').read())
exec(open(SC + 'red_parts.py').read())   # red paper design overrides
services_page(); seo_service_page(); book_page(); contact_page(); blog_index()
for i, p in enumerate(POSTS):
    article_page(p, i)
article_page(TEMPLATE, 0, template=True)
feed(); sitemap()
