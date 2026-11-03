# Manjil Shrestha — Portfolio

Personal site for a data-driven digital marketer in Melbourne. Target keyword: **Digital Marketing Expert in Melbourne**.

Zero build step. Plain HTML, CSS and JavaScript, so it runs on any host (cPanel, Netlify, Vercel, GitHub Pages).

## Run locally

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000.

## Where to edit things

| What                                   | File                 |
|----------------------------------------|----------------------|
| Name, email, socials, numbers, services, case studies, process, tools, experience, education, certifications, testimonials, articles, FAQ | `js/content.js` |
| Hero headline, About text, Contact copy, meta tags, structured data | `index.html` |
| Colours, fonts, spacing                | `css/styles.css` (tokens at the top) |
| Photos                                 | `assets/img/` (see the README there) |
| Logo / favicon                         | `assets/logo.svg`, `assets/favicon.svg`, `assets/logo-wordmark.svg` |

### Placeholders to replace before launch

- `js/content.js`: email, social links, the four headline numbers, case study clients and results, experience entries, testimonials, certifications, article links.
- `index.html`: the Formspree form id (`YOUR_FORM_ID`) in the contact form. Until it is set, the form opens the visitor's email app instead.
- `assets/Manjil-Shrestha-CV.pdf`: add your CV or remove the "Download CV" link in `index.html`.
- `assets/img/portrait.jpg` and the case study covers.

## Design

- **Palette**: ink `#08090C`, paper `#F4F1EA`, amber `#FFB020` → `#FF7A1A`, ice `#7FD6FF` for negative/secondary data.
- **Type**: Instrument Serif (italic display), Space Grotesk (UI), JetBrains Mono (data labels).
- **Motion**: GSAP + ScrollTrigger (pinned horizontal case studies, process scrub), Lenis smooth scroll, canvas signal field in the hero, count-up metrics, magnetic buttons, custom cursor. All of it respects `prefers-reduced-motion`.
- **SEO**: keyword-led H1, meta/OG/Twitter tags, canonical, `Person` + `ProfessionalService` + `WebSite` + `FAQPage` JSON-LD, sitemap and robots.

Libraries are vendored in `js/vendor/` (GSAP 3.12.5, Lenis 1.1.18), so there are no CDN dependencies.

## Deploy

- **GitHub Pages**: enable Settings → Pages → Source "GitHub Actions". The workflow in `.github/workflows/deploy-pages.yml` publishes on every push to `main`.
- **Any other host**: upload the repository contents as-is to the web root.

Update the canonical URL in `index.html`, `sitemap.xml` and `robots.txt` if the site moves off `manjilshrestha.online`.
