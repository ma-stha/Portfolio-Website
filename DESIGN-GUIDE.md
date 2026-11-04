# Design Guide: "Signal on Paper"

The rulebook for every page and every edit on this site. If something new follows this guide, it will look like it was always part of the site.

Read sections 1 and 2 before touching anything. The rest is reference.

---

## 1. The idea

**A data marketer's desk, printed in two inks.**

The site looks like printed things on grey-white paper: reports, receipts, tickets, stickers, tape and stamps. It is printed in only two inks, black and one loud red taken from the MANJIL logo. Everything is cut out, stuck down, slightly crooked, and casts a hard black shadow.

The personality is **confident, direct and a bit playful**. Big shouty headlines carry the confidence. Hard numbers carry the credibility. Stickers and starbursts carry the play.

Why it works for the brand: it feels physical and honest, like evidence on a desk. That matches the promise, "measured, not guessed".

---

## 2. The ten rules

These are non-negotiable. If an idea breaks one of them, change the idea.

1. **Two inks only.** Black (`--ink`) and red (`--red`) on paper. No new colours, no gradients between colours, no blues, purples or greys beyond the paper tones.
2. **Red is a signal, not a wallpaper.** Use it for the one thing that matters in each block: the key word, the main button, the winning number, the last bar in a chart.
3. **Everything solid has a 2px black border and a hard shadow.** Shadows are never blurred. They are offset black blocks, or red on dark backgrounds.
4. **Display type is heavy, condensed and UPPERCASE.** Anybody, always with `font-variation-settings`. Body copy is never uppercase.
5. **Every section headline highlights one word** with the red highlighter bar (`.hi`) or a red block (`.blk`). One word or short phrase, never a whole line.
6. **Nothing sits perfectly straight.** Cards, stickers, tickets and quotes tilt between 0.4° and 4°. Alternate the direction. Hover straightens them.
7. **Paper texture everywhere.** The body has the paper tile and the grain overlay. Card surfaces use `.paper` so they get the texture too.
8. **The starburst ✱ is the signature.** Use it for bullets, icons, loaders, the cursor and celebrations. Don't invent other decorative symbols.
9. **Numbers are the heroes.** Results, prices and scores are set big in the display face. Labels around them are small Space Mono capitals.
10. **Motion is springy and physical.** Things pop, tilt and snap back. Nothing fades in slowly or floats.

---

## 3. Colour

### Tokens

All colours live as CSS variables in `css/styles.css`. Never hard-code a hex in a component. Use the variable.

| Token | Hex | Use it for |
|-------|-----|-----------|
| `--paper` | `#E9E7E1` | Page background. The "desk". |
| `--paper-hi` | `#F5F4F0` | Card surfaces, inputs' surroundings, text on black or red. |
| `--paper-lo` | `#DCD9D1` | Image placeholders, recessed areas. |
| `--ink` | `#0B0B0B` | Text, borders, shadows, black bands, icon tiles. |
| `--muted` | `#5E5B55` | Secondary body text on paper only. |
| `--red` | `#F83232` | Highlights, primary buttons, red bands, chart accents. Sampled from the logo. |
| `--red-deep` | `#D61F1F` | Small red text (labels, negative numbers) on light cards. |
| `--line` | ink at 16% | Dashed dividers inside cards. |

Two extra surface tones exist for specific objects only. `#FBFAF7` is receipt and ticket paper. `#FFF6C9` is sticky-note yellow. Don't use either for anything else.

### Proportions

Aim for roughly **70% paper, 20% black, 10% red** on any screen. If red covers more than a quarter of the viewport, something is wrong. The one exception is a full red band, such as the CTA or numbers band, used at most once per page.

### Contrast rules

These numbers are measured. Follow them so the site stays readable.

