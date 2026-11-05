# Manjil Shrestha — Portfolio

Personal site for a data-driven digital marketer in Melbourne. Target keyword: **Digital Marketing Expert in Melbourne**.

Zero build step for visitors. Plain HTML, CSS and JavaScript, so it runs on any host (cPanel, Netlify, Vercel, GitHub Pages).

## Run locally

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000.

## Design: "Signal on Paper"

**Read [`DESIGN-GUIDE.md`](DESIGN-GUIDE.md) before building or editing any page.** It holds the rules, tokens, components and checklists that keep the whole site consistent.

- **Palette**: paper `#E9E7E1`, ink `#0B0B0B`, logo red `#F83232`. Nothing else.
- **Texture**: a seamless paper tile (`assets/img/paper.png`) plus an animated grain layer (`assets/img/grain.png`).
- **Type**: Anybody (variable display face), Archivo (body), Space Mono (data labels), Silkscreen (pixel accents), Caveat (handwritten sticky notes in articles).
- **Language**: hard black borders and offset shadows, red highlighter bars, tape strips, stamps, receipts with torn edges, draggable stickers and a starburst cursor.
- **Logo**: MANJIL wordmark redrawn as an exact vector, inlined as an SVG symbol. The `mastha` logo files from the purple version are kept in `assets/brand/`.

## Pages

| URL | What's on it |
|-----|--------------|
| `/` | Home: hero with campaign receipt, tapes, manifesto, about, numbers, services, growth calculator, case studies, process ring, stack, experience, testimonials, insights, FAQ, contact |
| `/services/` | Six detailed services with a sticky index, three pricing tickets, process, industries, FAQ |
| `/services/seo/` | SEO service page: search-results mockup that climbs to #1, pain points, what's included, 6-month roadmap, SEO health-check receipt, mini case study, pricing, FAQ, related services. Template for other service pages |
| `/book/` | Free consultation booking: calendar, Melbourne-time slots shown in the visitor's time zone, details form, confirmation with Google Calendar and .ics links |
| `/contact/` | Live Melbourne clock and status, contact methods, enquiry form, office hours, FAQ |
| `/blog/` | Featured post, topic filters, search, post cards, topics, newsletter |
| `/blog/<slug>/` | Article: sticky table of contents with reading progress, TL;DR, callouts, stat cards, charts, tables, code, checklist, sticky notes, author box, newsletter, previous/next, related posts |
| `/blog/_template/` | Copy-ready article template showing every component (noindex) |
| `/blog/feed.xml` | RSS feed |

## Where to edit things

| What | File |
|------|------|
| Home page content (email, socials, numbers, services, case studies, testimonials, insights, FAQ…) | `js/content.js` |
| Home hero and section copy | `index.html` |
| Inner page copy, prices, FAQs, articles | `tools/build_pages.py` and `tools/service_seo.py`, then rebuild |
| Inner page design (layout, nav, footer, charts, stickers) | `tools/red_parts.py`, `css/pages.css` |
| Booking hours and how far ahead people can book | top of `js/book.js` (`SLOTS`, `DAYS_AHEAD`) |
| Colours and fonts | tokens at the top of `css/styles.css` |

Scripts: the home page uses `main.js`. Inner pages use `core.js` (nav, cursor, stickers, forms) plus `pages.js`, `book.js` or `blog.js`.

## Rebuilding the inner pages

```bash
python3 tools/build_pages.py
```

This rewrites every page under `services/`, `book/`, `contact/` and `blog/`, plus `sitemap.xml` and `blog/feed.xml`. Edit the files in `tools/`, not the generated HTML.

### Adding another service page

1. Copy `tools/service_seo.py` to e.g. `tools/service_paid.py`, rename the function and change `path`, copy, pricing and FAQs.
2. In `tools/build_pages.py`, `exec` the new file next to the SEO one (before `red_parts.py`), call the function, and add the URL to `sitemap()`.
3. Optional: give it a hero sticker in `STICKERS` in `tools/red_parts.py`.
4. Rebuild.

### Writing a blog post

Either add a new entry to `POSTS` in `tools/build_pages.py` and rebuild (the card, sitemap and RSS update automatically), or copy `blog/_template/` by hand and follow the notes inside it.

## Before launch

- Replace everything marked **DEMO** in `js/content.js`, plus demo prices, testimonials and case-study numbers in `tools/`.
- Replace `YOUR_FORM_ID` with a Formspree form id in every form (`index.html` and `tools/`). Until then forms open the visitor's email app.
- Add `assets/Manjil-Shrestha-CV.pdf` or remove the "Download CV" links.
- Optional: set `calendlyUrl` in `js/content.js` to swap the booking widget for a Calendly embed.

## Design options

| Version | Where | Status |
|---------|-------|--------|
| Red "Signal on Paper" | repo root | **Main site** |
| Purple "Trajectory" | `/trajectory/` | Full alternative design, same content, noindex. See `trajectory/README.md` |
| Purple "Ultraviolet" | git commit `cf6a8f6` | Archived |

## The purple "Ultraviolet" version

The dark purple version with the UV torch is saved in git history at commit `cf6a8f6`. To look at it:

```bash
git checkout cf6a8f6
```

## Deploy

- **GitHub Pages**: enable Settings → Pages → Source "GitHub Actions". `.github/workflows/deploy-pages.yml` publishes on every push to `main`.
- **Any other host**: upload the repository contents as-is.

Update the canonical URL in `index.html`, `tools/build_pages.py` (`SITE`) and `robots.txt` if the domain changes.
