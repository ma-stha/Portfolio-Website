"""Builds the "LOUD" design (bold, full-bleed red/black, kinetic) into /loud/.

Run:  python3 tools/build_loud.py

Reuses the content and inner-page structure from tools/build_studio.py and
swaps the chrome, page heroes, section heads, posters and the whole home page.
Content still comes from js/content.js and tools/build_pages.py.
"""
import os, re, sys, json, shutil, math

TOOLS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TOOLS)
import build_studio as B   # noqa: E402  (loads shared content on import)

ROOT = B.ROOT
OUT = os.path.join(ROOT, 'loud')
B.OUT = OUT
E, S, SITE = B.E, B.S, B.SITE
RED, INK, PAPER = '#F83232', '#0A0A0A', '#F2EFE9'
DISPLAY = "Big Shoulders Display, Impact, sans-serif"
ARR = B.ARR

_write = B.write
def write(rel, text):
    full = os.path.join(OUT, rel); os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w').write(text); print('wrote loud/' + rel)
B.write = write

# ------------------------------------------------------------------ posters
def poster(seed, big, small, variant=0, W=600, H=400):
    bg, fg, ln = [(RED, INK, INK), (INK, RED, PAPER), (PAPER, INK, RED)][variant % 3]
    rnd = lambda n: (lambda x: x - math.floor(x))(math.sin(seed * 91 + n * 5.7) * 9999)
    s = [8 + i * 1.8 + rnd(i) * 7 for i in range(14)]
    p = [(x, y * .5 + H * .06) for x, y in B.scale(s, W, H, 0, 40)]
    fs = int(H * (0.78 if len(big) <= 4 else 0.6 if len(big) <= 6 else 0.46))
    bars = ''.join(f'<rect x="{x - W / 60:.0f}" y="{y + 10:.0f}" width="{W / 30:.0f}" height="{H - y:.0f}" fill="{ln}" opacity=".12"/>' for x, y in p)
    return (f'<svg viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><rect width="{W}" height="{H}" fill="{bg}"/>{bars}'
            f'<path d="{B.smooth(p)}" fill="none" stroke="{ln}" stroke-width="{max(3, W / 160):.0f}"/><circle cx="{p[-1][0] - 6:.0f}" cy="{p[-1][1]:.0f}" r="{max(8, W / 60):.0f}" fill="{ln}"/>'
            f'<text x="{W * .04:.0f}" y="{H * .1:.0f}" font-family="Martian Mono, monospace" font-size="{max(12, W / 40):.0f}" fill="{fg}">{E(small.upper())}</text>'
            f'<text x="{W * .02:.0f}" y="{H * .96:.0f}" font-family="{DISPLAY}" font-weight="900" font-size="{fs}" letter-spacing="-2" fill="{fg}">{E(big.upper())}</text></svg>')
B.poster = poster

# ------------------------------------------------------------------ heads, heroes, cta
def sec_head(no, label, title, aside=''):
    return (f'<header class="sh"><p class="sh__no">{no:02d}</p><p class="sh__label">{label}</p>'
            f'<h2 class="sh__title rv">{title}</h2>{f"<div class=sh__aside>{aside}</div>" if aside else ""}</header>')
B.sec_head = sec_head

def phero(P, trail, meta, title, lead, actions='', aside=''):
    words = title.rstrip('.').split(' ')
    lines, cur = [], ''
    for w in words:
        if len(cur) + len(w) > 14 and cur:
            lines.append(cur.strip()); cur = ''
        cur += w + ' '
    lines.append(cur.strip())
    t = ''.join(f'<span class="ln"><span>{E(l)}{"." if i == len(lines) - 1 and title.endswith(".") else ""}</span></span>' for i, l in enumerate(lines))
    meta_html = ''.join(f'<li>{m}</li>' for m in meta)
    return f'''    <section class="ph" id="top" data-theme="red">
      <div class="wrap">
        {B.crumbs(P, trail)}
        <h1 class="ph__title" aria-label="{E(title)}">{t}</h1>
        <div class="ph__grid">
          <ul class="ph__meta in">{meta_html}</ul>
          <div class="ph__main"><p class="ph__lead in">{lead}</p>{f'<div class="actions in">{actions}</div>' if actions else ''}</div>
          {f'<div class="ph__aside in">{aside}</div>' if aside else ''}
        </div>
      </div>
    </section>'''