| Combination | Contrast | Rule |
|-------------|----------|------|
| Ink on paper | 15.9 : 1 | Default for all text. |
| Paper-hi on ink | 17.9 : 1 | Default on black bands. |
| Ink on red | 5.2 : 1 | All text on red buttons, bands and tags must be ink. |
| Red on ink | 5.2 : 1 | Fine for numbers and accents on black. |
| Muted on paper | 5.5 : 1 | Fine for secondary text. |
| Paper-hi on red | 3.5 : 1 | **Large display text only**, such as the `.hi` highlighted word. |
| Red on paper | 3.1 : 1 | **Large display text only.** Never body or small labels. |
| Red-deep on paper-hi | 4.7 : 1 | Small red labels, but only inside light cards. |
| Muted on red | 1.8 : 1 | **Never.** Grey text on red is unreadable. |

On red surfaces, everything is ink. That includes tags and paragraphs inside red cards.

---

## 4. Typography

### The five faces

| Role | Font | Variable | Notes |
|------|------|----------|-------|
| Display | **Anybody** | `--f-display` | Headlines, big numbers, card titles, prices. Always uppercase, always heavy and condensed. |
| Body | **Archivo** | `--f-body` | Paragraphs, buttons, navigation. Normal case. |
| Data | **Space Mono** | `--f-mono` | Labels, dates, metadata, chart text, receipt text. Usually small capitals with letter-spacing. |
| Pixel accent | **Silkscreen** | `--f-pixel` | Only on stickers, such as "DATA > VIBES". Echoes the blocky logo. Never in body copy. |
| Handwriting | **Caveat** | `--f-hand` | Only for sticky notes and chart annotations. Reads as the author's own scribble. |

### Display settings

Anybody is a variable font. Always set weight and width together with `font-variation-settings`. Use these pairs, from heaviest to lightest:

| Use | Setting | Size |
|-----|---------|------|
| Page hero title | `"wght" 900, "wdth" 80` | `clamp(2.9rem, min(8.2vw, 13vh), 9rem)`, line-height .86 |
| Section headline `.h2` | `"wght" 850, "wdth" 85` | `clamp(2.3rem, 5.4vw, 4.8rem)`, line-height .95 |
| Big numbers and prices | `"wght" 900, "wdth" 75–80` | 2.2rem to 6.6rem |
| Card titles | `"wght" 880, "wdth" 85` | 1.2rem to 1.9rem |
| Article headings | `"wght" 900, "wdth" 84` | `clamp(1.7rem, 3vw, 2.4rem)` |
| Quotes and pull text | `"wght" 650–850, "wdth" 85–92` | 1.15rem to 2rem |

Letter-spacing on display text is slightly tight (`-0.02em` to `-0.03em`). Line-height is very tight (0.86 to 0.95). Headlines stack, they don't flow.

### Small text

- **Section label** (`.label`): Space Mono, 0.78rem, uppercase, letter-spacing 0.14em, with a short black rule before it. Format: `03 — Services`.
- **Card label** (`.label-sm`): Space Mono, 0.7rem, bold, uppercase, red-deep.
- **Metadata**: Space Mono, 0.68 to 0.76rem, uppercase.

### Body

Archivo at 17px (16px on phones), line-height 1.55. Articles use 1.12rem with line-height 1.72. Keep line length under about 60 characters (`max-width: 52ch` to `62ch`).

---

## 5. Surfaces, borders and shadows

### The paper stack

1. **The desk**: `body` uses `--paper` plus the tiled `assets/img/paper.png`.
2. **The grain**: `.grain` is a fixed, animated noise layer over everything, including red and black areas. It is what makes flat colours feel printed. Never remove it.
3. **Cards**: add the `.paper` class. It gives the lighter paper, the texture, a 2px ink border and a 6px hard shadow.

### Borders

One weight: `--b` (2px solid ink). Dashed dividers inside cards use 1.5–2px dashes in ink or `--line`. Don't use 1px borders on cards.

### Shadows

Shadows are **solid offset blocks, never blurred**.

