# Living Mark — Design Blueprint

**The rulebook for the creative branding design of Manjil Shrestha, branding expert in Australia.**

The site is built like a brand book for Manjil himself: a logo that changes shape, its own icon alphabet, a pattern system, a texture and a voice. Every page and component follows this document. When you add a page, start from the template (section 9). If something new doesn't fit a rule here, add the rule here first, then build it.

- **Live template:** `brand/_template/index.html` shows the standard blocks in the standard order.
- **Generator:** `tools/build_brand.py`. All copy for this design lives there; copy `page_template()` to make a page.
- **Styles:** `brand/css/brand.css`. Part 2 is the look; Part 1 is the structural base.

---

## Contents

1. [The idea](#1-the-idea)
2. [Ten rules that never break](#2-ten-rules-that-never-break)
3. [Colour](#3-colour)
4. [Type](#4-type)
5. [The icon alphabet](#5-the-icon-alphabet)
6. [Texture, shape and pattern](#6-texture-shape-and-pattern)
7. [Page architecture](#7-page-architecture)
8. [Component library](#8-component-library)
9. [How to add a new page](#9-how-to-add-a-new-page)
10. [How to add other things](#10-how-to-add-other-things)
11. [Motion and interaction](#11-motion-and-interaction)
12. [Writing style](#12-writing-style)
13. [SEO and accessibility](#13-seo-and-accessibility)
14. [Checklist for every page](#14-checklist-for-every-page)
15. [File map](#15-file-map)
16. [Do and don't](#16-do-and-dont)

---

## 1. The idea

**A brand is a living system, not a logo.** The site proves it by having one.

- **The living mark:** the hero shape moves between seven identities: Circle, Signature, Bloom, Squircle, Spark, Sun and Blob. It never sits perfectly still.
- **The icon alphabet:** twelve geometric icons replace bullets, section markers, the cursor and even words in the manifesto.
- **Print, not pixels:** risograph grain, halftone dots, sticker-like rounded cards and slight tilts make it feel made by hand.
- **Red leads:** the logo red is the hero colour. Ink, paper and one red tint (blush) support it.
- **Show, don't tell:** the brand builder, flip cards and generated case-study identities let visitors *experience* branding instead of reading about it.

The previous data-led designs were about numbers. This one is about **feeling, recognition and craft**. Numbers appear only as proof inside case studies.

---

## 2. Ten rules that never break

1. **Red is primary.** Every page has red in the first screen and a red block somewhere below.
2. **Four site colours only:** red `#F83232`, ink `#161211`, paper `#F4EEE6` and blush `#F9D8D1`. Client colours appear only inside client artwork.
3. **Every section declares a theme:** `light`, `blush`, `red` or `dark`.
4. **Headlines are sentence case**, in Bricolage Grotesque, with **exactly one word in Fraunces italic** (`<em>`).
5. **Icons come from the alphabet.** No emoji, no icon fonts, no stock icons. If you need a new one, draw it on the 100 × 100 grid (section 5).
6. **Rounded, not boxy.** Cards are 22–30px radius, buttons and chips are pills, and borders are 1.5px ink.
7. **No drop shadows and no gradients.** Depth comes from tilts, overlaps and texture.
8. **One playful moment per section:** a tilt, a flip, a hover reveal, a sticker. Never three at once.
9. **Everything works without motion, a mouse or JavaScript.** The interactions are extras.
10. **Copy lives in `tools/build_brand.py`.** Never edit generated HTML.

---

## 3. Colour

### Tokens (Part 2 `:root` in `brand/css/brand.css`)

| Token | Value | Use |
|---|---|---|
| `--red` | `#F83232` | Primary. Fills, marks, icons, buttons, the living mark. |
| `--red-deep` | `#C81E1E` on paper, `#A81616` on blush | Small red **text** (5:1 on paper, 5.6:1 on blush). |
| `--ink` | `#161211` | Warm black. Text, dark blocks, borders. |
| `--bg` | `#F4EEE6` | Paper. |
| `--blush` | `#F9D8D1` | The only secondary tone: a tint of red. |
| `--stone` | `#EADFD3` | Rare: code backgrounds, warning callouts. |
| `--accent` | Changes per theme | Icon colour. Red on light, blush and dark; ink on red. |
| `--em` | Changes per theme | Italic word colour. Red on light and dark, deep red on blush, ink on red. |

### Themes

| Theme | Declare | Background | Text | Icons and italic word | Texture |
|---|---|---|---|---|---|
| **Light** | `data-theme="light"` | paper | ink | red | grain |
| **Blush** | `data-theme="blush"` | blush | ink | red / deep red | red dots, 9px |
| **Red** | `data-theme="red"` | red | ink | ink | ink dots, 7px |
| **Dark** | `data-theme="dark"` | ink | paper | red | red dots, 9px |

The header and cursor read the theme under them and change colour, so **an undeclared section breaks the header**.

### Contrast

- **Ink on red:** 4.9:1. Use freely.
- **Ink on paper:** 16:1. **Ink on blush:** 14:1.
- **Red on ink:** 4.9:1.
- **Red on paper:** 3.3:1, so **display sizes only** (24px+). Small red text uses `--red-deep`.
- **Paper on red:** 3.3:1. Allowed **only** for one display-size italic word (as in the contact headline), never for body text or labels.

---

## 4. Type

| Role | Font | Variable | Settings |
|---|---|---|---|
| **Display and UI:** headlines, nav, buttons, body | Bricolage Grotesque | `--display`, `--sans` | weight 760 for headlines, `opsz` 96; body 400, `opsz` 14 |
| **The italic word, quotes, article body** | Fraunces | `--serif` | italic 380–400, `SOFT` 100, `WONK` 1 for the accent word |
| **Labels and data** | DM Mono | `--mono` | 12px, capitals, `+0.06em` |

All three load from Google Fonts in `layout()`.

### Scale

| Element | Class | Size | Line-height |
|---|---|---|---|
| Home H1 | `.hero__h1` | `clamp(3.2rem, 9.2vw, 10.4rem)` | 0.90 |
| Contact headline | `.contact__big` | `clamp(3.8rem, 11.5vw, 13rem)` | 0.88 |
| Page title | `.ph__title` | `clamp(3.2rem, 8.6vw, 9.6rem)` | 0.90 |
| Case study title | `.case__title` | `clamp(3rem, 7vw, 7.6rem)` | 0.90 |
| CTA line | `.cta__line` | `clamp(2.8rem, 6.4vw, 7rem)` | 0.94 |
| Section title | `.sh__title` | `clamp(2.6rem, 5.4vw, 5.8rem)` | 0.95 |
| Manifesto | `.manifesto__t` | `clamp(2.2rem, 5.2vw, 5.6rem)` | 1.04 |
| Card title | `.flip h3`, `.box__i h3` | 1.5–2.6rem | 0.95–1 |
| Body | `body` | 17px | 1.55 |
| Article body | `.prose` (Fraunces) | `clamp(1.15rem, 1.35vw, 1.3rem)` | 1.62 |
| Label | mono role | 12px caps | 1.5 |

### Rules

- **Sentence case** for every headline, with tight tracking (`-0.035em` to `-0.05em`).
- **Exactly one `<em>` per headline.** Pick the emotional word: *remember*, *brand*, *point*, *iconic*.
- **Labels are always mono caps.** Add new label classes to the type-role list at the top of Part 2.
- Never set body text in Fraunces outside articles and quotes. Never italicise more than one word in a headline.

---

## 5. The icon alphabet

Twelve icons, defined once in `GLYPHS` in `tools/build_brand.py` and inlined as an SVG sprite on every page (`#g-name`).

| Icon | Name | Meaning | Typical use |
|---|---|---|---|
| ✱ | `star` | Signature | The logo star, manifesto "unforgettable", launch |
| ✦ | `spark` | Idea | Cursor, identity service, CTAs, favicon |
| ✿ | `bloom` | Joy | Social, playful brands |
| ∩ | `arch` | Home | Rollout, hiring |
| 👁 | `eye` | Vision | "See", listen, work |
| ☀ | `sun` | Warmth | Warm brands, contact clock |
| 💬 | `bubble` | Voice | Naming, journal, "say" |
| ♥ | `heart` | Love | "Feel", kind words, packages |
| ♛ | `crown` | Premium | Premium brands |
| ≈ | `wave` | Flow | Process, timelines |
| ◔ | `quarter` | Craft | Patterns, "what's in the box" |
| ◎ | `target` | Focus | Strategy, FAQ |

(The symbols in the first column are approximations; the real icons are custom geometric shapes.)

**Use them with** `G(name, cls)`, which outputs `<svg class="g g--name"><use href="#g-name"/></svg>`. They take `currentColor` through `--accent`, so they re-colour in every theme. Their size is `1em`, so set `font-size`.

**To draw a new icon:**
1. Use a 100 × 100 grid with 2px margin.
2. Build it from circles, quarter circles, straight lines and simple curves. Use one filled shape, no strokes.
3. Add it to `GLYPHS` with a one-word meaning. Use `EVENODD` if it has holes.
4. Check it at 16px (favicon size) and at 600px (hero size).
5. Document it in the table above.

---

## 6. Texture, shape and pattern

- **Grain:** a fixed animated noise layer (`.grain`) over the whole site, blended with `multiply`. Don't remove it; it's what makes the colour feel printed.
- **Halftone dots:** red, blush and dark blocks carry a dot pattern (in each theme's `background-image`). The portrait in About is redrawn as red halftone on canvas.
- **Misregistration:** the living mark has a halftone layer slightly offset, like a riso print.
- **Corners:** 22px (`--r`) for cards, 26–34px for big images, pills for buttons and chips, 50% for icon discs.
- **Tilts:** cards and plans sit at ±0.6° to ±1.4° and straighten on hover.
- **Pattern band:** `band()` outputs a strip of icon tiles in four colourways that drifts as you scroll. Use it as a divider **at most once per page** above the footer (the footer already has one).
- **Client artwork:** `board(brand, kind)` generates identity scenes (`hero`, `cards`, `cup`, `bag`, `sign`, `pattern`, `palette`). Each demo client has its own colours, which may appear only inside its artwork and as `--c1` accents inside its own case study.

---

## 7. Page architecture

### Standard inner page

```
┌─────────────────────────────────────────────┐
│ HEADER (pill nav, takes the colour below)   │
├─────────────────────────────────────────────┤
│ RED HERO  .ph                               │  crumbs → title with one <em> → meta | lead + actions | aside
│           floating icon stickers behind     │
├─────────────────────────────────────────────┤
│ LIGHT     main content                      │
├─────────────────────────────────────────────┤
│ PATTERN BAND (optional, once)               │
├─────────────────────────────────────────────┤
│ BLUSH     offer / packages / form           │
├─────────────────────────────────────────────┤
│ RED       process / what's in the box       │
├─────────────────────────────────────────────┤
│ LIGHT     FAQ (always the last content)     │
├─────────────────────────────────────────────┤
│ DARK CTA  .cta  one line + one button       │
├─────────────────────────────────────────────┤
│ FOOTER (dark) pattern band + giant MANJIL   │
└─────────────────────────────────────────────┘
```

### Rhythm rules

1. **Inner pages open with the red hero.** The home page opens on paper with the red living mark.
2. **Never put two red blocks next to each other.** The same goes for two dark blocks, except the CTA followed by the footer.
3. **Light and blush may sit next to each other.** They read as different textures.
4. **Every content section has a numbered section head** (`sec_head(no, glyph, label, title, aside)`), with its own icon.
5. **FAQ is the last content block**, then the dark CTA.
6. **One signature interaction per page at most:** the builder, the deck, before/after, or the flip cards.

### Home page order

| # | Block | Theme | Job |
|---|---|---|---|
| — | Hero + living mark | light | Who and what: "Branding expert in Australia" H1 |
| — | Marquee | red | The six services as a ticker |
| 01 | Rebus manifesto | dark | Point of view |
| 02 | Brand builder | blush | Experience branding in five seconds |
| 03 | Selected work | light | Proof through craft |
| 04 | Flip-card services | red | What I do |
| — | Pattern band | mixed | The pattern system |
| 05 | Process line | light | How it works |
| 06 | Halftone about | dark | Who I am |
| 07 | Card deck quotes | blush | Social proof |
| 08 | Journal | light | Expertise |
| 09 | FAQ | light | Objections |
| — | Contact | red | Conversion |

---

## 8. Component library

### Frame and helpers (`tools/build_brand.py`)

| Helper | Output |
|---|---|
| `layout(P, path, title, desc, active, body, scripts, ld)` | Full page: head, fonts, sprite, grain, cursor, header, menu, footer |
| `phero(P, trail, meta, title, lead, actions, glyphs, aside)` | Red page hero. `glyphs` is three icon names for the floating stickers. `title` may contain one `<em>`. |
| `sec_head(no, glyph, label, title, aside)` | Numbered section head with icon |
| `cta(P, line, sub)` | Dark CTA band |
| `band()` | Pattern band divider |
| `G(name, cls)` | Inline icon |
| `contact_form(subject, label)` | Enquiry form with brand chips |
| `plans_html(P, PLANS)` | Three package cards; the middle one is the dark "Most chosen" |
| `faq(items)` + `B.faq_ld(items)` | FAQ accordion and JSON-LD |
| `journal_rows(P, posts, soon)` | Article list rows with icons |
| `board(brand, kind)` / `cover(seed, glyph, word, variant)` | Generated artwork |

### Blocks

| Block | Markup | Use |
|---|---|---|
| **Box grid** | `<ol class="box"><li class="box__i">{G(g,"box__g")}<h3/><p/></li></ol>` | 4 to 8 features. Flips to ink on hover. Great in red. |
| **Steps** | `<ol class="steps"><li class="step"><span class="step__g">{G}</span><span class="step__n">01</span><h3/><p/></li></ol>` | A 3 to 5 step process |
| **Timeline** | `<ol class="road"><li><span class="rd__when"/><h3/><p/></li></ol>` | Phases over time |
| **Packages** | `plans_html()` | Pricing, always three |
| **Service rows** | `.sv` with `.sv__icon` disc, facts and ticks | Detailed services |
| **Case study** | `.case` with head, hero art, story, gallery, results | Work pages |
| **Before / after** | `.ba` with a range input | One per page, identity work |
| **Ways** | `<ul class="ways"><li>{G}<span/><a/></li></ul>` | Contact methods |
| **Journal card** | `.jc` with a `cover()` | Article teasers |

### Buttons

| Class | Look | Use |
|---|---|---|
| `.btn.btn--red` | Red pill, ink text. Ink pill inside red blocks. | Primary action |
| `.btn.btn--ink` | Ink pill, paper text. Paper pill inside dark blocks. | Secondary or submit |
| `.tlink` | Underlined bold link with arrow | Tertiary |

Buttons lift and tilt −1.5° on hover, and an icon inside them spins. Put `{G('spark')}` before the label for special actions ("Surprise me", "Next card").

### Signature pieces (home only, never reuse)

| Piece | Hooks | Script |
|---|---|---|
| Living mark | `#mark`, `#markPath`, `#markShade`, `#markName`, `.rot__w` | `home.js` |
| Rebus manifesto | `.manifesto__t`, `.mw`, `.rb[data-word]` | `home.js` |
| Brand builder | `#bb`, `#bbName`, `input[name=bbP]`, `.bb__g[data-g]`, `#bbOut` | `home.js` + `window.BRAND_BUILDER` |
| Flip cards | `.flip`, `.flip__front`, `.flip__back` | `home.js` + CSS |
| Process line | `#prLine`, `.pr` | `home.js` |
| Halftone portrait | `.about__img`, `#halftone` | `home.js` |
| Card deck | `#deck`, `.card`, `#deckNext` | `home.js` |

---

## 9. How to add a new page

Example: a "Packaging design" service page at `/services/packaging/`.

**1. Copy the template function** in `tools/build_brand.py`:

```python
def packaging():
    P = '../../'                       # depth: '../' for /x/, '../../' for /x/y/
    path = 'services/packaging/'
    fq = [("Question?", "Answer.")]
    body = phero(P, [("Home", ""), ("Services", "services/"), ("Packaging", path)],
                 ["<span>Service</span>Packaging", "<span>Timeline</span>4 to 6 weeks", "<span>From</span>$4,000"],
                 "Packaging people <em>pick up</em>.",
                 "One or two sentences about who it's for and what changes.",
                 f'<a class="btn btn--ink" href="{P}book/">Book a brand chat {ARR}</a>',
                 ('arch', 'sun', 'spark')) + f'''

    <section class="sec" data-theme="light">
      <div class="wrap">
        {sec_head(1, "quarter", "What's included", "Every side of the <em>box</em>.")}
        <ol class="box">...</ol>
      </div>
    </section>

    <section class="sec" data-theme="light" id="faq">
      <div class="wrap faq">{sec_head(2, "target", "FAQ", "Straight answers.")}{faq(fq)}</div>
    </section>

{cta(P)}'''
    write(path + 'index.html', layout(P, path,
          'Packaging Design in Australia | Manjil Shrestha',
          'Meta description, 140 to 160 characters, with "branding" and "Australia".',
          'services', body, ['inner.js'], [B.faq_ld(fq)]))
```

**2. Call it** in the `__main__` block at the bottom of the file.

**3. Link it.**
- Add it to the footer `Site` column in `layout()`.
- If it's a service, add a link from its row in `services()`.
- Keep the main nav to four items plus the "Start a brand" button.

**4. Rebuild and check:**

```bash
python3 tools/build_brand.py
```

```bash
python3 -m http.server 8000
```

Open `http://localhost:8000/brand/services/packaging/` and run the checklist in section 14.

### Block recipes by page type

| Page | After the red hero |
|---|---|
| Service | Light intro or before/after → red box grid → light timeline → dark mini case → blush packages → FAQ → CTA |
| Case study | Use `.case` sections alternating light and blush → CTA |
| About | Light story → band → blush values (box grid) → red steps → FAQ → CTA |
| Landing / offer | Light pains → red box grid → blush one package → FAQ → CTA |
| Utility (thanks, 404, legal) | Short red hero → one light block → CTA |

---

## 10. How to add other things

**A case study**
1. Add a dict to `WORK`. It needs:
   - `slug`, `name`, `place`, `sector`, `year`
   - a `glyph` from the alphabet
   - a `font` personality
   - colours `c1`, `c2`, `ink`, `paper`
   - `props` (`cup`, `bag` or `sign`)
   - `tagline`, `services`, `challenge`, `idea`, `results`
2. The home tile, work page section and artwork generate automatically.

**A blog post**
1. Add a dict to `POSTS` with a `glyph` and a one-word `word` for its cover.
2. Use these components in the body: `.tldr`, `.callout`, `.stat-row`, `.table-wrap`, `blockquote`, `.checklist`, and margin notes with `<span class="side">`.

**A service:** add it to `SERVICES` (`id`, `g`, `title`, `short`, `text`, `deliver`, `time`, `price`). The home flip card, services row and jump link appear automatically.

**A brand-builder personality:** add it to both `BUILDER` and `FONTS`, and add a `.bb__out[data-font="..."]` rule in the CSS.

**A new component**
1. Check section 8 first.
2. Name it in BEM style.
3. Use tokens only (never hex), the 1.5px ink border, `--r` corners and one icon.
4. Test it in all four themes.
5. Document it here.

---

## 11. Motion and interaction

| Effect | Where | Rule |
|---|---|---|
| Living mark | Home hero | Changes every 2.9s. Click to advance (with icon burst). Pauses off-screen. |
| Line reveal | Hero and page titles, contact headline | Slides up from a mask on load |
| Fade up with tilt | `.rv` | 28px up and 0.6° tilt, settling straight |
| Rebus | Manifesto | Words light up with scroll; icons reveal their word on hover, focus or tap |
| Flip | Service cards | Hover on mouse, tap or Enter on touch and keyboard |
| Drift | Pattern bands | Move sideways with scroll, alternate directions |
| Icon burst | Form sent, booking confirmed, mark click, "Surprise me" | Icons fly out from the point. Celebrations only. |
| Cursor | Mouse only | Spinning red spark; grows over links; becomes a labelled disc over `[data-cursor]` |
| Grain | Everywhere | Subtle jitter, 1.2s loop |

**Rules**
- Use spring easing (`--spring`) for playful things and `--ease` for reveals.
- Hovers take 0.2–0.6s.
- Use `data-cursor` labels of one or two words: "View", "Read", "Flip", "Let's talk", "Drag".
- `prefers-reduced-motion`: no grain jitter, marquee, drift, spinning or bursts; the mark holds one shape; the manifesto is fully lit. Keep it this way for anything new.

---

## 12. Writing style

- **Voice:** warm, confident, a little playful. First person singular ("I"), talking to one business owner.
- **Headlines:** one idea with one italic emotional word. 3 to 9 words, ending with a full stop.
- **Leads:** who it's for and what changes, in 1 to 2 sentences.
- **Australian English and context:** colour, organise, licence; suburbs and cities; ASIC and IP Australia where relevant.
- **Proof:** case study results always have a label ("+41% online bag sales"). Mark demo content with the `DEMO` badge.
- **Banned:** "unlock", "elevate", "game-changer", "synergy", "next-level", "in today's world", and exclamation marks.

---

## 13. SEO and accessibility

**SEO**
- **Primary keyword:** "branding expert in Australia". It sits in the home H1, home title and Person JSON-LD (`jobTitle`, `areaServed`).
- **Title format:** `Topic | Manjil Shrestha`, or `Service in Australia | Manjil Shrestha`. Under 60 characters.
- **Headings:** one H1 per page. Section titles are H2, cards are H3.
- **JSON-LD:** FAQPage on FAQ pages, Service on service pages, BlogPosting on articles.
- **Design option status:** pages are `noindex`, canonical to the main site, and `/brand/` is disallowed in `robots.txt`. To make it the main site, move its files to the root, remove `noindex` in `layout()`, and update `sitemap.xml`.

**Accessibility**
- Icons are `aria-hidden`.
- The rebus paragraph and split titles carry the full sentence in `aria-label`.
- The living mark has `role="img"` and a description.
- Focus outlines are 3px in the accent colour and always visible.
- Flip cards and rebus icons are keyboard-reachable (`tabindex="0"`).
- The before/after slider is a real range input.
- The cursor is mouse-only and hides over form fields.
- Follow the contrast rules in section 3.

---

## 14. Checklist for every page

- [ ] The red hero comes first (inner pages), and the page ends with the dark CTA and footer.
- [ ] Every section has a theme and a numbered section head with an icon.
- [ ] One `<em>` per headline, and no more.
- [ ] Only the four site colours (client colours only inside client artwork).
- [ ] Icons are from the alphabet; no emoji or stock icons.
- [ ] At most one signature interaction and one pattern band.
- [ ] Generated by `tools/build_brand.py`; links and depth (`P`) are correct.
- [ ] Width 390px: no sideways scroll. At 1280 and 1440px the grid aligns.
- [ ] No console errors, keyboard works, reduced motion is fine.

---

## 15. File map

| What | File |
|---|---|
| This blueprint | `brand/DESIGN-BLUEPRINT.md` |
| Overview | `brand/README.md` |
| Generator and **all copy**: icons, services, work, posts, pages, template | `tools/build_brand.py` |
| Shared helpers (FAQ, crumbs, dates, logo symbol) | `tools/build_studio.py` |
| Styles | `brand/css/brand.css` |
| Shared behaviour: nav, cursor, header theme, forms, burst, band drift | `brand/js/core.js` |
| Home behaviour | `brand/js/home.js` |
| Services and identity: before/after | `brand/js/inner.js` |
| Contact clock / booking / blog | `brand/js/pages.js`, `book.js`, `blog.js` (copied from `js/`) |
| Email, socials, availability, Calendly | `js/content.js` |
| Page template | `brand/_template/index.html` |
| Article template | `brand/blog/_template/index.html` |

---

## 16. Do and don't

| Do | Don't |
|---|---|
| Lead with red and one living shape | Turn the page into a rainbow |
| Use the icon alphabet as language | Add emoji, icon fonts or stock illustrations |
| Write one italic emotional word | Italicise whole headlines |
| Round corners, tilt slightly | Add drop shadows or gradients |
| Let visitors play (builder, flip, drag) | Hide content behind interactions |
| Keep grain and halftone texture | Use flat, sterile backgrounds |
| Show craft in case studies | Lead with metrics everywhere |
| Generate pages from `tools/` | Hand-edit generated HTML |
