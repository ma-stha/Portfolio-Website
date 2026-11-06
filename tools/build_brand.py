"""Builds the "Living Mark" design (creative branding, red-led) into /brand/.

Run:  python3 tools/build_brand.py

Positioning: Manjil Shrestha, branding expert in Australia (brand + marketing).
All copy for this design lives in this file (BRAND content below), so it can
diverge from the data-led main site. Shared helpers (FAQ, crumbs, dates,
logo symbol) come from tools/build_studio.py.
Rules for extending it: brand/DESIGN-BLUEPRINT.md
"""
import os, re, sys, json, shutil, math, html

TOOLS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TOOLS)
import build_studio as B   # noqa: E402  (helpers only)

ROOT = B.ROOT
OUT = os.path.join(ROOT, 'brand')
E = html.escape
SITE = B.SITE
RED, INK, PAPER, BLUSH = '#F83232', '#161211', '#F4EEE6', '#F9D8D1'
ARR = '<span class="arr" aria-hidden="true">→</span>'
NE = '<span class="arr" aria-hidden="true">↗</span>'
DEMO = '<span class="demo">demo</span>'

def write(rel, text):
    full = os.path.join(OUT, rel); os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w').write(text); print('wrote brand/' + rel)

def strip(s):
    return re.sub(r'<[^>]+>', '', s)