| Token | Value | Use |
|-------|-------|-----|
| (small) | `3px 3px 0 ink` | Tags, small buttons, calendar days |
| (button) | `4px 4px 0 ink` | Buttons, slots, tools |
| `--sh` | `6px 6px 0 ink` | Standard cards |
| `--sh-lg` | `10px 10px 0 ink` | Hero objects, big blocks, CTA band |
| `--sh-red` | `8px 8px 0 red` | Black objects, such as code blocks and the clock card |
| Hover | `9–14px` offset in **red** | Cards on hover switch their shadow to red |

On black bands, light cards use a **red** shadow so they still read as lifted.

Shapes with a torn edge (tickets, receipts) use `clip-path`, which cuts off `box-shadow`. Wrap them and use `filter: drop-shadow(…)` on the wrapper instead (see `.plan-wrap` and `.slip`).

### Tilt

| Object | Tilt |
|--------|------|
| Large cards (services, files) | ±0.4° |
| Grid cards (blog, contact methods) | ±0.6° to 1.2°, alternate by `nth-child` |
| Tickets, stat cards, quotes | ±1° to 2° |
| Stickers, stamps, badges | ±4° to 14° |
| Red block behind a title word | -1.6° |

On hover, cards straighten to 0° and lift with `translate(-3px, -3px)`. Body text blocks, forms and the article column don't tilt, except the home contact form at 0.8°.

---

## 6. Layout

- **Container**: `.container`, max 1320px, side gutter `clamp(16px, 4vw, 56px)`.
- **Section spacing**: `.section` is `clamp(90px, 11vw, 160px)` top and bottom. Inner pages use `.section--tight`, `clamp(64px, 8vw, 110px)`.
- **Grids**: 12-column thinking, but most layouts are 2 columns (1.1fr / 0.9fr or 1.3fr / 0.7fr) or 3 to 4 equal cards. Card gaps are 18 to 26px. Bigger than usual, so shadows and tilts have room.

### Section anatomy

Every section opens the same way:

```html
<section class="section">
  <div class="container">
    <div class="head">                      <!-- or "head head--row" to put the lead on the right -->
      <p class="label reveal">04 — Growth lab</p>
      <h2 class="h2 reveal">What's a better funnel <span class="hi">worth</span>?</h2>
      <p class="lead reveal">One or two sentences. Plain, direct, useful.</p>
    </div>
    <!-- content -->
  </div>
</section>
```

### Page rhythm

Alternate surfaces so long pages have a beat:

**paper → paper → black band → paper → red band (CTA) → black footer**

- Use **black bands** (`.band--ink`) for process, timelines and "how it works", at most twice per page.
- Use a **red band** (`.band--red` or `.cta-band`) once per page, usually the final call to action.
- Use **tapes** (crossing red and black marquee strips) only on the home page, as a section divider.

### Page hero (inner pages)

Every inner page starts with the same structure, generated by `tools/red_parts.py`:

1. **Masthead strip**: a thin bordered row in Space Mono with the page name, tagline, Melbourne clock and "Open for work".
2. **Breadcrumbs**: Space Mono capitals, current page in red-deep.
3. **Label, then a giant title.** The last line or key word sits in the tilted red `.blk`.
4. **Lead paragraph**, then CTA buttons and/or a row of `.tag` chips.
5. **One or two draggable stickers.** Place them in empty space, never over the title or lead.

---

## 7. Components

Use these before inventing anything. Class names are in brackets.

### Buttons (`.btn`)

Pill-shaped, 2px border, 4px hard shadow. On hover they lift up and left. On press they push down into the shadow.

| Variant | Use |
|---------|-----|
| `.btn--red` | The single primary action in a block, such as "Book a call". |
| `.btn--ink` | A strong secondary action, or the primary action on a red surface. |
| `.btn--paper` | Secondary actions. |
| `.btn--sm`, `.btn--lg`, `.btn--block` | Sizes. |

Add `data-magnetic` so the button follows the cursor slightly. End primary labels with `→` or the ✱ star icon. One red button per block.