B.phero = phero

def cta(P, line='Have a number you want to move?', sub='A free 30-minute call with your real data. You will leave with the three things I would do first.'):
    return f'''    <section class="cta" data-theme="dark">
      <div class="wrap cta__grid">
        <p class="cta__line">{E(line)}</p>
        <div class="cta__side"><p>{sub}</p><a class="btn btn--red" href="{P}book/">Book a free consultation {ARR}</a></div>
      </div>
    </section>'''
B.cta = cta

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
  <meta name="theme-color" content="#F83232">
  <link rel="canonical" href="{SITE}{path}">
  <link rel="icon" type="image/svg+xml" href="{P}assets/favicon.svg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@400..900&family=Instrument+Sans:ital,wdth,wght@0,75..100,400..700;1,75..100,400..700&family=Martian+Mono:wdth,wght@75..112.5,300..700&family=Newsreader:ital,opsz,wght@0,6..72,300..500;1,6..72,300..500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{P}css/loud.css">{lds}
</head>
<body class="no-js">
  <script>document.body.classList.replace('no-js','js');</script>
  <svg width="0" height="0" style="position:absolute" aria-hidden="true">{B.SYMBOLS}</svg>
  <a class="skip" href="#main">Skip to content</a>
  <div class="cursor" id="cursor" aria-hidden="true"><span id="cursorLabel"></span></div>
  <div class="gridlines" aria-hidden="true"><div class="wrap"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div></div>
  <div class="preview" id="preview" aria-hidden="true"></div>
  <div class="toast" id="toast" role="status" aria-live="polite"></div>

  <header class="hd" id="nav">
    <div class="wrap hd__in">
      <a class="hd__brand" href="{P}" aria-label="Manjil Shrestha, home"><svg viewBox="0 0 1463 317"><use href="#logo"/></svg></a>
      <nav class="hd__nav" aria-label="Primary">{nav}</nav>
      <p class="hd__time"><span class="avail"><i></i>Open for work</span> <span class="hd__clock">MEL <span data-mel-clock>--:--</span></span></p>
      <a class="hd__cta" href="{P}book/">Book a call</a>
      <button class="hd__menu" id="burger" aria-label="Open menu" aria-expanded="false" aria-controls="menu">Menu</button>
    </div>
  </header>
  <div class="menu" id="menu" aria-hidden="true">
    <div class="wrap menu__in"><nav class="menu__links">{menu}</nav><div class="menu__foot"><a href="#" data-copy-email data-email-text>hello@</a><div data-socials class="menu__soc"></div></div></div>
  </div>

  <main id="main">
{body}
  </main>

  <footer class="ft" data-theme="dark">
    <div class="wrap">
      <div class="ft__grid">
        <div class="ft__col ft__col--lead"><p class="ft__big">Digital marketing expert in Melbourne. Born in Kathmandu, obsessed with numbers, allergic to vanity metrics.</p><a class="btn btn--red" href="{P}book/">Book a free consultation {ARR}</a></div>
        <div class="ft__col"><h4>Site</h4><a href="{P}">Home</a><a href="{P}services/">Services</a><a href="{P}services/seo/">SEO in Melbourne</a><a href="{P}blog/">Journal</a></div>
        <div class="ft__col"><h4>Contact</h4><a href="#" data-copy-email data-email-text>hello@</a><a href="{P}book/">Book a call</a><a href="{P}contact/">Contact page</a></div>
        <div class="ft__col"><h4>Elsewhere</h4><div data-socials class="ft__soc"></div></div>
      </div>
      <p class="ft__name" data-fit aria-hidden="true">MASTHA<span>✱</span></p>
      <div class="ft__bar"><span>© <span data-year>2026</span> Manjil Shrestha</span><span>Kathmandu → Melbourne, 9,572 km</span><button type="button" class="ft__grid-toggle" id="gridToggle">Show grid (G)</button><a href="#top">Back to top ↑</a></div>
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
B.layout = layout