# ====================================================================== GLYPHS
# The icon set. Twelve geometric marks on a 100 x 100 grid. They are the
# brand's second alphabet: section markers, bullets, service icons, patterns,
# cursor, favicon, case-study marks and the brand builder all use them.
def _sun():
    rays = []
    for k in range(8):
        a = k * math.pi / 4; c, s = math.cos(a), math.sin(a); w = 5.5
        p = [(50 + c * 31 - s * w, 50 + s * 31 + c * w), (50 + c * 48 - s * w, 50 + s * 48 + c * w), (50 + c * 48 + s * w, 50 + s * 48 - c * w), (50 + c * 31 + s * w, 50 + s * 31 - c * w)]
        rays.append('M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in p) + 'Z')
    return 'M50 27a23 23 0 1 0 .01 0Z ' + ' '.join(rays)

def _wave():
    out = []
    for base in (30, 66):
        top = [(x, base - 9 + 9 * math.sin(x / 100 * 2 * math.pi * 1.5)) for x in range(2, 99, 4)]
        bot = [(x, y + 16) for x, y in reversed(top)]
        out.append('M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in top + bot) + 'Z')
    return ' '.join(out)

STAR = re.search(r'<symbol id="star" viewBox="0 0 100 100"><path fill="currentColor" d="([^"]+)"', B.SYMBOLS).group(1)
GLYPHS = {
    'star': (STAR, 'Signature'),
    'spark': ('M50 2C54 36 64 46 98 50C64 54 54 64 50 98C46 64 36 54 2 50C36 46 46 36 50 2Z', 'Idea'),
    'bloom': ('M50 2a24 24 0 1 0 .01 0Z M74 26a24 24 0 1 0 .01 0Z M50 50a24 24 0 1 0 .01 0Z M26 26a24 24 0 1 0 .01 0Z M50 30a20 20 0 1 0 .01 0Z', 'Joy'),
    'arch': ('M8 98V50a42 42 0 0 1 84 0v48H68V50a18 18 0 0 0-36 0v48Z', 'Home'),
    'eye': ('M2 50Q50-4 98 50Q50 104 2 50Z M50 31a19 19 0 1 0 .01 0Z M50 41a9 9 0 1 0 .01 0Z', 'Vision'),
    'sun': (_sun(), 'Warmth'),
    'bubble': ('M6 8h88v60H46L20 94V68H6Z', 'Voice'),
    'heart': ('M50 92L11 53A22 22 0 0 1 50 20A22 22 0 0 1 89 53Z', 'Love'),
    'crown': ('M5 84L13 24L34 52L50 12L66 52L87 24L95 84Z', 'Premium'),
    'wave': (_wave(), 'Flow'),
    'quarter': ('M2 2H50A48 48 0 0 1 2 50Z M98 98H50A48 48 0 0 1 98 50Z M74 10a16 16 0 1 0 .01 0Z M8 66h26v26H8Z', 'Craft'),
    'target': ('M50 2a48 48 0 1 0 .01 0Z M50 17a33 33 0 1 0 .01 0Z M50 33a17 17 0 1 0 .01 0Z', 'Focus'),
}
EVENODD = {'eye', 'target'}
G_SPRITE = ''.join(f'<symbol id="g-{k}" viewBox="0 0 100 100"><path fill="currentColor"{" fill-rule=evenodd" if k in EVENODD else ""} d="{d}"/></symbol>' for k, (d, _) in GLYPHS.items())

def G(name, cls=''):
    return f'<svg class="g g--{name}{" " + cls if cls else ""}" viewBox="0 0 100 100" aria-hidden="true"><use href="#g-{name}"/></svg>'

def gpath(name, x, y, size, fill, rot=0):
    d, _ = GLYPHS[name]; s = size / 100
    fr = ' fill-rule="evenodd"' if name in EVENODD else ''
    return f'<path transform="translate({x:.1f} {y:.1f}) rotate({rot} {size / 2:.1f} {size / 2:.1f}) scale({s:.4f})" fill="{fill}"{fr} d="{d}"/>'

# ====================================================================== BRAND CONTENT
FONTS = {   # personality -> SVG/CSS text style
    'bold': ("Bricolage Grotesque", 800, True, "font-stretch:75%;letter-spacing:-.02em"),
    'warm': ("Fraunces", 600, False, "font-variation-settings:'SOFT' 100,'WONK' 0;letter-spacing:-.02em"),
    'premium': ("Fraunces", 300, True, "font-variation-settings:'SOFT' 0;letter-spacing:.16em"),
    'playful': ("Fraunces", 800, False, "font-variation-settings:'SOFT' 100,'WONK' 1;letter-spacing:-.03em"),
    'calm': ("Bricolage Grotesque", 400, False, "letter-spacing:.01em"),
}

WORK = [   # DEMO clients. Replace with real projects before launch.
    dict(slug='saltbush', name='Saltbush Coffee', place='Melbourne, VIC', sector='Specialty coffee roaster', year='2025', glyph='sun', font='warm',
         c1='#E8553D', c2='#F6C9A8', ink='#2A1A14', paper='#FBF3EA', props='cup', tagline='Roasted under a big sky.',
         services=['Strategy', 'Identity', 'Packaging'],
         challenge='A brilliant roaster with a forgettable label, lost on crowded café shelves and supermarket end caps.',
         idea='The sun that dries the saltbush plains became a mark that stamps cups, bags and shopfronts. Warm, hand-made and unmistakably Australian, without a single kangaroo.',
         results=[('3', 'new wholesale cafés in month one'), ('+41%', 'online bag sales'), ('#1', 'most-tagged café cup in Collingwood')]),
    dict(slug='little-creek', name='Little Creek Wines', place='Yarra Valley, VIC', sector='Boutique winery', year='2025', glyph='wave', font='premium',
         c1='#7A1F1F', c2='#E9DCC9', ink='#1C1212', paper='#F6F0E6', props='bag', tagline='Small creek. Serious wine.',
         services=['Naming', 'Identity', 'Labels'],
         challenge='Award-winning wine hiding behind a label that looked like every other bottle on the shelf.',
         idea='A single line for the creek that runs through the vineyard, drawn once and used everywhere: labels, cellar door signage, wax seals and the tasting menu.',
         results=[('2×', 'cellar door bookings'), ('+27%', 'average bottle price'), ('4', 'new Melbourne stockists')]),
    dict(slug='pedal-and-pip', name='Pedal & Pip', place='Brisbane, QLD', sector='Kids bike brand', year='2024', glyph='bloom', font='playful',
         c1='#FF5A5F', c2='#FFD3E0', ink='#2B1B1E', paper='#FFF6F2', props='bag', tagline='First rides, big grins.',
         services=['Strategy', 'Identity', 'Campaign'],
         challenge='A kids bike brand that parents trusted and kids completely ignored.',
         idea='Pip, a flower made of four circles, turned bikes, boxes and stickers into something kids ask for by name. Parents get the safety story; kids get a friend.',
         results=[('+58%', 'direct-to-consumer sales'), ('12k', 'stickers given away'), ('4.9★', 'average review')]),
    dict(slug='bower-studio', name='Bower Studio', place='Sydney, NSW', sector='Architecture practice', year='2024', glyph='quarter', font='calm',
         c1='#B23A48', c2='#EFE7E1', ink='#1D1A1A', paper='#F7F3EF', props='sign', tagline='Rooms that feel like somewhere.',
         services=['Positioning', 'Identity', 'Pitch system'],
         challenge='Beautiful buildings, generic brand. The practice kept losing pitches to bigger firms with glossier decks.',
         idea='A quarter-circle, the shape a door draws on a floor plan, became a flexible system for drawings, signage, the website and every pitch deck.',
         results=[('3 of 4', 'pitches won after launch'), ('+64%', 'enquiries'), ('1', 'award shortlist')]),
]

SERVICES = [
    dict(id='strategy', g='target', title='Brand strategy', short='Find the one thing you can own.',
         text='Positioning, audience, competitors and the story only you can tell. The thinking every good-looking brand quietly stands on.',
         deliver=['Half-day brand workshop', 'Audience and competitor map', 'Positioning statement', 'Brand pillars and personality', 'Messaging hierarchy'], time='2 to 3 weeks', price='From $3,500'),
    dict(id='identity', g='spark', title='Visual identity', short='A look people recognise in half a second.',
         text='Logo suite, colour, type, icons, patterns and the rules that hold them together. Designed as a system, not a single logo.',
         deliver=['Primary and secondary logos', 'Colour and type system', 'Custom icon set', 'Patterns and textures', 'Brand guidelines'], time='5 to 7 weeks', price='From $9,500'),
    dict(id='naming', g='bubble', title='Naming and voice', short='Words that sound like nobody else.',
         text='Business, product and campaign names, plus a tone of voice your whole team can write in. Screened against the ASIC business names register and IP Australia trade mark search before you fall in love.',
         deliver=['Naming territories', 'Shortlist of screened names', 'Tagline options', 'Tone of voice guide', 'Key messages'], time='2 to 4 weeks', price='From $2,800'),
    dict(id='campaigns', g='star', title='Brand campaigns', short='Launches people actually notice.',
         text='Campaign ideas, key visuals and rollout across social, outdoor and digital, built on the brand so every touchpoint adds up. Measured properly, because I come from the data side.',
         deliver=['Campaign idea and line', 'Key visuals', 'Social and ad templates', 'Launch plan', 'Results read-out'], time='3 to 6 weeks', price='From $4,500'),
    dict(id='social', g='bloom', title='Social and content', short='A feed that looks like a brand.',
         text='Content pillars, templates and art direction so your social presence feels designed every day, even when you post it yourself.',
         deliver=['Content pillars', 'Instagram and LinkedIn templates', 'Art direction guide', '30-day content calendar', 'Photo and video brief'], time='2 to 3 weeks', price='From $2,400'),
    dict(id='rollout', g='arch', title='Rollout and packaging', short='Everywhere your brand meets the world.',
         text='Packaging, signage, merch, decks and websites, art-directed so the brand survives contact with printers, developers and real life.',
         deliver=['Packaging and labels', 'Signage and environments', 'Stationery and merch', 'Pitch deck template', 'Website art direction'], time='Ongoing', price='Quoted per project'),
]

PLANS = [   # DEMO prices
    ("Brand Sprint", "$3,500", "One-off, 2 weeks", "Clarity and direction, fast.", ["Brand workshop", "Positioning and personality", "Moodboards and two creative routes", "Name or tagline check", "Next-step roadmap"], False),
    ("Brand Identity", "$9,500", "One-off, about 6 weeks", "The full system, built to last.", ["Everything in the Sprint", "Logo suite and custom icons", "Colour, type and patterns", "Brand guidelines", "Launch kit: social, stationery, deck"], True),
    ("Brand Partner", "$2,800", "Per month, ongoing", "A senior brand lead on call.", ["Monthly creative direction", "Campaign and content design", "Agency and printer wrangling", "Brand health check-ins", "Priority turnaround"], False),
]

PROCESS = [('eye', 'Listen', 'Workshops, customer chats and a hard look at the competition. I learn your business before I touch a pencil.'),
           ('target', 'Define', 'One sharp positioning, a personality and the words that go with it. Agreed before any design starts.'),
           ('spark', 'Design', 'Two creative routes, then one system: mark, colour, type, icons, patterns, all tested on real things.'),
           ('bubble', 'Voice', 'How the brand speaks, from taglines to error messages, so it sounds like you everywhere.'),
           ('star', 'Launch', 'Guidelines, templates and a rollout plan, then I stay close while it meets the world.')]

QUOTES = [  # DEMO
    ("Manjil found the thing we'd been circling for years and drew it in one afternoon. Customers now photograph our cups.", "Ana Ferreira", "Saltbush Coffee"),
    ("Our wine finally looks as good as it tastes. The cellar door doubled and nobody asks who designed the label anymore, they ask where to buy it.", "Tom Hadley", "Little Creek Wines"),
    ("Kids point at Pip in the park. That's the whole brief, delivered.", "Priya Nair", "Pedal & Pip"),
]

FAQ_HOME = [
    ("What does a branding expert actually do?", "I work out what your business should stand for, then make it visible: positioning, name and voice, logo and identity system, and the campaigns that launch it. The goal is a brand people recognise, remember and choose."),
    ("How much does branding cost in Australia?", "It ranges widely. A small-business identity from a senior independent usually sits in the low thousands to the low tens of thousands. My Brand Sprint starts at $3,500 and a full identity at $9,500, with fixed quotes before we start."),
    ("How long does a rebrand take?", "A focused strategy sprint takes about two weeks. A full identity takes around six weeks, plus rollout. I'll give you a week-by-week plan in the first call."),
    ("Do you work outside Melbourne?", "Yes. I'm Melbourne-based and work with businesses across Australia. Most work is remote, with in-person workshops where it helps."),
    ("Will I own my logo?", "Yes. You own the final artwork and files outright once the project is paid. I'll also point you to IP Australia so you can protect it as a trade mark."),
    ("Can you do the marketing as well?", "Yes. I started in data-driven digital marketing, so campaigns, social and the tracking behind them are part of the job, not an afterthought."),
]

BUILDER = {   # personality -> palette and taglines for the home page brand builder
    'bold': dict(label='Bold', c1='#F83232', c2='#161211', ink='#161211', paper='#F4EEE6', tags=['{n}. No half measures.', 'Louder than the rest.', 'Made to be noticed.']),
    'warm': dict(label='Warm', c1='#E8553D', c2='#F6C9A8', ink='#2A1A14', paper='#FBF3EA', tags=['Made with care, served with heart.', 'Come in, you are welcome here.', 'Good things, done kindly.']),
    'premium': dict(label='Premium', c1='#7A1F1F', c2='#E9DCC9', ink='#1C1212', paper='#F6F0E6', tags=['Quietly exceptional.', 'Considered in every detail.', 'Less, but better.']),
    'playful': dict(label='Playful', c1='#FF5A5F', c2='#FFD3E0', ink='#2B1B1E', paper='#FFF6F2', tags=['Serious fun.', 'Life is better with {n}.', 'Go on, have a little joy.']),
    'calm': dict(label='Calm', c1='#B23A48', c2='#EFE7E1', ink='#1D1A1A', paper='#F7F3EF', tags=['Breathe out.', 'Simple, steady, good.', 'Room to think.']),
}

# ====================================================================== VISUALS (SVG)
CHAR_W = {'bold': .5, 'warm': .56, 'premium': .9, 'playful': .6, 'calm': .62}   # rough em width per character

def fit(s, font, width, maxsize):
    return min(maxsize, width / (max(len(s), 1) * CHAR_W[font]))

def txt(x, y, s, size, fill, font='bold', anchor='start', extra='', keep_case=False):
    fam, w, up, style = FONTS[font]
    up = up and not keep_case
    return f'<text x="{x:.1f}" y="{y:.1f}" font-family="{fam}, sans-serif" font-weight="{w}" font-size="{size:.1f}" fill="{fill}" text-anchor="{anchor}" style="{style}"{extra}>{E(s.upper() if up else s)}</text>'

def mono(x, y, s, size, fill, anchor='start'):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-family="DM Mono, monospace" font-size="{size:.1f}" letter-spacing=".08em" fill="{fill}" text-anchor="{anchor}">{E(s.upper())}</text>'

def grain(uid):
    return f'<filter id="gr{uid}"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/><feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .35 0"/><feComposite in2="SourceGraphic" operator="in"/></filter>'

def board(b, kind, W=1200, H=800, uid=''):
    """Generated brand-identity scenes for the demo case studies."""
    c1, c2, ink, paper, g = b['c1'], b['c2'], b['ink'], b['paper'], b['glyph']
    nm, f = b['name'], b['font']
    u = f'{b["slug"]}{kind}{uid}'
    head = f'<svg viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" role="img" aria-label="{E(nm)}: {kind} (demo artwork)"><defs>{grain(u)}</defs>'
    tail = f'<rect width="{W}" height="{H}" filter="url(#gr{u})" opacity=".55"/></svg>'
    if kind == 'hero':
        body = (f'<rect width="{W}" height="{H}" fill="{c1}"/>' + gpath(g, W * .5, -H * .12, H * 1.12, c2, 8) +
                txt(W * .05, H * .86, nm, fit(nm, f, W * .42, H * .13), paper, f) + mono(W * .05, H * .93, b['tagline'], H * .028, paper) + mono(W * .05, H * .09, f'{b["place"]} · {b["year"]}', H * .026, paper))
    elif kind == 'cards':
        cw, ch = W * .46, W * .46 * .58
        back = f'<g transform="translate({W * .14:.0f} {H * .2:.0f}) rotate(-9)"><rect width="{cw:.0f}" height="{ch:.0f}" fill="{c1}"/>{gpath(g, cw * .58, ch * .12, ch * .76, c2)}</g>'
        front = (f'<g transform="translate({W * .4:.0f} {H * .36:.0f}) rotate(5)"><rect width="{cw:.0f}" height="{ch:.0f}" fill="{paper}" stroke="{ink}" stroke-opacity=".12"/>'
                 f'{gpath(g, cw * .08, ch * .12, ch * .2, c1)}{txt(cw * .08, ch * .62, nm, fit(nm, f, cw * .84, ch * .14), ink, f)}{mono(cw * .08, ch * .8, "hello@" + b["slug"].replace("-", "") + ".com.au", ch * .055, ink)}{mono(cw * .08, ch * .89, b["place"], ch * .055, ink)}</g>')
        body = f'<rect width="{W}" height="{H}" fill="{c2}"/>{back}{front}'
    elif kind == 'cup':
        cx = W * .5
        cup = (f'<path d="M{cx - 150} {H * .3} L{cx + 150} {H * .3} L{cx + 118} {H * .9} L{cx - 118} {H * .9}Z" fill="{paper}"/>'
               f'<path d="M{cx - 139} {H * .5} L{cx + 139} {H * .5} L{cx + 128} {H * .7} L{cx - 128} {H * .7}Z" fill="{c1}"/>'
               f'<rect x="{cx - 168}" y="{H * .24}" width="336" height="{H * .07}" rx="14" fill="{ink}"/>' + gpath(g, cx - 52, H * .53, 104, c2))
        body = f'<rect width="{W}" height="{H}" fill="{c2}"/>' + gpath(g, -W * .08, H * .45, H * .7, c1, -12) + cup + mono(W * .05, H * .09, 'Takeaway cup', H * .026, ink)
    elif kind == 'bag':
        bx, by, bw, bh = W * .3, H * .3, W * .4, H * .62
        bag = (f'<path d="M{bx + bw * .3} {by} C{bx + bw * .3} {by - H * .2} {bx + bw * .7} {by - H * .2} {bx + bw * .7} {by}" fill="none" stroke="{ink}" stroke-width="14"/>'
               f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="{paper}"/>' + gpath(g, bx + bw * .25, by + bh * .16, bw * .5, c1) +
               txt(bx + bw / 2, by + bh * .86, nm, fit(nm, f, bw * .86, bw * .085), ink, f, 'middle'))
        body = f'<rect width="{W}" height="{H}" fill="{c2}"/>{bag}' + mono(W * .05, H * .09, 'Tote and merch', H * .026, ink)
    elif kind == 'sign':
        cx, cy, r = W * .55, H * .55, H * .3
        sign = (f'<path d="M{W * .2} {H * .12} H{cx} V{cy - r}" fill="none" stroke="{ink}" stroke-width="10"/><circle cx="{cx}" cy="{cy}" r="{r}" fill="{c1}"/>' +
                gpath(g, cx - r * .55, cy - r * .55, r * 1.1, paper))
        body = f'<rect width="{W}" height="{H}" fill="{c2}"/><rect x="0" y="{H * .12 - 20}" width="{W * .22}" height="40" fill="{ink}"/>{sign}' + mono(W * .05, H * .93, 'Street signage', H * .026, ink)
    elif kind == 'pattern':
        n, s = 6, W / 6
        cells = []
        for i in range(n * 4):
            x, y = (i % n) * s, (i // n) * s
            col = [c1, ink, c2, c1][(i * 7 + i // n) % 4]
            cells.append(f'<rect x="{x}" y="{y}" width="{s}" height="{s}" fill="{paper if (i + i // n) % 2 else c2}"/>' + gpath(g, x + s * .15, y + s * .15, s * .7, col, (i * 90) % 360))
        body = f'<rect width="{W}" height="{H}" fill="{paper}"/>' + ''.join(cells)
    elif kind == 'palette':
        cols = [(c1, 'Primary'), (ink, 'Ink'), (c2, 'Accent'), (paper, 'Paper')]
        wsz = W / 4
        body = ''.join(f'<rect x="{i * wsz}" y="0" width="{wsz}" height="{H}" fill="{c}"/>{mono(i * wsz + 24, H - 64, n, 22, paper if c in (c1, ink) else ink)}{mono(i * wsz + 24, H - 32, c, 22, paper if c in (c1, ink) else ink)}' for i, (c, n) in enumerate(cols))
        body += txt(40, H * .32, 'Aa', H * .26, paper, f, keep_case=True) + mono(40, H * .4, FONTS[f][0], 22, paper)
    else:
        raise ValueError(kind)
    return head + body + tail

def cover(seed, glyph, word, variant=0, W=1200, H=750):
    """Journal covers: red pattern posters built from the glyph set."""
    bg, fg, alt = [(RED, INK, PAPER), (INK, RED, PAPER), (PAPER, RED, INK)][variant % 3]
    s = W / 8
    cells = ''.join(gpath(list(GLYPHS)[(seed + i) % 12], (i % 8) * s + s * .2, (i // 8) * s + s * .2, s * .6, alt if (i + seed) % 5 == 0 else fg, (i * 45) % 360) for i in range(8 * 5))
    return (f'<svg viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><defs>{grain("c" + str(seed) + str(variant))}</defs><rect width="{W}" height="{H}" fill="{bg}"/>'
            f'<g opacity=".22">{cells}</g>' + gpath(glyph, W * .56, H * .08, H * .84, fg, seed * 13) +
            f'<text x="{W * .05:.0f}" y="{H * .9:.0f}" font-family="Bricolage Grotesque, sans-serif" font-weight="800" font-size="{H * .22:.0f}" style="font-stretch:75%" letter-spacing="-4" fill="{alt if variant != 2 else INK}">{E(word.upper())}</text>'
            f'<rect width="{W}" height="{H}" filter="url(#grc{seed}{variant})" opacity=".6"/></svg>')

# ====================================================================== HELPERS
def sec_head(no, glyph, label, title, aside=''):
    return (f'<header class="sh"><p class="sh__no">{no:02d}</p><p class="sh__label">{G(glyph)}<span>{label}</span></p>'
            f'<h2 class="sh__title rv">{title}</h2>{f"<div class=sh__aside>{aside}</div>" if aside else ""}</header>')

def crumbs(P, trail):
    return B.crumbs(P, trail)

def phero(P, trail, meta, title, lead, actions='', glyphs=('spark', 'bloom', 'star'), aside=''):
    meta_html = ''.join(f'<li>{m}</li>' for m in meta)
    stick = ''.join(f'<span class="ph__g ph__g--{i}">{G(g)}</span>' for i, g in enumerate(glyphs))
    return f'''    <section class="ph" id="top" data-theme="red">
      <div class="ph__stickers" aria-hidden="true">{stick}</div>
      <div class="wrap">
        {crumbs(P, trail)}
        <h1 class="ph__title" aria-label="{E(strip(title))}"><span class="ln"><span>{title}</span></span></h1>
        <div class="ph__grid">
          <ul class="ph__meta in">{meta_html}</ul>
          <div class="ph__main"><p class="ph__lead in">{lead}</p>{f'<div class="actions in">{actions}</div>' if actions else ''}</div>
          {f'<div class="ph__aside in">{aside}</div>' if aside else ''}
        </div>
      </div>
    </section>'''

def cta(P, line='Got a brand that deserves <em>better</em>?', sub='A free 30-minute brand chat. You will leave with three things I would change first.'):
    return f'''    <section class="cta" data-theme="dark">
      <div class="wrap cta__grid">
        <p class="cta__line">{line}</p>
        <div class="cta__side"><p>{sub}</p><a class="btn btn--red" href="{P}book/" data-cursor="Let's talk">Start a brand {ARR}</a></div>
      </div>
    </section>'''

def faq(items, uid='q'):
    return B.faq(items, uid)

def band(P='', glyphs=None, theme='light'):
    gs = glyphs or list(GLYPHS)
    tiles = ''.join(f'<li class="tile tile--{i % 4}">{G(g)}</li>' for i, g in enumerate(gs * 3))
    return f'<div class="band" data-theme="{theme}" aria-hidden="true"><ul class="band__row">{tiles}</ul></div>'

def contact_form(subject, label='What are you building?'):
    needs = ''.join(f'<label><input type="checkbox" name="needs" value="{v}"><span>{v}</span></label>' for v in ["Strategy", "Identity", "Naming", "Campaign", "Social", "Packaging", "Full-time role"])
    return f'''<form class="form js-form" data-subject="{subject}" action="https://formspree.io/f/YOUR_FORM_ID" method="POST" novalidate>
          <label class="field"><span>Your name</span><input name="name" required autocomplete="name"></label>
          <label class="field"><span>Email</span><input type="email" name="email" required autocomplete="email"></label>
          <fieldset class="chips"><legend>I need help with</legend>{needs}</fieldset>
          <label class="field"><span>Budget</span><select name="budget"><option value="">Not sure yet</option><option>Under $5k</option><option>$5k to $10k</option><option>$10k to $25k</option><option>$25k+</option></select></label>
          <label class="field"><span>{label}</span><textarea name="message" rows="3" required></textarea></label>
          <input type="text" name="_gotcha" tabindex="-1" autocomplete="off" class="hp" aria-hidden="true">
          <div class="form__foot"><button type="submit" class="btn btn--ink"><span class="btn__text">Send it {ARR}</span><span class="btn__sent">Sent. Talk soon.</span></button><p class="small" data-form-note>Reply within one business day.</p></div>
        </form>'''

# ====================================================================== LAYOUT
NAV = [('Work', 'work/', 'work'), ('Services', 'services/', 'services'), ('Journal', 'blog/', 'blog'), ('Contact', 'contact/', 'contact')]
FONT_URL = ("https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wdth,wght@12..96,75..100,200..800"
            "&family=Fraunces:ital,opsz,wght,SOFT,WONK@0,9..144,100..900,0..100,0..1;1,9..144,100..900,0..100,0..1&family=DM+Mono:wght@400;500&display=swap")

def layout(P, path, title, desc, active, body, scripts=(), ld=()):
    nav = ''.join(f'<a href="{P}{h}"{" aria-current=page" if k == active else ""}>{n}</a>' for n, h, k in NAV)
    menu = ''.join(f'<a href="{P}{h}">{G(g)}<span>{n}</span></a>' for (n, h), g in zip([('Home', ''), *[(n, h) for n, h, _ in NAV], ('Start a brand', 'book/')], ['star', 'spark', 'bloom', 'bubble', 'heart', 'arch']))
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
  <link href="{FONT_URL}" rel="stylesheet">
  <link rel="stylesheet" href="{P}css/brand.css">{lds}
</head>
<body class="no-js">
  <script>document.body.classList.replace('no-js','js');</script>
  <svg width="0" height="0" style="position:absolute" aria-hidden="true">{B.SYMBOLS}{G_SPRITE}</svg>
  <a class="skip" href="#main">Skip to content</a>
  <div class="grain" aria-hidden="true"></div>
  <div class="cursor" id="cursor" aria-hidden="true">{G('spark', 'cursor__g')}<span id="cursorLabel"></span></div>
  <div class="toast" id="toast" role="status" aria-live="polite"></div>

  <header class="hd" id="nav">
    <div class="wrap hd__in">
      <a class="hd__brand" href="{P}" aria-label="Manjil Shrestha, home"><svg viewBox="0 0 1463 317"><use href="#logo"/></svg></a>
      <p class="hd__role">Branding expert<br>in Australia</p>
      <nav class="hd__nav" aria-label="Primary">{nav}</nav>
      <a class="hd__cta" href="{P}book/">{G('spark')}<span>Start a brand</span></a>
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
    {band(P, theme="red")}
    <div class="wrap">
      <div class="ft__grid">
        <div class="ft__col ft__col--lead"><p class="ft__big">Branding expert in Australia. I build brands people <em>remember</em>, and the marketing that makes them grow.</p><a class="btn btn--red" href="{P}book/">Start a brand {ARR}</a></div>
        <div class="ft__col"><h4>Site</h4><a href="{P}">Home</a><a href="{P}work/">Work</a><a href="{P}services/">Services</a><a href="{P}services/brand-identity/">Brand identity</a><a href="{P}blog/">Journal</a></div>
        <div class="ft__col"><h4>Say hello</h4><a href="#" data-copy-email data-email-text>hello@</a><a href="{P}book/">Book a brand chat</a><a href="{P}contact/">Contact</a></div>
        <div class="ft__col"><h4>Elsewhere</h4><div data-socials class="ft__soc"></div></div>
      </div>
      <div class="ft__logo" aria-hidden="true"><svg viewBox="0 0 1463 317"><use href="#logo"/></svg></div>
      <div class="ft__bar"><span>© <span data-year>2026</span> Manjil Shrestha</span><span>Melbourne-based, working Australia-wide</span><span class="ft__glyphs">{"".join(G(g) for g in ["star", "spark", "bloom", "heart"])}</span><a href="#top">Back to top ↑</a></div>
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

# ====================================================================== HOME
def home():
    P = ''
    words = ['remember', 'choose', 'trust', 'talk about', 'love']
    rot = ''.join(f'<span class="rot__w{" is-on" if i == 0 else ""}">{w}</span>' for i, w in enumerate(words))
    marquee = ''.join(f'<span>{w}</span>{G(g)}' for w, g in zip(['Strategy', 'Identity', 'Naming', 'Voice', 'Campaigns', 'Packaging', 'Social', 'Rollout'], ['spark', 'bloom', 'bubble', 'heart', 'star', 'arch', 'sun', 'target']))
    # Rebus manifesto: words that become icons
    def rb(word, g):
        return f'<span class="rb" tabindex="0" data-word="{word}">{G(g)}<span class="rb__w">{word}</span></span>'
    manifesto = (f'A brand is not a logo. It is what people {rb("see", "eye")} when they find you, what they {rb("feel", "heart")} when they use you, '
                 f'and what they {rb("say", "bubble")} about you when you are not in the room. My job is to make all three {rb("unforgettable", "star")}.')
    mwords = re.split(r'(<span class="rb".*?</span></span>)', manifesto)
    man_html = ''.join(p if p.startswith('<span class="rb"') else ''.join(f'<span class="mw">{w}</span> ' for w in p.split()) for p in mwords)
    glyph_btns = ''.join(f'<button type="button" class="bb__g{" is-on" if k == "sun" else ""}" data-g="{k}" aria-label="{v[1]} icon" title="{v[1]}">{G(k)}</button>' for k, v in GLYPHS.items())
    pers = ''.join(f'<label class="bb__p"><input type="radio" name="bbP" value="{k}"{" checked" if k == "warm" else ""}><span>{v["label"]}</span></label>' for k, v in BUILDER.items())
    tiles = ''.join(f'''<a class="wk wk--{i}" href="work/#{w["slug"]}" data-cursor="View">
            <div class="wk__img">{board(w, "hero", 1200, 820, "h")}</div>
            <div class="wk__meta"><h3>{E(w["name"])}</h3><p>{E(w["sector"])}, {E(w["place"])}</p><p class="wk__tags">{" · ".join(w["services"])} {DEMO}</p></div>
          </a>''' for i, w in enumerate(WORK))
    flips = ''.join(f'''<li class="flip" tabindex="0" data-cursor="Flip">
            <div class="flip__in">
              <div class="flip__f flip__front"><span class="flip__n">{i + 1:02d}</span>{G(s["g"], "flip__g")}<h3>{E(s["title"])}</h3><p>{E(s["short"])}</p></div>
              <div class="flip__f flip__back"><h3>{E(s["title"])}</h3><ul>{"".join(f"<li>{E(d)}</li>" for d in s["deliver"])}</ul><p class="flip__price">{E(s["price"])}</p><a class="tlink" href="services/#{s["id"]}">Details</a></div>
            </div></li>''' for i, s in enumerate(SERVICES))
    stops = ''.join(f'<li class="pr pr--{i}" style="--i:{i}"><span class="pr__g">{G(g)}</span><span class="pr__n">{i + 1:02d}</span><h3>{t}</h3><p>{d}</p></li>' for i, (g, t, d) in enumerate(PROCESS))
    deck = ''.join(f'<figure class="card card--{i}" style="--i:{i}"><span class="card__g">{G(["heart", "star", "bloom"][i])}</span><blockquote>{E(q)}</blockquote><figcaption><b>{E(n)}</b>{E(o)} {DEMO}</figcaption></figure>' for i, (q, n, o) in enumerate(QUOTES))
    jcards = ''.join(f'''<a class="jc rv" href="blog/{p["slug"]}/" data-cursor="Read">
            <div class="jc__img">{cover(p["seed"], p["glyph"], p["word"], i)}</div>
            <p class="jc__k">{E(p["tag"])} · {p["minutes"]} min</p><h3>{E(p["title"])}</h3></a>''' for i, p in enumerate(POSTS))
    values = ''.join(f'<li>{G(g)}<span>{t}</span></li>' for g, t in [('eye', 'Curious first'), ('target', 'One sharp idea'), ('heart', 'Made with care'), ('wave', 'Built to flex')])
    body = f'''    <section class="hero" id="top" data-theme="light">
      <div class="wrap hero__in">
        <div class="hero__top in"><p>{G('star')}Manjil Shrestha<br><span>a.k.a. mastha</span></p><p>Brand strategy, identity<br><span>and marketing</span></p><p>Melbourne-based<br><span>working Australia-wide</span></p><p class="hero__live"><i></i>Booking new brands<br><span>for early 2027</span></p></div>
        <div class="hero__stage">
          <div class="mark" id="mark" data-cursor="Click me" role="img" aria-label="A red shape that changes between brand marks">
            <svg viewBox="-110 -110 220 220" class="mark__svg"><defs><pattern id="ht" width="6" height="6" patternUnits="userSpaceOnUse"><circle cx="3" cy="3" r="1.3" fill="#161211" opacity=".16"/></pattern></defs><path id="markPath" d="M0-100A100 100 0 1 1-.1-100Z" fill="#F83232"/><path id="markShade" d="M0-100A100 100 0 1 1-.1-100Z" fill="url(#ht)"/></svg>
            <span class="mark__name" id="markName">Circle</span>
          </div>
          <h1 class="hero__h1"><span class="hero__kick in">Branding expert in Australia</span><span class="ln"><span>I make brands</span></span><span class="ln"><span>people <span class="rot" id="rot">{rot}</span></span></span></h1>
        </div>
        <div class="hero__foot in">
          <p>Strategy, identity and the marketing that makes it stick. For Australian businesses that are too good to look ordinary.</p>
          <div class="hero__actions"><a class="btn btn--red" href="book/" data-cursor="Let's talk">Start a brand {ARR}</a><a class="tlink" href="#builder">Try the brand builder</a></div>
        </div>
      </div>
    </section>

    <div class="marquee" data-theme="red" aria-hidden="true"><div class="marquee__row">{marquee * 3}</div></div>

    <section class="manifesto" id="manifesto" data-theme="dark" aria-label="Manifesto">
      <div class="wrap">
        <p class="manifesto__k">{G('star')}Manifesto</p>
        <p class="manifesto__t" aria-label="{E(strip(manifesto))}">{man_html}</p>
        <p class="manifesto__hint">Hover the icons. Every brand needs its own alphabet; this is mine.</p>
      </div>
    </section>

    <section class="builder" id="builder" data-theme="blush">
      <div class="wrap">
        {sec_head(2, "spark", "Brand builder", "Give me a name. I'll give you a <em>brand</em>.", '<p>A five-second taste of how I think. The real thing takes a few weeks and a lot more listening.</p>')}
        <div class="bb">
          <form class="bb__in" id="bb" onsubmit="return false">
            <label class="field bb__name"><span>Your business name</span><input id="bbName" value="Saltbush" maxlength="22" autocomplete="off" spellcheck="false"></label>
            <fieldset class="bb__ps"><legend>Personality</legend>{pers}</fieldset>
            <fieldset class="bb__gs"><legend>Pick a mark</legend><div class="bb__grid">{glyph_btns}</div></fieldset>
            <div class="bb__row"><button type="button" class="btn btn--ink" id="bbShuffle">{G('spark')}Surprise me</button><a class="tlink" href="book/">Build the real one</a></div>
          </form>
          <div class="bb__out" id="bbOut" data-font="warm" aria-live="polite">
            <div class="bb__logo"><span class="bb__mark">{G('sun')}</span><span class="bb__word" id="bbWord">Saltbush</span></div>
            <p class="bb__tag" id="bbTag">Made with care, served with heart.</p>
            <div class="bb__mocks">
              <div class="mk mk--card"><span class="bb__mark">{G('sun')}</span><b class="bb__w2">Saltbush</b><small>hello@saltbush.com.au</small></div>
              <div class="mk mk--bag"><i></i><span class="bb__mark">{G('sun')}</span><b class="bb__w2">Saltbush</b></div>
              <div class="mk mk--app"><span class="bb__mark">{G('sun')}</span></div>
              <div class="mk mk--post"><span class="bb__mark">{G('sun')}</span><p class="bb__tag2">Made with care, served with heart.</p></div>
            </div>
            <ul class="bb__pal" id="bbPal"><li></li><li></li><li></li><li></li></ul>
          </div>
        </div>
      </div>
    </section>

    <section class="work" id="work" data-theme="light">
      <div class="wrap">
        {sec_head(3, "eye", "Selected work", "Brands with a <em>point</em> of view.", '<a class="tlink" href="work/">All case studies</a>')}
        <div class="work__grid">{tiles}</div>
      </div>
    </section>

    <section class="svc" id="services" data-theme="red">
      <div class="wrap">
        {sec_head(4, "bloom", "What I do", "Six ways to be <em>unforgettable</em>.", '<a class="tlink" href="services/">Services and pricing</a>')}
        <ol class="flips">{flips}</ol>
      </div>
    </section>

    {band()}

    <section class="process" id="process" data-theme="light">
      <div class="wrap">
        {sec_head(5, "wave", "How it works", "From blank page to <em>brand</em>.")}
        <div class="process__track">
          <svg class="process__line" viewBox="0 0 1000 200" preserveAspectRatio="none" aria-hidden="true"><path id="prLine" d="M0 150 C 100 150, 100 50, 200 50 S 300 150, 400 150 S 500 50, 600 50 S 700 150, 800 150 S 900 50, 1000 50"/></svg>
          <ol class="process__list">{stops}</ol>
        </div>
      </div>
    </section>

    <section class="about" id="about" data-theme="dark">
      <div class="wrap about__grid">
        <figure class="about__img rv" data-cursor="Wave hello">
          <canvas id="halftone" aria-hidden="true"></canvas>
          <img src="assets/img/portrait.jpg" alt="Portrait of Manjil Shrestha" width="1000" height="1371">
          <figcaption>{G('star')}Manjil Shrestha, Melbourne</figcaption>
        </figure>
        <div class="about__txt">
          <p class="sh__no">06</p>
          <h2 class="about__title rv">Hi, I'm Manjil. I make businesses <em>impossible</em> to ignore.</h2>
          <p class="about__p rv">I grew up in Kathmandu surrounded by hand-painted signs, festival colour and shopkeepers who knew every customer by name. That's still my definition of a brand: something people recognise from across the street and feel good about up close.</p>
          <p class="about__p rv">I started in data-driven digital marketing, so I design brands that look great and perform. Today I help Australian businesses find their story, build identities around it and launch them with campaigns that actually get noticed.</p>
          <ul class="values">{values}</ul>
          <a class="btn btn--red" href="book/">Work with me {ARR}</a>
        </div>
      </div>
    </section>

    <section class="kind" data-theme="blush" aria-label="Kind words">
      <div class="wrap kind__grid">
        <div class="kind__head">{sec_head(7, "heart", "Kind words", "What clients <em>say</em>.")}<div class="kind__nav"><button type="button" class="btn btn--ink" id="deckNext">{G('spark')}Next card</button><span id="deckCount">1 / {len(QUOTES)}</span></div></div>
        <div class="deck" id="deck">{deck}</div>
      </div>
    </section>

    <section class="sec" id="journal" data-theme="light">
      <div class="wrap">
        {sec_head(8, "bubble", "Journal", "Notes on brands that <em>work</em>.", '<a class="tlink" href="blog/">All articles</a>')}
        <div class="jgrid">{jcards}</div>
      </div>
    </section>

    <section class="sec" id="faq" data-theme="light">
      <div class="wrap faq">
        {sec_head(9, "target", "FAQ", "Good questions.")}
        {faq(FAQ_HOME)}
      </div>
    </section>

    <section class="contact" id="contact" data-theme="red">
      <div class="contact__g" aria-hidden="true">{G('star')}</div>
      <div class="wrap">
        <p class="contact__big"><span class="ln"><span>Let's make</span></span><span class="ln"><span>something <em>iconic</em>.</span></span></p>
        <div class="contact__grid">
          <div class="contact__info">
            <p>Tell me about your business and where you want it to go. I reply within one business day with honest thoughts, even if I'm not the right fit.</p>
            <button type="button" class="contact__email" data-copy-email><span data-email-text>hello@</span><small>Copy</small></button>
            <dl class="contact__dl"><div><dt>Based</dt><dd>Melbourne, Australia</dd></div><div><dt>Works</dt><dd>Australia-wide</dd></div><div><dt>Elsewhere</dt><dd data-socials class="contact__soc"></dd></div></dl>
          </div>
          {contact_form("Brand enquiry")}
        </div>
      </div>
    </section>'''
    person = json.dumps({"@context": "https://schema.org", "@type": "Person", "name": "Manjil Shrestha", "alternateName": "mastha", "jobTitle": "Branding Expert",
                         "knowsAbout": ["Branding", "Brand strategy", "Visual identity", "Marketing"], "address": {"@type": "PostalAddress", "addressLocality": "Melbourne", "addressRegion": "VIC", "addressCountry": "AU"}, "areaServed": "Australia", "url": SITE}, ensure_ascii=False)
    builder_js = f'<script>window.BRAND_BUILDER = {json.dumps(BUILDER)}; window.BRAND_FONTS = {json.dumps({k: [v[0], v[1], v[2]] for k, v in FONTS.items()})};</script>'
    write('index.html', layout(P, '', 'Branding Expert in Australia | Manjil Shrestha', 'Manjil Shrestha is a branding expert in Australia. Brand strategy, visual identity, naming and campaigns for businesses that are too good to look ordinary.', 'home', body + '\n' + builder_js, ['home.js'], [person, B.faq_ld(FAQ_HOME)]))

# ====================================================================== WORK
def work():
    P = '../'
    items = []
    for i, w in enumerate(WORK):
        side = 'b' if w['props'] in ('bag',) else 'a'
        prop = w['props']
        items.append(f'''
    <section class="case" id="{w["slug"]}" data-theme="{["light", "blush"][i % 2]}" style="--c1:{w["c1"]};--c2:{w["c2"]}">
      <div class="wrap">
        <header class="case__head">
          <p class="case__no">{G(w["glyph"])}Case {i + 1:02d} {DEMO}</p>
          <h2 class="case__title rv">{E(w["name"])}</h2>
          <dl class="case__facts"><div><dt>Client</dt><dd>{E(w["sector"])}</dd></div><div><dt>Where</dt><dd>{E(w["place"])}</dd></div><div><dt>Year</dt><dd>{w["year"]}</dd></div><div><dt>Work</dt><dd>{" · ".join(w["services"])}</dd></div></dl>
        </header>
        <figure class="case__hero rv">{board(w, "hero", 1600, 900)}</figure>
        <div class="case__story">
          <div><h3>{G("target")}The challenge</h3><p>{E(w["challenge"])}</p></div>
          <div><h3>{G("spark")}The idea</h3><p>{E(w["idea"])}</p></div>
        </div>
        <div class="case__gallery">
          <figure class="rv">{board(w, "cards")}</figure>
          <figure class="rv">{board(w, prop)}</figure>
          <figure class="rv">{board(w, "pattern")}</figure>
          <figure class="rv">{board(w, "palette")}</figure>
        </div>
        <ul class="case__res">{"".join(f'<li class="rv"><b>{E(v)}</b><span>{E(l)}</span></li>' for v, l in w["results"])}</ul>
      </div>
    </section>''')
    body = phero(P, [("Home", ""), ("Work", "work/")], ["<span>Projects</span>Four demo case studies", "<span>Clients</span>VIC, NSW, QLD", "<span>Focus</span>Identity and launch"],
                 "Work that people <em>notice</em>.", "Selected brand projects across Australia. Strategy first, then identity systems built to flex from a coffee cup to a billboard.",
                 f'<a class="btn btn--ink" href="#{WORK[0]["slug"]}">See the work {ARR}</a>', ('eye', 'sun', 'bloom')) + ''.join(items) + f'''

{cta(P, "Your brand could be <em>next</em>.")}'''
    write('work/index.html', layout(P, 'work/', 'Branding Case Studies | Manjil Shrestha, Branding Expert in Australia', 'Brand strategy and identity case studies from Manjil Shrestha, a branding expert in Australia.', 'work', body))

# ====================================================================== SERVICES
SVC_FAQ = [("Do I need strategy if I just want a logo?", "A logo without strategy is decoration. The Brand Sprint is the short version: two weeks to agree what the brand stands for, so the design has something to say."),
           ("What do I get at the end?", "Final files in every format you need, guidelines that explain how to use them, and templates for the things you make most often. You own all of it."),
           ("Do you work with in-house teams and agencies?", "Often. I can lead the brand and hand over to your team or agency, or slot into an existing project."),
           ("Can you help with marketing after launch?", "Yes. The Brand Partner retainer covers campaigns, content and creative direction month to month.")]

def plans_html(P, plans):
    return '<div class="plans">' + ''.join(f'''<article class="plan{" plan--hot" if hot else ""} rv">
          <header>{G(["target", "spark", "heart"][i])}<h3>{E(n)}</h3>{'<span class="plan__tag">Most chosen</span>' if hot else ''}</header>
          <p class="plan__price">{E(pr)}</p><p class="plan__unit">{E(u)} {DEMO}</p><p class="plan__for">{E(f)}</p>
          <ul>{"".join(f"<li>{E(x)}</li>" for x in items)}</ul>
          <a class="btn {"btn--red" if hot else "btn--ink"}" href="{P}book/">Start with a chat {ARR}</a>
        </article>''' for i, (n, pr, u, f, items, hot) in enumerate(plans)) + '</div>'

def services():
    P = '../'
    jump = ''.join(f'<a href="#{s["id"]}">{G(s["g"])}<span>{E(s["title"])}</span></a>' for s in SERVICES)
    rows = ''.join(f'''
        <article class="sv" id="{s["id"]}">
          <div class="sv__a"><span class="sv__icon">{G(s["g"])}</span><p class="sv__no">{i + 1:02d}</p><h2>{E(s["title"])}</h2><p class="sv__short">{E(s["short"])}</p>
            <dl class="sv__facts"><div><dt>Timeline</dt><dd>{E(s["time"])}</dd></div><div><dt>Investment</dt><dd>{E(s["price"])}</dd></div></dl></div>
          <div class="sv__b"><h3>What it is</h3><p>{E(s["text"])}</p>{'<a class="tlink" href="brand-identity/">The full identity process</a>' if s["id"] == "identity" else ''}</div>
          <div class="sv__c"><h3>What you get</h3><ul class="ticks">{"".join(f"<li>{G(s['g'])}{E(d)}</li>" for d in s["deliver"])}</ul></div>
        </article>''' for i, s in enumerate(SERVICES))
    steps = ''.join(f'<li class="step rv"><span class="step__g">{G(g)}</span><span class="step__n">{i + 1:02d}</span><h3>{t}</h3><p>{d}</p></li>' for i, (g, t, d) in enumerate(PROCESS))
    body = phero(P, [("Home", ""), ("Services", "services/")], ["<span>Services</span>Six, mix and match", "<span>Packages</span>From $2,400", "<span>Where</span>Australia-wide"],
                 "Brands built to be <em>remembered</em>.", "Strategy, identity, naming, campaigns and the rollout that ties them together. Pick one, or let me build the whole brand.",
                 f'<a class="btn btn--ink" href="{P}book/">Book a brand chat {ARR}</a><a class="tlink" href="#pricing">Packages and pricing</a>', ('target', 'spark', 'bubble')) + f'''

    <section class="sec sec--tight" data-theme="light">
      <div class="wrap"><nav class="jump" aria-label="Services">{jump}</nav>{rows}</div>
    </section>

    {band()}

    <section class="sec" id="pricing" data-theme="blush">
      <div class="wrap">
        {sec_head(1, "heart", "Packages", "Three ways to <em>start</em>.", '<p>Fixed quotes, no surprises. Every project starts with a free brand chat.</p>')}
        {plans_html(P, PLANS)}
      </div>
    </section>

    <section class="sec" data-theme="red">
      <div class="wrap">
        {sec_head(2, "wave", "Process", "Five steps, zero <em>mystery</em>.")}
        <ol class="steps">{steps}</ol>
      </div>
    </section>

    <section class="sec" data-theme="light">
      <div class="wrap faq">
        {sec_head(3, "target", "FAQ", "Before you ask.")}
        {faq(SVC_FAQ)}
      </div>
    </section>

{cta(P, "Not sure where to <em>start</em>?", "Tell me about the business. I'll tell you honestly what it needs first, even if that's nothing from me.")}'''
    write('services/index.html', layout(P, 'services/', 'Branding Services in Australia | Manjil Shrestha', 'Brand strategy, visual identity, naming, campaigns, social and packaging from Manjil Shrestha, a branding expert in Australia.', 'services', body, ['inner.js'], [B.faq_ld(SVC_FAQ)]))

# ====================================================================== BRAND IDENTITY SERVICE PAGE
ID_FAQ = [("How many logo concepts will I see?", "Two distinct creative routes, each shown working on real things, not floating on white. We choose one and refine it together."),
          ("What if I hate both routes?", "It almost never happens, because we agree the strategy first. If it does, we go back to the brief together before designing again."),
          ("Will my logo work small and in one colour?", "Yes. Every mark is tested at favicon size, in one colour and reversed, before it is signed off."),
          ("Can you trade mark it for me?", "I'm not a lawyer, so I don't file trade marks. I do run early searches and recommend you speak to a trade mark attorney or apply through IP Australia.")]
BOX = [('star', 'Logo suite', 'Primary logo, wordmark, stacked and icon versions, in colour, one colour and reversed.'),
       ('bloom', 'Colour system', 'A primary palette, supporting tones and accessible pairings with every code you need.'),
       ('bubble', 'Typography', 'Display and text typefaces, a type scale and licensing sorted.'),
       ('spark', 'Custom icons', 'A small icon family drawn in the same hand as the logo.'),
       ('quarter', 'Patterns and texture', 'Patterns, textures and graphic devices for packaging, social and space.'),
       ('eye', 'Photo and illustration direction', 'How the brand looks in pictures, with dos, don\'ts and a shot list.'),
       ('arch', 'Guidelines', 'A clear, friendly brand book your team and suppliers will actually use.'),
       ('heart', 'Launch kit', 'Social templates, stationery, email signature and a pitch deck, ready on day one.')]

def identity():
    P = '../../'
    box = ''.join(f'<li class="box__i rv" tabindex="0">{G(g, "box__g")}<h3>{t}</h3><p>{d}</p></li>' for g, t, d in BOX)
    weeks = [("Week 1", "Discover", "Workshop, research, competitor audit."), ("Week 2", "Define", "Positioning and personality signed off."), ("Weeks 3–4", "Design", "Two routes shown on real mockups."),
             ("Week 5", "Refine", "One route, every detail, every size."), ("Week 6", "Deliver", "Files, guidelines and launch kit.")]
    road = ''.join(f'<li class="rv"><span class="rd__when">{w}</span><h3>{t}</h3><p>{d}</p></li>' for w, t, d in weeks)
    ex = WORK[0]
    before = (f'<svg viewBox="0 0 1200 800" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><rect width="1200" height="800" fill="#E9E6E1"/><rect x="380" y="300" width="440" height="200" rx="8" fill="#fff" stroke="#bbb"/>'
              f'<circle cx="460" cy="400" r="46" fill="#7DA7C9"/><text x="530" y="392" font-family="Arial, sans-serif" font-size="40" fill="#5A6A7A">Saltbush</text><text x="532" y="432" font-family="Arial, sans-serif" font-size="20" fill="#8A97A3">coffee roasters pty ltd</text>'
              f'<text x="60" y="80" font-family="DM Mono, monospace" font-size="24" fill="#8A97A3" letter-spacing="2">BEFORE</text></svg>')
    after = board(ex, 'hero', 1200, 800, 'ba').replace('</svg>', '<text x="1140" y="80" font-family="DM Mono, monospace" font-size="24" fill="#FBF3EA" text-anchor="end" letter-spacing="2">AFTER</text></svg>')
    body = phero(P, [("Home", ""), ("Services", "services/"), ("Brand identity", "services/brand-identity/")], ["<span>Service</span>Visual identity", "<span>Timeline</span>About 6 weeks", "<span>From</span>$9,500"],
                 "Brand identity <em>design</em>.", "Not just a logo. A complete visual system, from mark to icons to patterns, designed so your brand looks like itself everywhere, for years.",
                 f'<a class="btn btn--ink" href="{P}book/">Book a free brand chat {ARR}</a><a class="tlink" href="#box">What\'s in the box</a>', ('star', 'quarter', 'spark')) + f'''

    <section class="sec" data-theme="light">
      <div class="wrap">
        {sec_head(1, "eye", "Before and after", "Same business. <em>Different</em> league.", '<p>Drag the handle. Demo project: Saltbush Coffee.</p>')}
        <div class="ba rv" id="ba" style="--p:50%" data-cursor="Drag">
          <div class="ba__after">{after}</div>
          <div class="ba__before">{before}</div>
          <input type="range" min="0" max="100" value="50" id="baRange" aria-label="Compare before and after">
          <span class="ba__handle" aria-hidden="true">{G("spark")}</span>
        </div>
      </div>
    </section>

    <section class="sec" id="box" data-theme="red">
      <div class="wrap">
        {sec_head(2, "quarter", "What's in the box", "Eight things your brand <em>gets</em>.")}
        <ol class="box">{box}</ol>
      </div>
    </section>

    <section class="sec" data-theme="light">
      <div class="wrap">
        {sec_head(3, "wave", "Timeline", "Six weeks, start to <em>launch</em>.")}
        <ol class="road">{road}</ol>
      </div>
    </section>

    <section class="sec" data-theme="dark">
      <div class="wrap">
        {sec_head(4, ex["glyph"], "Mini case study", "Saltbush, <em>under a big sky</em>.", f'<a class="tlink" href="{P}work/#{ex["slug"]}">Full case study</a>')}
        <div class="mini">
          <figure class="mini__img rv">{board(ex, "cup", 1200, 800, "m")}</figure>
          <div class="mini__txt"><p>{E(ex["idea"])}</p><ul class="case__res">{"".join(f'<li class="rv"><b>{E(v)}</b><span>{E(l)}</span></li>' for v, l in ex["results"])}</ul><p class="small">Demo project for illustration.</p></div>
        </div>
      </div>
    </section>

    <section class="sec" id="pricing" data-theme="blush">
      <div class="wrap">
        {sec_head(5, "heart", "Pricing", "Clear prices, no <em>fine print</em>.")}
        {plans_html(P, PLANS)}
      </div>
    </section>

    <section class="sec" data-theme="light">
      <div class="wrap faq">
        {sec_head(6, "target", "Identity FAQ", "Straight answers.")}
        {faq(ID_FAQ)}
      </div>
    </section>

{cta(P, "Ready to look like you <em>mean it</em>?")}'''
    svc = json.dumps({"@context": "https://schema.org", "@type": "Service", "name": "Brand identity design", "provider": {"@type": "Person", "name": "Manjil Shrestha"}, "areaServed": "Australia", "offers": {"@type": "Offer", "price": "9500", "priceCurrency": "AUD"}}, ensure_ascii=False)
    write('services/brand-identity/index.html', layout(P, 'services/brand-identity/', 'Brand Identity Design in Australia | Manjil Shrestha', 'Brand identity design by Manjil Shrestha, a branding expert in Australia: logo suite, colour, type, icons, patterns, guidelines and launch kit.', 'services', body, ['inner.js'], [svc, B.faq_ld(ID_FAQ)]))

# ====================================================================== BOOK
BOOK_FAQ = [("Is the brand chat really free?", "Yes. No card, no invoice, no obligation."), ("What should I bring?", "Your website or socials, a few brands you admire, and the thing that keeps bugging you about your current brand."),
            ("Can I reschedule?", "Of course. Reply to the confirmation email with a better time."), ("Will you sign an NDA?", "Happy to. Send it through before the call.")]

def book():
    P = '../'
    body = phero(P, [("Home", ""), ("Start a brand", "book/")], ["<span>Length</span>30 minutes", "<span>Format</span>Video call", "<span>Cost</span>Free"],
                 "Book a free brand <em>chat</em>.", "Thirty minutes about your business, your customers and your brand. No pitch deck. You'll leave with three things I would change first.", '', ('bubble', 'heart', 'spark')) + f'''

    <section class="sec sec--tight" data-theme="light">
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
              <label class="field"><span>Website or Instagram</span><input name="website"></label>
              <label class="field"><span>Main focus</span><select name="focus"><option value="">Not sure yet</option><option>Brand strategy</option><option>Visual identity</option><option>Naming and voice</option><option>Brand campaign</option><option>Social and content</option><option>Packaging and rollout</option><option>Full-time role</option></select></label>
              <label class="field"><span>Budget</span><select name="budget"><option value="">Prefer not to say</option><option>Under $5k</option><option>$5k to $10k</option><option>$10k to $25k</option><option>$25k+</option></select></label>
              <label class="field"><span>What would make this call worth it?</span><textarea name="notes" rows="3"></textarea></label>
              <input type="text" name="_gotcha" tabindex="-1" autocomplete="off" class="hp" aria-hidden="true">
              <div class="form__foot"><button type="button" class="tlink" data-back>Back</button><button type="submit" class="btn btn--red">Request this time {ARR}</button></div>
              <p class="small" data-form-note>I will confirm by email with a meeting link.</p>
            </form>
          </div>
          <div class="panel-step" data-step="3">
            <div class="confirm"><span class="confirm__icon" aria-hidden="true">{G("heart")}</span><h3>Requested.</h3><p>I will confirm by email within one business day with a meeting link.</p>
              <dl class="kpis kpis--list"><div><dt>When</dt><dd id="cWhen"></dd></div><div><dt>Who</dt><dd id="cWho"></dd></div><div><dt>Focus</dt><dd id="cFocus"></dd></div></dl>
              <div class="actions"><a class="btn btn--red" id="gcalLink" target="_blank" rel="noopener">Add to Google Calendar</a><a class="tlink" id="icsLink" download="brand-chat.ics">Download .ics</a></div></div>
          </div>
          <div class="booker__bar" id="bookBar"><p id="bookSum"></p><button type="button" class="btn btn--ink" id="toDetails" disabled>Continue {ARR}</button></div>
        </div>
        <aside class="book__side">
          <h3>What we'll cover</h3>
          <ol class="agenda"><li>{G("eye")}Your business, your customers and what makes you different.</li><li>{G("target")}What your brand says today, and what it should say.</li><li>{G("spark")}Three changes I would make first.</li><li>{G("star")}Next steps: with me, someone else, or on your own.</li></ol>
          <div class="who"><img src="{P}assets/img/avatar.png" alt="" width="56" height="56"><p><strong>Manjil Shrestha</strong><span>Branding expert in Australia</span></p></div>
        </aside>
      </div>
    </section>

    <section class="sec" data-theme="light">
      <div class="wrap faq">
        {sec_head(1, "bubble", "Booking", "Good questions.")}
        {faq(BOOK_FAQ)}
      </div>
    </section>'''
    write('book/index.html', layout(P, 'book/', 'Book a Free Brand Chat | Manjil Shrestha, Branding Expert in Australia', 'Book a free 30-minute brand chat with Manjil Shrestha, a branding expert in Australia.', 'book', body, ['book.js'], [B.faq_ld(BOOK_FAQ)]))

# ====================================================================== CONTACT
CONTACT_FAQ = [("Where do you work?", "Melbourne-based, with clients across Australia. Most work is remote, with workshops in person where it helps."),
               ("Are you open to full-time roles?", "Yes, for the right brand or marketing team. Choose \"Full-time role\" in the form and include the link."),
               ("How quickly do you reply?", "Within one business day, usually the same day.")]

def contact():
    P = '../'
    days = [("Mon", "9:00 to 18:00"), ("Tue", "9:00 to 18:00"), ("Wed", "9:00 to 18:00"), ("Thu", "9:00 to 18:00"), ("Fri", "9:00 to 17:00"), ("Sat", "Closed"), ("Sun", "Closed")]
    aside = f'<div class="clockbox">{G("sun")}<p class="lab__k">Melbourne, now</p><p class="clock" id="mClock">--:--</p><p id="mStatus">Checking…</p></div>'
    body = phero(P, [("Home", ""), ("Contact", "contact/")], ["<span>Reply</span>Within one business day", "<span>Based</span>Melbourne, Australia", "<span>Open to</span>Projects and roles"],
                 "Say <em>hello</em>.", "A new brand, a rebrand, a campaign or a full-time role. Write a few lines and I will get back to you.", '', ('heart', 'bubble', 'sun'), aside) + f'''

    <section class="sec sec--tight" data-theme="light">
      <div class="wrap">
        <ul class="ways">
          <li class="rv">{G("bubble")}<span>Email</span><button type="button" data-copy-email data-email-text>hello@</button></li>
          <li class="rv">{G("spark")}<span>Call</span><a href="{P}book/">Book a free brand chat {ARR}</a></li>
          <li class="rv">{G("eye")}<span>LinkedIn</span><a href="https://www.linkedin.com/in/manjilshrestha" target="_blank" rel="noopener">/in/manjilshrestha {NE}</a></li>
          <li class="rv">{G("arch")}<span>Hiring</span><a href="{P}assets/Manjil-Shrestha-CV.pdf">Download CV {ARR}</a></li>
        </ul>
      </div>
    </section>

    <section class="sec" data-theme="blush">
      <div class="wrap contact2">
        <div>{sec_head(1, "heart", "Write to me", "Tell me about your <em>brand</em>.")}{contact_form("Website enquiry")}</div>
        <aside class="contact2__side"><h3>Studio hours, Melbourne</h3><ul class="hours">{"".join(f'<li data-day="{d}"><span>{d}</span><span>{h}</span></li>' for d, h in days)}</ul><h3>Elsewhere</h3><div data-socials class="side__soc"></div></aside>
      </div>
    </section>

    <section class="sec" data-theme="light">
      <div class="wrap faq">
        {sec_head(2, "target", "Quick answers", "Good to know.")}
        {faq(CONTACT_FAQ)}
      </div>
    </section>'''
    write('contact/index.html', layout(P, 'contact/', 'Contact Manjil Shrestha | Branding Expert in Australia', 'Get in touch with Manjil Shrestha, a branding expert in Australia, about brand strategy, identity, naming or campaigns.', 'contact', body, ['pages.js'], [B.faq_ld(CONTACT_FAQ)]))

# ====================================================================== JOURNAL CONTENT
POSTS = [
    dict(slug='your-logo-is-not-your-brand', tag='Strategy', tagkey='strategy', date='2026-10-21', minutes=6, seed=3, glyph='star', word='Brand',
         title='Your logo is not your brand (here is what is)',
         dek='A logo is a signature. The brand is the reputation behind it. Here is how to tell the difference, and what to fix first if your brand feels flat.',
         body=lambda: f'''
<div class="tldr"><h4>TL;DR</h4><ul>
<li>A logo identifies you. A brand is what people believe and feel about you.</li>
<li>Most "we need a new logo" problems are really positioning problems.</li>
<li>Fix the story first, then the system, then the logo.</li></ul></div>

<p>Every month someone asks me for a new logo. Usually what they want is to be noticed, trusted or remembered, and a logo alone can't do that. It's the face of the brand, not the whole person.</p>

<h2 id="signature"><span class="num">01</span>A logo is a signature</h2>
<p class="has-note">Think of your logo as a signature on a letter. It tells people who it's from. Whether they want to read it depends on everything else: what you say, how you say it, and how you made them feel last time. <span class="side">The best logos get their meaning over time. Nobody loved the Nike swoosh in 1971.</span></p>
<div class="stat-row"><div><b>1</b><span>idea your brand should own</span></div><div><b>3</b><span>places it must show up: look, voice, experience</span></div><div><b>0</b><span>kangaroos required to look Australian</span></div></div>

<h2 id="what-a-brand-is"><span class="num">02</span>What a brand actually is</h2>
<p>A brand is the sum of every impression. In practice I break it into three layers, and only one of them is visual.</p>
<ul><li><strong>Story:</strong> what you stand for, who it's for and why you're different.</li><li><strong>System:</strong> logo, colour, type, icons, patterns and photography working together.</li><li><strong>Behaviour:</strong> tone of voice, customer experience and the decisions you make when nobody's watching.</li></ul>
<div class="callout"><span class="callout__i">✦</span><p><strong>Quick test:</strong> cover your logo on your website and social. Could a stranger still tell it's you? If not, the system needs work, not the logo.</p></div>

<h2 id="fix-order"><span class="num">03</span>Fix things in the right order</h2>
<p>When a brand feels flat, I work from the inside out:</p>
<ol><li>Agree one sharp positioning line. If you can't say it in a sentence, nobody else can either.</li><li>Define a personality with three words, and three words you are not.</li><li>Build the visual system around that personality.</li><li>Only then refine or replace the logo.</li></ol>
<blockquote>People don't remember logos. They remember how you made them feel, and the logo becomes the shortcut to that feeling.<cite>Manjil Shrestha</cite></blockquote>

<h2 id="checklist"><span class="num">04</span>The five-minute brand check</h2>
<ul class="checklist">
<li><label><input type="checkbox"><span>I can explain what we stand for in one sentence</span></label></li>
<li><label><input type="checkbox"><span>Our website, socials and packaging look like the same company</span></label></li>
<li><label><input type="checkbox"><span>We have a consistent colour palette and two typefaces at most</span></label></li>
<li><label><input type="checkbox"><span>Our team writes in a recognisable tone of voice</span></label></li>
<li><label><input type="checkbox"><span>Customers describe us the way we describe ourselves</span></label></li></ul>
<p>Three ticks or fewer? Start with the story. <a href="../../book/">Book a free brand chat</a> and we'll find it together.</p>'''),
    dict(slug='how-to-name-a-business-in-australia', tag='Naming', tagkey='naming', date='2026-09-30', minutes=7, seed=6, glyph='bubble', word='Name',
         title='How to name a business in Australia without regret',
         dek='A great name is short, ownable and legally clear. Here is the naming process I use, plus the Australian checks to run before you print anything.',
         body=lambda: f'''
<div class="tldr"><h4>TL;DR</h4><ul>
<li>Generate widely, then filter hard: meaning, sound, length and spelling.</li>
<li>In Australia, check the ASIC business names register and IP Australia trade marks before you fall in love.</li>
<li>Registering a business name does not give you ownership of it. A trade mark does far more.</li></ul></div>

<p>Naming is the most emotional part of branding. Everyone has an opinion, every good name seems taken, and the one you love turns out to mean something rude in another language. Here's how to get through it calmly.</p>

<h2 id="territories"><span class="num">01</span>Start with territories, not names</h2>
<p>Before brainstorming, decide what kinds of names you're open to. I usually explore four territories:</p>
<ul><li><strong>Descriptive:</strong> says what you do. Clear, but hard to protect.</li><li><strong>Evocative:</strong> suggests a feeling or story, like Saltbush or Little Creek.</li><li><strong>Invented:</strong> a new word. Easy to own, harder to explain.</li><li><strong>Founder or place:</strong> personal and credible, but less flexible if you grow.</li></ul>

<h2 id="filter"><span class="num">02</span>Filter like a brand strategist</h2>
<p class="has-note">Score your shortlist out of five on each of these, and be honest. <span class="side">Say it out loud on a phone call. If you have to spell it twice, it's a problem.</span></p>
<div class="table-wrap"><table><thead><tr><th>Test</th><th>Question</th></tr></thead><tbody>
<tr><td>Meaning</td><td>Does it support our positioning?</td></tr>
<tr><td>Sound</td><td>Is it easy to say, hear and remember?</td></tr>
<tr><td>Spelling</td><td>Can people type it after hearing it once?</td></tr>
<tr><td>Length</td><td>Does it fit on a cup, an app icon and a sign?</td></tr>
<tr><td>Ownability</td><td>Can we protect it and get a usable domain?</td></tr></tbody></table></div>

<h2 id="checks"><span class="num">03</span>The Australian checks</h2>
<p>Run these before you share the name with anyone outside the team:</p>
<ol><li><strong>ASIC business names register:</strong> is the exact name already registered?</li><li><strong>IP Australia trade mark search:</strong> is anything similar registered for related goods or services?</li><li><strong>Domains:</strong> a <code>.com.au</code> needs an Australian presence, such as an ABN. Check <code>.com</code> too.</li><li><strong>Socials:</strong> are the handles free on the platforms you'll actually use?</li></ol>
<div class="callout callout--warn"><span class="callout__i">!</span><p><strong>Watch out:</strong> a registered business name lets you trade under it. It doesn't stop others using something similar. For real protection, talk to a trade mark attorney or apply through IP Australia.</p></div>

<h2 id="decide"><span class="num">04</span>How to decide</h2>
<p>Put your top three on real things: a mock shopfront, a business card, an Instagram profile. Live with them for a week. The right name usually stops feeling strange and starts feeling inevitable.</p>
<blockquote>A good name doesn't have to explain everything. It has to be worth remembering.<cite>Manjil Shrestha</cite></blockquote>'''),
    dict(slug='brand-consistency-small-business', tag='Identity', tagkey='identity', date='2026-09-02', minutes=5, seed=9, glyph='bloom', word='System',
         title='Why your brand looks different everywhere (and how to fix it)',
         dek='Inconsistent brands look smaller than they are. A simple brand system, not a thicker rulebook, keeps every touchpoint looking like you.',
         body=lambda: f'''
<div class="tldr"><h4>TL;DR</h4><ul>
<li>Inconsistency usually comes from missing tools, not lazy people.</li>
<li>A small system beats a big guideline: core assets, templates and a few rules.</li>
<li>Audit, simplify, then template the things you make most.</li></ul></div>

<p>Your website is red, your Instagram is pastel, your invoice is in Comic Sans and your van has the old logo. It happens to almost every growing business, and it quietly makes you look smaller and less trustworthy than you are.</p>

<h2 id="why"><span class="num">01</span>Why brands drift</h2>
<p>Drift happens when people have to guess. A new designer, a printer, a freelancer or you at 11pm before a market day. If the right files and rules aren't easy to find, everyone improvises.</p>
<div class="stat-row"><div><b>1</b><span>shared folder with the right files</span></div><div><b>5</b><span>templates cover most of what you make</span></div><div><b>10</b><span>rules, not 100 pages</span></div></div>

<h2 id="audit"><span class="num">02</span>Run a quick audit</h2>
<p class="has-note">Screenshot or photograph every touchpoint: website, socials, emails, packaging, signage, uniforms, invoices. Lay them out on one wall or one board. <span class="side">The wall test is brutal and brilliant. Patterns jump out in seconds.</span></p>
<div class="callout"><span class="callout__i">✦</span><p><strong>Tip:</strong> circle everything that looks like it came from a different company. That's your fix list.</p></div>

<h2 id="system"><span class="num">03</span>Build a small system</h2>
<ul><li><strong>Core assets:</strong> logo versions, colour codes, two typefaces, a few icons and one pattern.</li><li><strong>Templates:</strong> social posts, presentations, email header, price list, signage.</li><li><strong>Ten rules:</strong> the dos and don'ts that matter most, on one page.</li></ul>
<blockquote>Consistency is not about being boring. It's about being recognisable at a glance.<cite>Manjil Shrestha</cite></blockquote>

<h2 id="keep"><span class="num">04</span>Keep it alive</h2>
<p>Name a brand owner, even if it's you. Review new work against the ten rules once a month. When something new comes up, add a template rather than another exception.</p>
<p>Want a brand system your whole team can use? <a href="../../services/brand-identity/">See the identity service</a>.</p>'''),
]
TEMPLATE = dict(slug='_template', tag='Category', tagkey='strategy', date='2026-11-06', minutes=4, seed=11, glyph='spark', word='Title',
    title='Your article title goes here (keep it under 65 characters)',
    dek='The dek: one or two sentences that tell the reader what they will learn and why it matters. This also becomes the meta description.',
    body=lambda: '''
<div class="tldr"><h4>TL;DR</h4><ul><li>Three bullets that summarise the article.</li><li>Lead with the most useful idea.</li><li>Keep each under 20 words.</li></ul></div>
<p>Intro paragraph. Two to four sentences. Say why this matters to an Australian business owner today.</p>
<h2 id="section-one"><span class="num">01</span>First section heading</h2>
<p class="has-note">Body copy in Fraunces. Use short paragraphs. <span class="side">Margin note: an aside, a story, or a tip.</span></p>
<div class="stat-row"><div><b>1</b><span>stat label</span></div><div><b>2</b><span>stat label</span></div><div><b>3</b><span>stat label</span></div></div>
<div class="callout"><span class="callout__i">✦</span><p><strong>Callout:</strong> a tip worth highlighting.</p></div>
<div class="callout callout--warn"><span class="callout__i">!</span><p><strong>Warning:</strong> a common mistake.</p></div>
<h2 id="section-two"><span class="num">02</span>Second section heading</h2>
<ul><li>Bullet list item</li><li>Bullet list item</li></ul>
<blockquote>A pull quote that is worth sharing on its own.<cite>Manjil Shrestha</cite></blockquote>
<div class="table-wrap"><table><thead><tr><th>Column</th><th>Column</th></tr></thead><tbody><tr><td>Cell</td><td>Cell</td></tr></tbody></table></div>
<ul class="checklist"><li><label><input type="checkbox"><span>Checklist item</span></label></li><li><label><input type="checkbox"><span>Checklist item</span></label></li></ul>''')
SOON = [dict(tag='Marketing', tagkey='marketing', title='Brand vs performance: why you need both', dek='How brand building makes every ad dollar work harder.'),
        dict(tag='Identity', tagkey='identity', title='Designing a logo that works at 16 pixels', dek='The small-size test every mark should pass.')]

def journal_rows(P, posts, soon=()):
    rows = []
    for i, p in enumerate(posts):
        rows.append(f'''<li class="jr" data-post data-tags="{p["tagkey"]}" data-text="{E((p["title"] + " " + p["dek"] + " " + p["tag"]).lower())}">
            <a href="{P}blog/{p["slug"]}/" data-cursor="Read"><span class="jr__g">{G(p["glyph"])}</span><span class="jr__date">{B.fmt_date(p["date"])}</span><span class="jr__title">{E(p["title"])}</span><span class="jr__tag">{E(p["tag"])}</span><span class="jr__min">{p["minutes"]} min {ARR}</span></a></li>''')
    for s in soon:
        rows.append(f'<li class="jr jr--soon post--soon" data-post data-tags="{s["tagkey"]}" data-text="{E((s["title"] + " " + s["dek"]).lower())}"><div><span class="jr__g">{G("spark")}</span><span class="jr__date">In progress</span><span class="jr__title">{E(s["title"])}</span><span class="jr__tag">{E(s["tag"])}</span><span class="jr__min">Soon</span></div></li>')
    return '<ol class="journal">' + ''.join(rows) + '</ol>'

def blog_index():
    P = '../'
    feat = POSTS[0]
    filt = ''.join(f'<button class="filter{" is-on" if k == "all" else ""}" data-filter="{k}">{n}</button>' for k, n in [("all", "All"), ("strategy", "Strategy"), ("identity", "Identity"), ("naming", "Naming"), ("marketing", "Marketing")])
    nl = '<form class="nl js-form" data-subject="Newsletter signup" action="https://formspree.io/f/YOUR_FORM_ID" method="POST" novalidate><label class="field"><span>One brand idea a month</span><input type="email" name="email" required placeholder="you@business.com.au" autocomplete="email"></label><input type="text" name="_gotcha" tabindex="-1" autocomplete="off" class="hp" aria-hidden="true"><button class="btn btn--ink" type="submit"><span class="btn__text">Subscribe</span><span class="btn__sent">Subscribed</span></button></form>'
    body = phero(P, [("Home", ""), ("Journal", "blog/")], ["<span>Journal</span>Brand notes", "<span>Topics</span>Strategy, identity, naming", "<span>Cadence</span>Monthly"],
                 "Notes on brands that <em>work</em>.", "Practical ideas on strategy, identity, naming and marketing for Australian businesses. No jargon, no fluff.", '', ('bubble', 'spark', 'star'), nl) + f'''

    <section class="sec sec--tight" data-theme="light" id="articles">
      <div class="wrap">
        <a class="feat rv" href="{feat["slug"]}/" data-post data-tags="{feat["tagkey"]}" data-text="{E((feat["title"] + " " + feat["dek"]).lower())}" data-cursor="Read">
          <div class="feat__img">{cover(feat["seed"], feat["glyph"], feat["word"], 0)}</div>
          <div class="feat__txt"><p class="feat__k">Featured, {B.fmt_date(feat["date"])}, {feat["minutes"]} min</p><h2>{E(feat["title"])}</h2><p>{E(feat["dek"])}</p><span class="tlink">Read the article</span></div>
        </a>
        <div class="blog-tools rv"><div class="filters" role="group" aria-label="Filter by topic">{filt}</div><label class="search"><span class="sr">Search articles</span><input type="search" id="postSearch" placeholder="Search"><span id="postCount"></span></label></div>
        {journal_rows(P, POSTS, SOON)}
        <p class="empty" id="emptyState">Nothing matches that yet. <a class="tlink" href="{P}contact/">Suggest a topic</a></p>
      </div>
    </section>
{cta(P, "Rather talk about <em>your</em> brand?", "A free 30-minute brand chat is faster than reading.")}'''
    write('blog/index.html', layout(P, 'blog/', 'Branding Journal: Strategy, Identity and Naming | Manjil Shrestha', 'Practical branding articles from Manjil Shrestha, a branding expert in Australia: strategy, identity, naming and marketing.', 'blog', body, ['blog.js']))

def article(p, i, template=False):
    P = '../../'
    path = f'blog/{p["slug"]}/'
    prev_p = POSTS[i - 1] if i > 0 and not template else None
    next_p = POSTS[i + 1] if i + 1 < len(POSTS) and not template else None
    pn = '' if template else '<nav class="pn" aria-label="More articles">' + (f'<a href="{P}blog/{prev_p["slug"]}/"><span>Newer</span>{E(prev_p["title"])}</a>' if prev_p else '<span></span>') + (f'<a href="{P}blog/{next_p["slug"]}/"><span>Older</span>{E(next_p["title"])}</a>' if next_p else '<span></span>') + '</nav>'
    body = f'''    <article class="art">
      <header class="art__head" id="top" data-theme="red">
        <div class="ph__stickers" aria-hidden="true"><span class="ph__g ph__g--0">{G(p["glyph"])}</span><span class="ph__g ph__g--1">{G("spark")}</span></div>
        <div class="wrap">
          {crumbs(P, [("Home", ""), ("Journal", "blog/"), (p["tag"], "blog/")])}
          <div class="art__grid">
            <ul class="ph__meta"><li><span>Topic</span>{E(p["tag"])}</li><li><span>Published</span>{B.fmt_date(p["date"])}</li><li><span>Reading time</span>{p["minutes"]} minutes</li><li><span>Author</span>Manjil Shrestha</li></ul>
            <div><h1 class="art__title"><span class="ln"><span>{E(p["title"])}</span></span></h1><p class="art__dek in">{E(p["dek"])}</p>
              <div class="share in"><a data-share="linkedin" target="_blank" rel="noopener">LinkedIn {NE}</a><a data-share="x" target="_blank" rel="noopener">X {NE}</a><button type="button" data-copy-link>Copy link</button></div></div>
          </div>
        </div>
      </header>
      <div class="wrap"><figure class="art__cover in">{cover(p["seed"], p["glyph"], p["word"], i % 3, 1600, 640)}</figure></div>
      <div class="wrap art__body">
        <aside class="toc"><p>Contents</p><ol id="toc"></ol><p class="toc__p"><span id="tocLeft">{p["minutes"]} min left</span></p><div class="meter"><i id="tocBar"></i></div></aside>
        <div class="art__col">
          <details class="toc-m"><summary>Contents</summary><ol id="tocMobile"></ol></details>
          <div class="prose" data-minutes="{p["minutes"]}">{p["body"]()}</div>
          <footer class="art__end">
            <div class="byline"><img src="{P}assets/img/avatar.png" alt="" width="64" height="64"><p><strong>Manjil Shrestha</strong> is a branding expert in Australia. He builds brand strategy, identity and campaigns for businesses that are too good to look ordinary. <a class="tlink" href="{P}book/">Book a free brand chat</a></p></div>
            {pn}
          </footer>
        </div>
      </div>
    </article>
    <section class="sec" data-theme="light">
      <div class="wrap">{sec_head(1, "bubble", "Keep reading", "More from the <em>journal</em>.", f'<a class="tlink" href="{P}blog/">All articles</a>')}{journal_rows(P, [q for q in POSTS if q is not p])}</div>
    </section>'''
    ld = json.dumps({"@context": "https://schema.org", "@type": "BlogPosting", "headline": p["title"], "datePublished": p["date"], "author": {"@type": "Person", "name": "Manjil Shrestha"}}, ensure_ascii=False)
    write(path + 'index.html', layout(P, path, p["title"] + ' | Manjil Shrestha', p["dek"], 'blog', body, ['blog.js'], [] if template else [ld]))

# ====================================================================== PAGE TEMPLATE
# Copy this function to make a new page. Standard order (DESIGN-BLUEPRINT.md section 6):
#   red hero -> light -> pattern band -> blush -> red -> light (FAQ) -> dark CTA -> dark footer
def page_template():
    P = '../'
    path = '_template/'
    fq = [("What is this page?", "A copy-ready template that shows every Living Mark block in the standard order."),
          ("How do I make a new page?", "Copy page_template() in tools/build_brand.py, rename it, change P, path, the copy and the write() call, then rebuild.")]
    body = phero(P, [("Home", ""), ("Template", path)], ["<span>Label</span>Value", "<span>Label</span>Value", "<span>Label</span>Value"],
                 "Page title with one <em>italic</em> word.", "One or two sentences: who this is for and what changes for them. Warm, plain words.",
                 f'<a class="btn btn--ink" href="{P}book/">Primary action {ARR}</a><a class="tlink" href="#faq">Secondary link</a>', ('spark', 'heart', 'star')) + f'''

    <!-- BLOCK: light section with card grid -->
    <section class="sec" data-theme="light">
      <div class="wrap">
        {sec_head(1, "eye", "Section label", "A headline with one <em>italic</em> word.", '<p>Optional aside, one sentence.</p>')}
        <ol class="box box--light">{"".join(f'<li class="box__i rv" tabindex="0">{G(g, "box__g")}<h3>Card title</h3><p>One or two lines about this item.</p></li>' for g in ["star", "bloom", "bubble", "spark"])}</ol>
      </div>
    </section>

    <!-- BLOCK: pattern band (divider) -->
    {band()}

    <!-- BLOCK: blush section with packages -->
    <section class="sec" data-theme="blush" id="pricing">
      <div class="wrap">
        {sec_head(2, "heart", "Packages", "Three ways to <em>start</em>.")}
        {plans_html(P, PLANS)}
      </div>
    </section>

    <!-- BLOCK: red section with steps -->
    <section class="sec" data-theme="red">
      <div class="wrap">
        {sec_head(3, "wave", "Process", "Five steps, zero <em>mystery</em>.")}
        <ol class="steps">{"".join(f'<li class="step rv"><span class="step__g">{G(g)}</span><span class="step__n">{i + 1:02d}</span><h3>{t}</h3><p>{d}</p></li>' for i, (g, t, d) in enumerate(PROCESS))}</ol>
      </div>
    </section>

    <!-- BLOCK: light FAQ (always the last content block) -->
    <section class="sec" data-theme="light" id="faq">
      <div class="wrap faq">
        {sec_head(4, "target", "FAQ", "Straight answers.")}
        {faq(fq)}
      </div>
    </section>

{cta(P)}'''
    write(path + 'index.html', layout(P, path, 'Page template | Manjil Shrestha', 'Copy-ready Living Mark page template.', '', body, ['inner.js'], [B.faq_ld(fq)]))

# ====================================================================== ASSETS + RUN
def copy_assets():
    for rel in ['js/content.js', 'js/book.js', 'js/blog.js', 'js/pages.js', 'js/vendor/gsap.min.js', 'js/vendor/ScrollTrigger.min.js', 'js/vendor/lenis.min.js', 'js/vendor/LICENSE-lenis.txt', 'assets/img/portrait.jpg', 'assets/img/avatar.png']:
        dst = os.path.join(OUT, rel); os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copyfile(os.path.join(ROOT, rel), dst)
    d = GLYPHS['spark'][0]
    open(os.path.join(OUT, 'assets/favicon.svg'), 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="{RED}"/><g transform="translate(12 12) scale(.4)"><path fill="{PAPER}" d="{d}"/></g></svg>\n')

if __name__ == '__main__':
    copy_assets()
    home(); work(); services(); identity(); book(); contact(); blog_index()
    for i, p in enumerate(POSTS):
        article(p, i)
    article(TEMPLATE, 0, template=True)
    page_template()