### Highlights

- **`.hi`**: the red highlighter bar behind one word in a headline. It wipes in when the headline scrolls into view. Text turns paper-white.
- **`.blk`**: a bordered, shadowed, tilted red block around a word in a page title.
- **`<mark>`**: a soft red underline highlight for a phrase inside body text.
- **`.outline`**: outlined display text with a hard shadow. Use sparingly, at most once per page.

### Tags (`.tag`, `.tag--red`, `.tag--ink`)

Small pill labels in Space Mono capitals with a 3px shadow. Use them for categories, facts and filters. Text inside is always ink, except paper-hi on `.tag--ink`.

### Cards (`.paper`)

The default container for anything grouped. Common patterns:

- **Icon tile**: 60px black square with a red line icon. On card hover it flips to red with a black icon and tilts.
- **Card title**: Anybody, uppercase.
- **Ticked list** (`.ticks`): each item starts with a red ✱, separated by dashed lines.
- **Card footer**: a dashed top border, then KPI chips and small facts.

### Tickets and receipts

Paper with a **torn zig-zag bottom edge**. Use them for anything that feels like a transaction or a result:

- **Pricing** (`.plan-wrap > .plan`): the popular plan is red, with a black "Most popular" badge.
- **Campaign receipt** (home hero): dotted leaders between label and number, dashed rules, a barcode, "THANK YOU FOR GROWING".
- **Score slip** (`.slip`): the SEO health check result.

### Stickers (`.sticker`)

Draggable on desktop, absolutely positioned with `--x`, `--y` and `--r`. They pop in after the hero animates. Hidden on phones on inner pages.

| Type | Look | Use |
|------|------|-----|
| `.sticker--badge` | Black circle, rotating text ring, red star | A promise: "OPEN FOR WORK", "FREE CALL" |
| `.sticker--tag` | Paper rectangle, pixel font | A joke or motto: "DATA > VIBES" |
| `.sticker--pill` | Red pill | A quick fact: "GA4 ✓ certified", "Rank #1 ↗" |

At most two stickers per hero, and none in the middle of a page.

### Stamps (`.stamp`)

Round, double-ringed rubber stamps in Space Mono capitals ("Melbourne ✱ Based", "Verified ✓ Certified"). Use them sparingly as a seal of trust on a card corner. Rotate 10° to 15°.

### Tape (`.tape-bit`)

Short strips of red or black tape that pin photos and notes to the page. Place them across corners at ±25° to 30°.

### Sticky notes (`.sticky`)

Yellow paper, Caveat handwriting, red tape on top, slight tilt. They sit in the margin beside article paragraphs, or inline on smaller screens. Use them for asides with personality: a joke, a war story, an opinion. At most three per article.

### FAQ (`.faq__item`)

Uppercase display questions with a black star that spins red when opened. Bound automatically by `core.js`. Questions double as FAQ schema for Google.

### Forms (`.form`, `.field`, `.chips`)

White inputs with 2px borders and square corners. On focus they lift and get a red shadow. Field labels are Space Mono capitals. Choice chips turn black and tilt when selected. Errors use a red border and red shadow.

### Call-to-action band (`.cta-band`)

A red block with a faint grid, black border, large shadow and a faded spinning star in the corner. Headline in display type, one line of support, one or two buttons. Use one per page, near the end.

---

## 8. Signature details

- **The starburst ✱** (`#star` SVG symbol). Use it for list bullets, icon accents, the loader, the cursor, badges and the confirmation icon. Clicking a star bursts it into mini red and black stars (`data-pop`, or `UV.burst()` in code).
- **The logo** (`#logo` SVG symbol). Black on paper, paper-white on black. The star inside the logo is always red. Never stretch it, recolour the star, or put it on red. The footer shows it full-width.
- **The live dot** (`.live`). A pulsing red dot that means "now": Melbourne clock, "Open for work", availability.
- **Melbourne clock.** The masthead and nav show live Melbourne time. It reinforces the local keyword.
- **Generated chart art.** When there is no photo, use a printed-chart cover: light grey grid, black-hatched bars, a red trend line with a black offset shadow, and a red last bar with a red dot. See `cover_svg()` in `tools/red_parts.py`.