# ================================================================== HOME
def route_svg():
    return '''<svg class="route" viewBox="0 0 600 260" aria-hidden="true">
      <path id="rt" d="M90 70 C 220 -10, 420 40, 510 200" class="route__path"/>
      <circle cx="90" cy="70" r="9" class="route__a"/><circle cx="510" cy="200" r="12" class="route__b"/>
      <circle r="7" class="route__dot"><animateMotion dur="4s" repeatCount="indefinite" rotate="auto"><mpath href="#rt"/></animateMotion></circle>
      <text x="40" y="112" class="route__t">KATHMANDU</text><text x="40" y="130" class="route__s">27.72° N · where it started</text>
      <text x="380" y="240" class="route__t">MELBOURNE</text><text x="380" y="256" class="route__s">37.81° S · where it grows</text>
    </svg>'''

def home():
    P = ''
    cases = S['caseStudies']
    letters = ''.join(f'<span class="nb" style="--i:{i};--h:{b}" data-base="{b}"><span class="nb__l">{c}</span></span>' for i, (c, b) in enumerate(zip('MANJIL', [.46, .56, .64, .74, .86, 1])))
    panels = ''.join(f'''<article class="res res--{i % 4}">
            <p class="res__k">Case {i + 1:02d} / {c["industry"]} / {c["year"]}</p>
            <p class="res__big">{B.kfmt(c["kpis"][0])}</p>
            <p class="res__unit">{E(c["kpis"][0]["label"])}</p>
            <div class="res__body"><h3>{E(c["title"])}</h3><p>{E(c["result"])}</p>
              <ul class="res__kpis">{"".join(f"<li><b>{B.kfmt(k)}</b>{E(k['label'])}</li>" for k in c["kpis"][1:])}</ul></div>
          </article>''' for i, c in enumerate(cases))
    rows = ''.join(f'''<li class="srow" style="--d:{(-1) ** i}"><a href="services/#{s["id"]}" data-cursor="Explore">
            <span class="srow__n">{i + 1:02d}</span><span class="srow__w">{E(s["title"].replace(" & ", " + ").upper())}</span>
            <span class="srow__d">{E(s["short"])}<b>{ARR}</b></span></a></li>''' for i, s in enumerate(B.SERVICES))
    steps = ''.join(f'''<article class="mt mt--{i % 3}" style="--i:{i}">
            <p class="mt__n">{i + 1:02d}</p><div><h3>{E(p["title"])}</h3><p>{E(p["text"])}</p></div></article>''' for i, p in enumerate(S['process']))
    figs = ''.join(f'<li><b><span data-count="{n["value"]}" data-decimals="{n.get("decimals", 0)}">0</span>{E(n.get("suffix", ""))}</b>{E(n["label"])}</li>' for n in S['numbers'])
    cv = ''.join(f'<li class="sb rv"><span class="sb__yr">{E(e["period"])}</span><span class="sb__role">{E(e["role"])}</span><span class="sb__org">{E(e["org"])}</span><span class="sb__txt">{E(e["text"])}</span></li>' for e in S['experience'])
    certs = ' · '.join(E(c) for c in S['certifications'])
    edu = ' · '.join(f'{E(e["title"])}, {E(e["org"])}' for e in S['education'])
    quotes = ''.join(f'<figure class="qt__item{" is-on" if i == 0 else ""}"><blockquote>{E(t["quote"])}</blockquote><figcaption>{E(t["name"])}, {E(t["org"])} (demo)</figcaption></figure>' for i, t in enumerate(S['testimonials']))
    calc = S['calculator']
    fq = [(f['q'], f['a']) for f in S['faq']]
    body = f'''    <section class="hero" id="top" data-theme="red">
      <div class="wrap hero__in">
        <div class="hero__top in"><p>Manjil Shrestha<br><span>a.k.a. mastha</span></p><p>Independent<br><span>since 2020</span></p><p>SEO, paid, analytics, CRO<br><span>judged on revenue</span></p><p class="hero__live"><i></i>Taking 2 new clients<br><span>this quarter</span></p></div>
        <div class="namechart" id="namechart" aria-hidden="true">
          {letters}
          <svg class="namechart__line" id="ncLine" preserveAspectRatio="none"><polyline id="ncPoly" points=""/><circle id="ncDot" r="10"/></svg>
          <span class="namechart__tag" id="ncTag">▲ +212%</span>
        </div>
        <div class="hero__foot">
          <h1 class="hero__h1"><span class="ln"><span>Digital marketing</span></span><span class="ln"><span>expert in Melbourne.</span></span></h1>
          <div class="hero__cta in"><p>I make the numbers go up, and I can prove it. Search, paid media and analytics for businesses that are done guessing.</p><a class="btn btn--ink" href="book/">Book a free consultation {ARR}</a></div>
        </div>
      </div>
    </section>

    <section class="kin" id="manifesto" data-theme="dark" aria-label="Manifesto">
      <div class="kin__pin">
        <div class="wrap kin__in">
          <p class="kin__l">Most marketing is</p>
          <p class="kin__w kin__w--old"><span>guesswork</span><i class="kin__strike"></i></p>
          <p class="kin__l kin__l--2">Mine is</p>
          <p class="kin__w kin__w--new">measured<span>.</span></p>
          <p class="kin__note">Tracking first. Campaigns second. Scale only what the numbers prove.</p>
        </div>
      </div>
    </section>

    <section class="results" id="work" data-theme="light">
      <div class="results__pin">
        <div class="results__head wrap"><p class="sh__no">02</p><h2 class="results__title">Receipts<span>.</span></h2><p class="results__hint">Four engagements. Scroll →</p></div>
        <div class="results__track" id="resTrack">{panels}
          <a class="res res--end" href="book/" data-cursor="Let's go"><p class="res__k">Case 05 / your business / 2027</p><p class="res__big">YOU?</p><p class="res__unit">Book a free call {ARR}</p></a>
        </div>
      </div>
    </section>

    <section class="svcs" id="services" data-theme="light">
      <div class="wrap">{sec_head(3, "What I do", "Six ways to make the line go up.", '<a class="tlink" href="services/">Services and pricing</a>')}</div>
      <ol class="svcs__rows">{rows}</ol>
    </section>

    <section class="about" id="about" data-theme="dark">
      <div class="wrap about__grid">
        <figure class="about__img rv"><img src="assets/img/portrait.jpg" alt="Portrait of Manjil Shrestha" width="1000" height="1371"><figcaption>MANJIL SHRESTHA, MELBOURNE</figcaption></figure>
        <div class="about__txt">
          <p class="sh__no">04</p>
          <h2 class="about__title rv">From Kathmandu to Melbourne, one spreadsheet at a time.</h2>
          <p class="about__p rv">I started in content in Nepal and kept asking one annoying question: what did it actually do? That question followed me 9,572 km to Melbourne and turned into a method. Today I build the tracking, campaigns and experiments that show exactly where revenue comes from, and where it leaks.</p>
          {route_svg()}
          <ul class="about__figs">{figs}</ul>
        </div>
      </div>
    </section>

    <section class="method" id="process" data-theme="light">
      <div class="wrap">{sec_head(5, "The method", "A loop, not a launch.")}</div>
      <div class="wrap method__stack">{steps}</div>
    </section>

    <section class="sec sec--ink" id="lab" data-theme="dark">
      <div class="wrap">
        {sec_head(6, "Growth model", "What's a better funnel worth?", '<p>The back-of-envelope maths I run before every CRO engagement. Illustrative only.</p>')}
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

    <section class="sec" id="experience" data-theme="light">
      <div class="wrap">
        {sec_head(7, "Track record", "Where the data habit came from.", '<a class="tlink" href="assets/Manjil-Shrestha-CV.pdf">Download CV</a>')}
        <ol class="board">{cv}</ol>
        <p class="board__extra rv"><b>Education</b> {edu}<br><b>Certified</b> {certs}</p>
      </div>
    </section>

    <section class="qt" data-theme="red" aria-label="Testimonials">
      <div class="wrap">
        <p class="qt__mark" aria-hidden="true">“</p>
        <div class="qt__stage">{quotes}</div>
        <div class="qt__nav"><button type="button" id="qPrev" aria-label="Previous quote">←</button><span id="qCount">1 / {len(S["testimonials"])}</span><button type="button" id="qNext" aria-label="Next quote">→</button></div>
      </div>
    </section>

    <section class="sec" id="journal" data-theme="light">
      <div class="wrap">
        {sec_head(8, "Journal", "Notes from the dashboard.", '<a class="tlink" href="blog/">All articles</a>')}
        {B.journal_rows(P, B.POSTS)}
      </div>
    </section>

    <section class="sec" id="faq" data-theme="light">
      <div class="wrap faq">
        {sec_head(9, "FAQ", "Before we start.")}
        {B.faq(fq)}
      </div>
    </section>

    <section class="contact" id="contact" data-theme="dark">
      <div class="wrap">
        <p class="contact__big"><span class="ln"><span>Let's talk</span></span><span class="ln"><span>numbers<b>.</b></span></span></p>
        <div class="contact__grid">
          <div class="contact__info">
            <p>Tell me what you're trying to grow. I reply within one business day with an honest take on whether I can help.</p>
            <button type="button" class="contact__email" data-copy-email><span data-email-text>hello@</span><small>Copy</small></button>
            <dl class="contact__dl"><div><dt>Based</dt><dd>Melbourne, Australia</dd></div><div><dt>Status</dt><dd data-availability>Available</dd></div><div><dt>Elsewhere</dt><dd data-socials class="contact__soc"></dd></div></dl>
          </div>
          {B.contact_form("Project enquiry")}
        </div>
      </div>
    </section>'''
    person = json.dumps({"@context": "https://schema.org", "@type": "Person", "name": "Manjil Shrestha", "alternateName": "mastha", "jobTitle": "Digital Marketing Expert", "address": {"@type": "PostalAddress", "addressLocality": "Melbourne", "addressCountry": "AU"}, "url": SITE}, ensure_ascii=False)
    write('index.html', layout(P, '', 'Digital Marketing Expert in Melbourne | Manjil Shrestha', 'Manjil Shrestha (mastha) is a bold, data-driven digital marketing expert in Melbourne. SEO, paid media, analytics and CRO, judged on revenue.', 'home', body, ['home.js'], [person, B.faq_ld(fq)]))

# ================================================================== assets + run
def copy_assets():
    for rel in ['js/content.js', 'js/book.js', 'js/blog.js', 'js/pages.js', 'js/vendor/gsap.min.js', 'js/vendor/ScrollTrigger.min.js', 'js/vendor/lenis.min.js', 'js/vendor/LICENSE-lenis.txt', 'assets/img/portrait.jpg', 'assets/img/avatar.png']:
        dst = os.path.join(OUT, rel); os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copyfile(os.path.join(ROOT, rel), dst)
    star = re.search(r'<symbol id="star" viewBox="0 0 100 100"><path fill="currentColor" d="([^"]+)"', B.SYMBOLS).group(1)
    open(os.path.join(OUT, 'assets/favicon.svg'), 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" fill="{INK}"/><g transform="translate(8 8) scale(.48)"><path fill="{RED}" d="{star}"/></g></svg>\n')

if __name__ == '__main__':
    copy_assets()
    home(); B.services(); B.seo(); B.book(); B.contact(); B.blog_index()
    for i, p in enumerate(B.POSTS):
        B.article(p, i)
    B.article(B.TEMPLATE, 0, template=True)
