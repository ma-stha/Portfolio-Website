# LOUD — Design Blueprint

**The rulebook for the bold red and black design of Manjil Shrestha's portfolio.**

Every page, section and component follows this document. When you add a page, start from the template (section 9). If something new doesn't fit a rule here, add the rule here first, then build it.

- **Live template:** `loud/_template/index.html` shows every standard block in the standard order.
- **Generator:** `tools/build_loud.py` (copy `page_template()`).
- **Styles:** `loud/css/loud.css`. Part 2 is the look; Part 1 is the structural base.

---

## Contents

1. [The idea in one paragraph](#1-the-idea-in-one-paragraph)
2. [Ten rules that never break](#2-ten-rules-that-never-break)
3. [Colour](#3-colour)
4. [Type](#4-type)
5. [Grid, spacing and lines](#5-grid-spacing-and-lines)
6. [Page architecture](#6-page-architecture)
7. [Component library](#7-component-library)
8. [Motion and interaction](#8-motion-and-interaction)
9. [How to add a new page](#9-how-to-add-a-new-page)
10. [How to add other things](#10-how-to-add-other-things)
11. [Writing style](#11-writing-style)
12. [SEO and accessibility](#12-seo-and-accessibility)
13. [Pre-launch checklist for every page](#13-pre-launch-checklist-for-every-page)
14. [File map](#14-file-map)
15. [Do and don't](#15-do-and-dont)

---

## 1. The idea in one paragraph

**Numbers are the heroes, and so is the name.** The site is printed in three flat colours: logo red, ink black and warm paper. Pages are stacks of full-width colour blocks. Headlines are tall, condensed and uppercase. Results are set enormous. Labels look like data readouts in a monospace font. Nothing is rounded, blurred, shadowed or gradient-filled. The signature is the hero: the name MANJIL drawn as a rising bar chart with a live trend line. It says "I make the line go up" before a single word is read.

---

## 2. Ten rules that never break

1. **Three colours only:** red `#F83232`, ink `#0A0A0A` and paper `#F2EFE9`. No greys as fills, no extra accents.
2. **Text on red is always black.** Never white, never grey, never red.
3. **Every section declares a theme:** red, dark or light. Colours inside follow the theme automatically (section 3).
4. **Headlines are Big Shoulders Display, uppercase, 800 to 900 weight, line-height 0.82 to 0.92.**
5. **One big number per block.** If a block has a result, it's the biggest thing in it.
6. **Lines are 2px solid ink.** Hairlines (1px) only for rows inside a list.
7. **Square corners, flat colour.** No `border-radius` (except the cursor, status dots and round avatars), no `box-shadow`, no gradients, no blur.
8. **Page rhythm:** red hero first, colour blocks alternate with light ones, and the page ends in black (CTA, then footer).
9. **Motion supports reading.** It reveals, never decorates. Everything works with motion off.
10. **Same content source.** Copy lives in `js/content.js` (home) and `tools/build_pages.py` (inner pages), never typed into generated HTML.

---

## 3. Colour

### Tokens (`:root` in `loud/css/loud.css`, Part 2)

| Token | Value | Use |
|---|---|---|
| `--signal` | `#F83232` | The logo red. Constant. Use for red **backgrounds** and red on dark. |
| `--red` | `#F83232`, but **ink inside red blocks** | The accent. Bullets, chart ends, meters, active states. Flips automatically. |
| `--red-ink` | `#D21C1C` on paper, ink in red, `#FF4A4A` in dark | Small red **text** (labels, numbers under 24px). |
| `--ink` | `#0A0A0A` | Text and dark blocks. |
| `--bg` | `#F2EFE9` | Paper. Light blocks, text on dark. |
| `--stone` | `#E4DFD6` | Rare: code background, highlighted search row. |
| `--mute` | Changes per theme | Secondary text. About 62–70% of the text colour. |
| `--rule` / `--rule-2` | Changes per theme | Hairline / stronger hairline. |

### Theme scopes

Put the theme on the `<section>`. Everything inside re-colours itself.

| Theme | How to declare | Background / text | Accent (`--red`) |
|---|---|---|---|
| **Red** | `data-theme="red"` or class `sec--stone` | red / ink | ink |
| **Dark** | `data-theme="dark"` or class `sec--ink` | ink / paper | red |
| **Light** | `data-theme="light"` or plain `sec` | paper / ink | red |

`.ph` (page hero) and `.art__head` (article header) are always red. `.cta` and `.ft` (footer) are always dark. The header and cursor read the theme under them and switch colour, so **an undeclared section breaks the header**.

### Proportion

On a full page: roughly **50% paper, 30% red, 20% black** by area. On the home page red and black are louder. On inner pages paper carries the reading.

### Contrast rules

- Ink on red: 5.2:1. Use freely.
- Paper on ink: 17.3:1. Use freely.
- Red on ink: 5.2:1. Fine for any size.
- Red on paper: 3.3:1. **Display sizes only (24px+).** For small red text on paper use `--red-ink` (4.7:1).
- Never paper text on red.

---

## 4. Type

### Families

| Role | Font | CSS variable | Weights |
|---|---|---|---|
| Display: headlines, big numbers, big words | Big Shoulders Display | `--display` | 800, 900 |
| Reading: body, leads, form inputs | Instrument Sans | `--sans` | 400, 500, 600 |
| Data labels: eyebrows, meta, buttons, nav | Martian Mono | `--mono` | 500, 600 |
| Long-form article body | Newsreader | `--serif` | 300–500 |

All four load from Google Fonts in `layout()` in `tools/build_loud.py`.

### Scale (desktop clamp values)

| Element | Class | Size | Line-height |
|---|---|---|---|
| Kinetic word (manifesto) | `.kin__w` | `clamp(4.4rem, 17vw, 19rem)` | 0.80 |
| Contact headline | `.contact__big` | `clamp(4.6rem, 17vw, 19rem)` | 0.80 |
| Hero name letters | `.nb__l` | `clamp(4rem, 15.5vw, 15rem)` | 0.80 |
| Result number | `.res__big` | `clamp(5.4rem, 15vw, 16rem)` | 0.78 |
| Inner page title | `.ph__title` | `clamp(3.4rem, 10.4vw, 12rem)` | 0.82 |
| CTA line | `.cta__line` | `clamp(3rem, 7.6vw, 8.4rem)` | 0.84 |
| Section title | `.sh__title` | `clamp(2.8rem, 6.6vw, 7.4rem)` | 0.86 |
| Home H1 | `.hero__h1` | `clamp(2.6rem, 5.8vw, 6.6rem)` | 0.84 |
| Card title | `.incl h3`, `.road h3` | `1.9rem` | 0.90 |
| Lead paragraph | `.ph__lead` | `clamp(1.15rem, 1.6vw, 1.5rem)` | 1.35 |
| Body | `body` | `17px` (16px mobile) | 1.5 |
| Label | mono role | `11.5px`, caps, `+0.04em` | 1.5 |

### Rules

- **Display text is always uppercase.** Use `text-transform`, not capitals typed in the source, so copy stays readable for search and screen readers.
- **Headlines: 2 to 8 words, end with a full stop.** One claim per headline.
- **Labels are always mono caps.** Add the class to the type-role list at the top of Part 2 instead of styling each label by hand.
- **Numbers use tabular figures** (already set on the display-number roles).
- Never set body text in the display font, and never set headlines in the sans.
- Outlined text (`-webkit-text-stroke: 2px`, transparent fill) is allowed for **one** big word per section, with a solid word next to it.

---

## 5. Grid, spacing and lines

- **Container:** `.wrap`, max width `1440px`, side padding `--pad` = `clamp(16px, 3vw, 40px)`.
- **Grid:** 12 columns, gap `--gap` = `clamp(12px, 1.6vw, 24px)`. Press **G** (or the footer button) to see it.
- **Section padding:** `.sec` = `clamp(80px, 10vw, 150px)` top and bottom. `.sec--tight` = `clamp(44px, 5vw, 70px)`.
- **Section head layout (`.sh`):** number in column 1, label in columns 2–3, title in columns 4–10, aside in columns 11–12. On tablet and phone the title and aside drop to full width.
- **Header height:** `--hd` = `64px` (58px on phones). Sticky elements offset by `var(--hd)`.
- **Lines:** list and block tops are `2px solid var(--ink)`. Rows inside lists use `1px solid var(--rule-2)`. Timeline tops (`.road`) are `6px`, and the first one is red.
- **Breakpoints:** `1100px` (tablet: nav becomes a menu, columns stack) and `760px` (phone: one column, horizontal tracks become swipeable).

---

## 6. Page architecture

### The standard inner page

Every new page uses this order. Drop blocks you don't need, but keep the colour order.

```
┌──────────────────────────────────────────┐
│ HEADER (fixed, takes the colour below)   │
├──────────────────────────────────────────┤
│ 1  RED HERO  .ph                         │  crumbs → giant title → meta | lead + actions | aside
├──────────────────────────────────────────┤
│ 2  LIGHT     .sec                        │  the main point (cards, problem, offer)
├──────────────────────────────────────────┤
│ 3  RED       .sec.sec--stone             │  how it works (steps)
├──────────────────────────────────────────┤
│ 4  LIGHT     .sec                        │  detail (timeline, table, story)
├──────────────────────────────────────────┤
│ 5  DARK      .sec.sec--ink               │  proof (numbers, tool, case study)
├──────────────────────────────────────────┤
│ 6  LIGHT     .sec                        │  pricing or next step
├──────────────────────────────────────────┤
│ 7  LIGHT     .sec  #faq                  │  FAQ (always the last content block)
├──────────────────────────────────────────┤
│ 8  DARK CTA  .cta                        │  one line + one button to /book/
├──────────────────────────────────────────┤
│ FOOTER (dark) giant MASTHA ✱             │
└──────────────────────────────────────────┘
```

### Rhythm rules

1. **The first block is always red** (`.ph`, `.art__head` or the home `.hero`).
2. **Never put two red blocks next to each other**, or two dark blocks, except at the very end (CTA plus footer).
3. **Two light blocks in a row are fine.** A 2px ink rule separates them automatically.
4. **At most three red blocks and three dark blocks per page**, not counting the hero, CTA and footer.
5. **Every content section has a section head** (`sec_head()`), numbered in order from 01.
6. **FAQ is always the last content block**, followed by the CTA.
7. **Pages always end in black:** CTA, then footer.

### The home page order (reference)

| # | Block | Theme | Purpose |
|---|---|---|---|
| — | `.hero` name chart | red | Who, what, where. H1 is "Digital marketing expert in Melbourne." |
| 01 | `.kin` manifesto | dark | Point of view: guesswork vs measured |
| 02 | `.results` Receipts | light | Proof first |
| 03 | `.svcs` service rows | light | What I do |
| 04 | `.about` route story | dark | Who I am |
| 05 | `.method` stacking cards | light | How I work |
| 06 | `#lab` growth model | dark | Interactive proof |
| 07 | `#experience` board | light | Track record |
| — | `.qt` quotes | red | Social proof |
| 08 | `#journal` | light | Expertise |
| 09 | `#faq` | light | Objections |
| — | `.contact` | dark | Conversion |

---

## 7. Component library

Class names in **bold** are the ones to use. Python helpers live in `tools/build_studio.py` (imported as `B`) and are overridden for LOUD in `tools/build_loud.py`.

### Page frame

| Component | Markup / helper | Notes |
|---|---|---|
| **Layout** | `layout(P, path, title, desc, active, body, scripts, ld)` | Head, fonts, header, menu, cursor, footer. `P` is the relative prefix (`''`, `'../'`, `'../../'`). |
| **Page hero** | `phero(P, trail, meta, title, lead, actions, aside)` | Red. Title is split into lines of about 14 characters. `meta` is a list of `"<span>Label</span>Value"`. `aside` holds one proof element. |
| **Crumbs** | `B.crumbs(P, [("Home",""), ("Page","page/")])` | Called by `phero`. |
| **Section head** | `sec_head(no, label, title, aside='')` | `(01)` · ■ LABEL · TITLE · aside. |
| **CTA band** | `cta(P, line, sub)` | Dark. One line, one red button to `/book/`. |

### Buttons and links

| Class | Looks like | Use |
|---|---|---|
| **`.btn.btn--red`** | Red block, black mono caps. Turns ink inside red blocks. | The primary action. One per block. |
| **`.btn.btn--ink`** | Ink block, paper text. Turns paper inside dark blocks. | Secondary or form submit. |
| **`.tlink`** | Mono caps with an underline and arrow | Tertiary links ("All articles"). |
| `ARR` | `→` that slides on hover | Put at the end of button labels. |

The hover is a colour fill that wipes up from the bottom while the button lifts 3px.

### Content blocks

| Block | Markup | When |
|---|---|---|
| **Card grid** | `<ol class="incl"><li class="rv"><span>01</span><h3>…</h3><p>…</p></li></ol>` | 3 to 6 features or inclusions. 3 columns. |
| **Steps** | `<ol class="steps"><li class="step rv"><span class="step__n">01</span><h3>…</h3><p>…</p></li></ol>` | A process of 3 to 5 steps. Best in a red block. |
| **Timeline** | `<ol class="road"><li class="rv"><span class="rd__when">Month 1</span><h3>…</h3><p>…</p></li></ol>` | Phases over time. 4 columns. |
| **Pain points** | `<ol class="pains"><li class="rv"><span>a.</span><p><strong>…</strong> …</p></li></ol>` | 3 problems the reader recognises. |
| **Ticks list** | `<ul class="ticks"><li>…</li></ul>` | Deliverables. Square red bullets. |
| **KPI row** | `<dl class="kpis kpis--row"><div><dt>Label</dt><dd>+212%</dd></div></dl>` | 3 or 4 proof numbers. Best in a dark block. |
| **Pricing** | `B.plans_html(P, plans)` | Exactly 3 plans. The middle one is `hot` (dark, "Most chosen"). |
| **Comparison table** | `<div class="tablewrap"><table class="cmp">…</table></div>` | Under pricing. |
| **FAQ** | `B.faq([(q, a), …])` + `B.faq_ld(items)` in `ld` | 3 to 6 questions. Always add the JSON-LD. |
| **Journal rows** | `B.journal_rows(P, posts)` | Article lists. The row turns red on hover. |
| **Contact form** | `B.contact_form("Subject")` | Uses Formspree when `YOUR_FORM_ID` is replaced. Until then it opens the visitor's email app. |
| **Line chart** | `B.line_chart(series, W, H, label)` | Case studies. Line draws in on reveal. The end dot is red. |
| **Poster** | `poster(seed, BIG, small, variant)` | Generated covers. Variants: 0 red, 1 ink, 2 paper. |

### Home-only signature pieces

| Piece | Classes / ids | Script |
|---|---|---|
| Name chart | `.namechart#namechart`, `.nb[data-base]`, `#ncPoly`, `#ncDot`, `#ncTag` | `home.js`: name chart |
| Kinetic manifesto | `.kin`, `.kin__w--old`, `.kin__strike`, `.kin__w--new` | `home.js`: manifesto |
| Receipts track | `.results`, `#resTrack`, `.res.res--0…3`, `.res--end` | `home.js`: receipts |
| Service rows | `.svcs__rows`, `.srow[style=--d:±1]`, `.srow__w` | `home.js`: drift |
| Route story | `.about`, `.route`, `#rt` | SVG `animateMotion` |
| Stacking cards | `.method__stack`, `.mt.mt--0…2[style=--i:n]` | CSS `position: sticky` |
| Growth model | `#lab`, `#iV #iC #iA #iL`, `#rY`, `#labSvg` | `home.js`: growth model |
| Experience board | `.board`, `.sb` | Row turns red on hover |
| Quotes | `.qt`, `.qt__item`, `#qPrev #qNext #qCount` | `home.js`: quotes |

These are signatures. **Don't reuse them on inner pages.** Each appears once on the site, which is why it's memorable.

### Article components (blog posts)

`.tldr` · `.callout` (`--warn`) · `.stat-row` · `.figure` · `.table-wrap` · `.checklist` · `<blockquote>` (red bar, display caps) · margin notes (`.side`) · `.byline` · `.pn` (previous/next). See `loud/blog/_template/`.

---

## 8. Motion and interaction

| Effect | Where | Rule |
|---|---|---|
| **Line reveal** | `.ln > span` in hero titles | Slides up from a mask, 1.15s `expo.out`, staggered 0.08s. Only on the first screen and the contact headline. |
| **Fade up** | `.rv` (scroll), `.in` (on load) | 34px up and fade in, 0.9s. Put `.rv` on titles, cards and rows. |
| **Count up** | `data-count="172"` | Numbers count from 0 when 60% visible. |
| **Pinned scrub** | Manifesto, Receipts | Home only. Desktop and phone for the manifesto; desktop only for Receipts. |
| **Hover fill** | Buttons, journal rows, board rows, service rows | Red or colour fill wipes in; text stays black on red. |
| **Cursor** | All pages, mouse only | A dot. It becomes a ring over links and a filled label circle over `[data-cursor="Label"]`. It hides over form fields. |
| **Header** | All pages | Hides on scroll down, returns on scroll up, takes the colour of the block under it. |

**Rules**

- Easing: `cubic-bezier(.2,.8,.1,1)` (`--ease`) for most things, and `--spring` for the button lift and cursor.
- Durations: 0.2–0.35s for hovers, 0.45–0.9s for reveals, and up to 1.2s for hero lines.
- `prefers-reduced-motion`: everything is shown at once, with no pinning, no drift and no spinning star. Already handled; keep it that way for anything new.
- Add `data-cursor="Verb"` only to big targets (cards, panels, rows). One or two words: "Explore", "Read", "Let's go".

---

## 9. How to add a new page

Example: an "About" page at `/about/`.

**Step 1. Copy the template function.** In `tools/build_loud.py`, copy `page_template()` and rename it:

```python
def about():
    P = '../'                 # one folder deep → '../'   two deep → '../../'
    path = 'about/'
    fq = [("Question?", "Answer.")]
    body = phero(P, [("Home", ""), ("About", path)],
                 ["<span>Based</span>Melbourne", "<span>Since</span>2020", "<span>Focus</span>Revenue"],
                 "From Kathmandu to Melbourne.",
                 "Short lead: who this page is for and what they'll learn.",
                 f'<a class="btn btn--red" href="{P}book/">Book a free consultation {ARR}</a>') + f'''

    <section class="sec" data-theme="light">
      <div class="wrap">
        {sec_head(1, "Story", "One spreadsheet at a time.")}
        ...
      </div>
    </section>

    <section class="sec" data-theme="light" id="faq">
      <div class="wrap faq">{sec_head(2, "FAQ", "Straight answers.")}{B.faq(fq)}</div>
    </section>

{cta(P)}'''
    write(path + 'index.html', layout(P, path,
          'About Manjil Shrestha | Digital Marketing Expert in Melbourne',   # title
          'Meta description, 140 to 160 characters, with the keyword.',       # description
          'about',                                                           # active nav key
          body, ['pages.js'], [B.faq_ld(fq)]))
```

**Step 2. Call it** in the `if __name__ == '__main__':` block at the bottom: `about()`.

**Step 3. Add it to navigation** (optional). Add `('About', 'about/', 'about')` to `NAV` in `tools/build_loud.py`. Keep the main nav to **five items or fewer**. Otherwise link it from the footer `Site` column in `layout()`.

**Step 4. Put the copy in the right place.** Short, page-specific copy can live in the function. Anything shared with the main site belongs in `tools/build_pages.py` or `js/content.js`.

**Step 5. Rebuild and check.**

```bash
python3 tools/build_loud.py
```

```bash
python3 -m http.server 8000
```

Open `http://localhost:8000/loud/about/` and run the checklist in section 13.

### Choosing blocks for a new page

| Page type | Recommended blocks after the hero |
|---|---|
| Service page | Pains (light) → What's included `.incl` (red) → Timeline `.road` (light) → Case study, KPIs and chart (dark) → Pricing (light) → FAQ → CTA |
| About / story | Story text (light) → Values `.incl` (red) → Timeline of career `.road` (light) → Numbers `.kpis` (dark) → FAQ → CTA |
| Case study | Challenge (light) → Approach `.steps` (red) → Results `.kpis` and chart (dark) → What's next (light) → CTA |
| Landing / offer | Pains (light) → Offer `.incl` (red) → Proof `.kpis` (dark) → One plan (light) → FAQ → CTA |
| Utility (legal, thanks, 404) | Red hero (short title) → one light block → CTA |

---

## 10. How to add other things

- **A blog post:** add an entry to `POSTS` in `tools/build_pages.py` and run `python3 tools/build_loud.py`. The card, journal rows and article page are generated. Use the components listed in section 7 (Article components).
- **A service page:** follow section 9 with the "Service page" recipe. `B.seo()` in `tools/build_studio.py` is the full working example.
- **A home section:** add it inside `home()` in `tools/build_loud.py`. Give the `<section>` a `data-theme`, an `id` and a `sec_head()`, and place it so it obeys the rhythm rules in section 6. If it needs styling, add a commented block to Part 2 of `loud/css/loud.css` under the `HOME` heading.
- **A new component:**
  1. Check section 7 first. Most needs are covered.
  2. If not, name it in BEM style (`.thing`, `.thing__part`, `.thing--variant`).
  3. Style it with tokens only (`var(--ink)`, `var(--red)`, never hex values) so it re-colours in red and dark blocks.
  4. Make the borders 2px and the corners square.
  5. Add its labels to the mono type-role list and its titles to the display list.
  6. Test it in all three themes.
  7. Document it in section 7 of this file.
- **New colours or fonts:** don't. If the brand changes, change the tokens in Part 2 `:root` only.

---

## 11. Writing style

- **Voice:** direct, confident, specific. Write as one person ("I"), not a team ("we").
- **Headlines:**
  - Make one claim, usually with a number or a contrast: "Six ways to make the line go up." or "Numbers, not adjectives."
  - Keep them to 2 to 8 words and end with a full stop.
- **Leads:** 1 to 2 sentences that say who it's for and what changes for them.
- **Labels:** 1 to 3 words, nouns: "Track record", "Pricing", "Proof".
- **Buttons:** verb first, 2 to 5 words: "Book a free consultation", "Start with a call".
- **Numbers:** always with context: "+212% organic leads", not "+212%".
- **Banned:** "unlock", "elevate", "supercharge", "cutting-edge", "seamless", "game-changer", "in today's digital landscape", and exclamation marks.
- **Demo content:** anything not real is labelled as demo. Replace it before launch.

---

## 12. SEO and accessibility

**SEO**
- Title format: `Topic | Manjil Shrestha`, or `Service in Melbourne | Manjil Shrestha`. Under 60 characters.
- Meta description: 140–160 characters, with "digital marketing" and "Melbourne" where natural.
- **One `<h1>` per page.** In LOUD it's the `.ph__title` (or `.hero__h1` on home). Section titles are `<h2>`, cards are `<h3>`.
- JSON-LD: FAQ pages pass `B.faq_ld()`. Add `Service`, `BlogPosting` or `Person` where relevant.
- LOUD is a **design option**: pages are `noindex` with canonical URLs pointing to the main site, and `/loud/` is disallowed in `robots.txt`. If LOUD becomes the main site:
  1. Move its files to the root.
  2. Remove `noindex` in `layout()`.
  3. Update `sitemap.xml`.

**Accessibility**
- **Contrast:** follow the rules in section 3. Never put paper on red, and use red text on paper only at display sizes.
- **Focus:** a visible 3px outline in the accent colour. Never remove it.
- **Display text:** split lines carry an `aria-label` with the full title. Decorative SVGs have `aria-hidden="true"`.
- **Controls:**
  - Buttons are `<button>`, links are `<a>`.
  - FAQ toggles use `aria-expanded` and `aria-controls`.
  - The menu uses `aria-hidden`.
- **Keyboard:** everything works by keyboard. The custom cursor is mouse-only and never replaces focus styles.
- **Reduced motion:** honoured everywhere (section 8).
- **Images:** real `alt` text. The portrait's `width` and `height` are set to prevent layout shift.

---

## 13. Pre-launch checklist for every page

**Design**
- [ ] The first block is red, and the page ends with the dark CTA and footer.
- [ ] No two red or two dark blocks touch (except CTA and footer).
- [ ] Every section has a `data-theme` or `sec--stone`/`sec--ink` class.
- [ ] Every section head is numbered in order from 01.
- [ ] Each block has one main idea, one biggest element and at most one primary button.
- [ ] Only the three colours. No radius, shadow or gradient.
- [ ] Headlines are display caps, 2–8 words, and end with a full stop.

**Build**
- [ ] The page is generated by `tools/build_loud.py`; nothing is hand-edited in `loud/**/index.html`.
- [ ] `P` and `path` are correct, and all links work.
- [ ] One `<h1>`. Title and description are written.

**Test**
- [ ] Width 390px: no sideways scroll, text not cut off, buttons are reachable.
- [ ] Width 1280px and 1440px: grid aligns (press G).
- [ ] No console errors.
- [ ] Keyboard: Tab through the page; focus is always visible.
- [ ] Reduced motion on: everything is visible.

---

## 14. File map

| What | File |
|---|---|
| This blueprint | `loud/DESIGN-BLUEPRINT.md` |
| Overview | `loud/README.md` |
| Generator: layout, hero, CTA, home page, page template | `tools/build_loud.py` |
| Shared inner-page structure and helpers (imported) | `tools/build_studio.py` |
| Inner page content: services, prices, FAQs, posts | `tools/build_pages.py` |
| Home content: numbers, case studies, process, FAQ… | `js/content.js` |
| Styles (Part 1 base, Part 2 LOUD look) | `loud/css/loud.css` |
| Shared behaviour: nav, cursor, header theme, forms, reveals | `loud/js/core.js` |
| Home behaviour: name chart, manifesto, receipts, lab, quotes | `loud/js/home.js` |
| Services, SEO, contact behaviour | `loud/js/pages.js` (copied from `js/pages.js`) |
| Booking widget | `loud/js/book.js` (copied from `js/book.js`) |
| Blog filters and table of contents | `loud/js/blog.js` (copied from `js/blog.js`) |
| Page template (all blocks, in order) | `loud/_template/index.html` |
| Article template (all article components) | `loud/blog/_template/index.html` |
| Logo symbol | `tools/symbols.txt` (`#logo`, `#star`) |

Build everything:

```bash
python3 tools/build_loud.py
```

---

## 15. Do and don't

| Do | Don't |
|---|---|
| Let one number or word be enormous | Make everything medium-sized |
| Use full-width colour blocks | Use floating cards with shadows |
| Keep text on red black | Put white or grey text on red |
| Use 2px ink rules | Use soft grey borders and rounded boxes |
| Write labels in mono caps | Mix in a fifth font or italics in headlines |
| Show proof (numbers, charts, receipts) | Use stock photos, icons, emoji or illustrations |
| Keep each signature piece unique | Copy the name chart or manifesto onto other pages |
| Generate pages from `tools/` | Hand-edit generated HTML |
| Test at 390, 1280 and 1440px | Only check on a laptop |