---

## 9. Charts and data graphics

Every chart follows the same print style:

- **Background**: `#E4E1DA` with a faint 9% black grid, or the paper card itself.
- **Bars**: black-hatched pattern with a 2px black outline. Highlight one bar or series in solid red.
- **Lines**: red, 3 to 5px, with a black copy offset by 4px as a shadow.
- **Points**: red diamonds (rotated squares) or circles with a black outline.
- **Reference lines**: black, dashed.
- **Labels**: Space Mono capitals, small, in black.
- **Annotations**: Caveat handwriting in red-deep or black, with an arrow: "fixes shipped →".
- **Captions**: below the chart in Space Mono capitals, starting "Fig. 1 ·". Label demo data as illustrative.

No pie charts, 3D or gradients.

---

## 10. Icons

- Simple line icons on a 24px grid, 2 to 2.4px stroke, square or mitred joins. Solid shapes only for bar-chart style icons.
- Icons sit inside the 60px black tile with the icon in red, or inline at text size in ink.
- Reuse the icon set in `ICONS` in `tools/build_pages.py` before drawing new ones.

---

## 11. Photography and images

- **Portraits** go in a polaroid frame: paper border, tape on two corners, handwritten caption. Shown **black and white**, turning to colour on hover.
- **Profile picture**: the red-ring avatar (`assets/img/avatar.png`), always circular with a 2px black border.
- **Case study and blog covers**: real screenshots or photos if you have them. Otherwise use generated chart art. Covers sit inside a bordered frame with a red category tag in the top-left corner.
- No stock photos of handshakes, laptops or smiling teams. They break the "printed evidence" idea.

---

## 12. Motion

| Thing | Behaviour |
|-------|-----------|
| Easing | `--ease` (smooth out) for movement. `--spring` (overshoot) for anything that pops, tilts or straightens. |
| Scroll reveal | `.reveal`: rises 34px with a 0.6° tilt and settles. Add it to heads, cards and list items. |
| Headline highlight | `.hi` wipes in from the left when its headline is revealed. |
| Page title | Lines slide up from below. The red `.blk` wipes in left to right. Stickers pop in last. |
| Hover on cards | Straighten, lift 3–5px, shadow turns red. |
| Hover on buttons | Lift 2px with a bigger shadow, arrow nudges right, star spins. |
| Cursor | A spinning red starburst, larger over links, with a black label ("Read", "Drag me"). It turns black over red areas. Desktop only. |
| Counters | Numbers count up when they scroll into view. |
| Celebrations | Star bursts on form send, email copy and booking confirmation. |
| Smooth scroll | Lenis plus GSAP ScrollTrigger, already set up in `core.js` and `main.js`. |

**Reduced motion:** everything must work with `prefers-reduced-motion: reduce`. Content shows instantly, highlights appear without the wipe, and nothing spins or bursts. The stylesheets already handle this. New animations must check `UV.reduce` in JS or sit inside the existing reduced-motion block in CSS.

---

## 13. Writing style

The design is loud, so the words are calm and precise.

- **Headlines**: short and punchy, often a twist on a phrase: "Results, not reports." "A loop, not a launch." Highlight the twist word.
- **Body**: short sentences in Australian English. Say what happens and what it's worth.
- **Numbers over adjectives**: "+212% organic enquiries", not "huge growth".
- **Labels**: two to four words in Space Mono capitals.
- **Calls to action**: verb first, specific: "Book a free 30-min call", not "Learn more".
- **Personality** goes in stickers, sticky notes and chart annotations. Keep the main copy professional.
- Mark demo numbers and testimonials as demo until they're real.

---

## 14. Accessibility checklist

