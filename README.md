# Manjil Shrestha — Portfolio

Personal site for a data-driven digital marketer in Melbourne. Target keyword: **Digital Marketing Expert in Melbourne**.

Zero build step. Plain HTML, CSS and JavaScript, so it runs on any host (cPanel, Netlify, Vercel, GitHub Pages).

## Run locally

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000.

## Where to edit things

| What | File |
|------|------|
| Email, socials, receipt figures, tapes, manifesto, numbers, services, calculator defaults, case studies, process, tools, experience, education, certifications, testimonials, articles, FAQ | `js/content.js` |
| Hero headline, About text, Contact copy, meta tags, structured data | `index.html` |
| Colours, fonts, spacing | `css/styles.css` (tokens at the top) |
| Photos | `assets/img/` (see the README there) |
| Logo | `assets/logo.svg`, `assets/logo-light.svg`, `assets/mark.svg`, `assets/favicon.svg` |

### Placeholders to replace before launch

- `js/content.js`: email, social links, receipt numbers, headline numbers, case studies, experience, testimonials, certifications, article links.
- `index.html`: the Formspree form id (`YOUR_FORM_ID`). Until it is set, the form opens the visitor's email app.
- `assets/Manjil-Shrestha-CV.pdf`: add your CV or remove the "Download CV" link.
- `assets/img/portrait.jpg` and optional case study covers.

## Design: "Signal on Paper"

- **Palette**: paper `#E9E7E1`, ink `#0B0B0B`, logo red `#F83232`. Nothing else.
- **Texture**: a seamless paper tile (`assets/img/paper.png`) plus an animated grain layer (`assets/img/grain.png`) over every section.
- **Type**: Anybody (variable display face; the hero letters thin out and widen around the cursor), Archivo (body), Space Mono (data labels), Silkscreen (pixel accents that echo the blocky logo).
- **Logo**: redrawn as an exact vector from the supplied artwork, inlined as an SVG symbol so it recolours per section.
- **Signature moments**: campaign-receipt card with live counters, draggable stickers, clickable starburst that pops into particles, crossing marquee tapes, scroll-filled manifesto, a live growth calculator, pinned horizontal case studies, a scroll-driven process ring, and a starburst cursor.
- **Motion**: GSAP + ScrollTrigger and Lenis, vendored in `js/vendor/`. Everything respects `prefers-reduced-motion`.
- **SEO**: keyword-led H1, meta/OG/Twitter tags, canonical, `Person`, `ProfessionalService`, `WebSite` and `FAQPage` JSON-LD, sitemap and robots.

## Deploy

- **GitHub Pages**: enable Settings → Pages → Source "GitHub Actions". The workflow in `.github/workflows/deploy-pages.yml` publishes on every push to `main`.
- **Any other host**: upload the repository contents as-is to the web root.

Update the canonical URL in `index.html`, `sitemap.xml` and `robots.txt` if the site moves off `manjilshrestha.online`.