- Follow the contrast table in section 3. Ink on red, never grey on red.
- Every interactive element has a visible focus style: a 3px red outline, already global.
- Decorative elements (stickers, stars, tapes, charts without data value) get `aria-hidden="true"`.
- Headlines split into animated lines keep the full sentence in `aria-label`.
- Images have real alt text. Decorative images use `alt=""`.
- Tap targets are at least 40px.
- The page works without JavaScript: content is visible because `.js` hiding only applies when JS has loaded.

---

## 15. Responsive behaviour

| Breakpoint | Changes |
|------------|---------|
| ≤ 1180px | Nav links collapse into the red full-screen menu. |
| ≤ 1024px | Two-column layouts stack. Sticky side panels become static. Article table of contents becomes a collapsible box. Sticky notes move inline. |
| ≤ 760px | Grids become one column. Tilts on grid cards are removed so edges line up. Hero stickers are hidden on inner pages. Display sizes scale down. |

Check every new page at 390px, 1280px and 1440px wide. There must be no sideways scroll at any width.

---

## 16. Building a new page

1. **Inner pages are generated.** Add the page function in `tools/` (copy `tools/service_seo.py` for a service page). Run `python3 tools/build_pages.py`. The shared layout, nav, footer, masthead, stickers and SEO tags come from `tools/red_parts.py` automatically.
2. **Start from the anatomy**: page hero, then three to six sections that each open with label, headline with one `.hi` word, and lead.
3. **Pick components from section 7.** Only create a new one if nothing fits, and build it from the same parts: paper, 2px border, hard shadow, slight tilt, display title, mono labels, one red accent.
4. **Plan the rhythm**: at most two black bands, one red CTA band at the end.
5. **Add stickers** to the hero in `STICKERS` in `tools/red_parts.py`, at most two.
6. **Write the copy** following section 13.
7. **Check it**: no new colours, contrast rules met, works at 390px, reduced motion respected, no console errors, no sideways scroll.

### New component checklist

- [ ] Uses only `--paper`, `--paper-hi`, `--ink`, `--red` (and `--red-deep` for small text)
- [ ] 2px ink border and a hard, unblurred shadow
- [ ] Slight tilt that straightens on hover
- [ ] Display title in Anybody uppercase with variation settings
- [ ] Labels and metadata in Space Mono capitals
- [ ] Exactly one red accent
- [ ] Spring easing on hover and pop-in
- [ ] Readable at 390px and with reduced motion

---

## 17. Do and don't

| Do | Don't |
|----|-------|
| Use red for one thing per block | Paint large areas red, except one CTA band |
| Hard offset shadows | Soft, blurred drop shadows |
| Slight, alternating tilts | Wild rotations on readable content |
| Heavy uppercase display headlines | Uppercase paragraphs |
| One highlighted word per headline | Highlighting whole sentences |
| Numbers as the visual hero | Vague claims without figures |
| Ink text on red | Grey or white small text on red |
| The ✱ star for bullets and accents | Emoji, checkmarks or new symbols as decoration |
| Generated chart art when there's no image | Stock photos |
| Paper texture on every surface | Flat white backgrounds |
| Square input corners, pill buttons and tags | Rounded-corner cards |

---

## 18. Where things live

| What | File |
|------|------|
| Colour, type and spacing tokens, home components | `css/styles.css` |
| Inner page components (cards, tickets, blog, articles, booking) | `css/pages.css` |
| Shared layout, nav, footer, stickers, charts and covers for inner pages | `tools/red_parts.py` |
| Inner page content | `tools/build_pages.py`, `tools/service_seo.py` |
| Home page content | `js/content.js` and `index.html` |
| Shared behaviour (cursor, stickers, reveal, forms) | `js/core.js` (inner pages), `js/main.js` (home) |
| Logo and star SVG symbols | `tools/symbols.txt`; logo files in `assets/` |
| Textures | `assets/img/paper.png`, `assets/img/grain.png` |
