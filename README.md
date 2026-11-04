# mastha — Manjil Shrestha Portfolio

Personal site for a data-driven digital marketer in Melbourne. Target keyword: **Digital Marketing Expert in Melbourne**.

Zero build step. Plain HTML, CSS and JavaScript, so it runs on any host (cPanel, Netlify, Vercel, GitHub Pages).

## Run locally

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000.

## Concept: "Ultraviolet"

Near-black textured paper, one violet light. The cursor is a UV torch: it lights the paper and reveals ink that is otherwise invisible.

- **Hidden notes**: seven handwritten notes across the page only appear under the torch. A counter in the bottom-left tracks how many a visitor has found, with a reward when they find all seven.
- **Hero photo**: shown as a violet duotone. Under the torch it reveals the full-colour photo.
- **Case files**: results are redacted. Resting the torch on the numbers declassifies the file with a stamp. On phones, files declassify as they scroll into view.
- **Touch devices**: the torch wanders through the hero by itself, and follows the visitor's finger anywhere on the page.
- **Accessibility**: a "Reveal all" button shows every hidden element. Reduced-motion users get everything revealed by default.

Other sections: client marquee, about with stats, services accordion, growth lab calculator, typing terminal process, toolkit, experience timeline with education and certifications, testimonial slider, insights, FAQ (published as FAQ schema), contact card and form, and a footer logo that lights up under the torch.

## Where to edit things

| What | File |
|------|------|
| All repeated content: email, socials, clients, stats, services, case files, process, calculator defaults, toolkit, experience, education, certifications, testimonials, insights, FAQ | `js/content.js` |
| Hero headline, About text, hidden notes, meta tags, structured data | `index.html` |
| Colours, fonts, torch size | `css/styles.css` (tokens at the top) |
| Photos | `assets/img/` (see the README there) |

Everything marked **DEMO** in `js/content.js` is placeholder data.

### Before launch

- Replace DEMO data in `js/content.js`.
- Set the Formspree form id (`YOUR_FORM_ID`) in `index.html`. Until then the form opens the visitor's email app.
- Add `assets/Manjil-Shrestha-CV.pdf` or remove the two "Download CV" links.
- Set `bookingUrl` in `js/content.js` to a Calendly or similar link.

## Brand

- **Logo**: `assets/mastha-logo.svg` (light), `mastha-logo-dark.svg`, `mastha-logo-violet.svg`. Traced as an exact vector from the supplied artwork and inlined as an SVG symbol.
- **Favicon / app icons**: generated from the violet-ring avatar (`assets/favicon-32.png`, `icon-192.png`, `icon-512.png`, `apple-touch-icon.png`).
- **Palette**: paper `#141317`, ink `#ECE8F4`, violet `#7844E9` (sampled from the avatar ring), UV glow `#B596FF`.
- **Type**: Geist (UI and headlines), Geist Mono (data), Pirata One (blackletter accents that match the logo), Caveat (the hidden handwriting).
- The earlier MANJIL logo files are kept in `assets/brand/`.

## Deploy

- **GitHub Pages**: enable Settings → Pages → Source "GitHub Actions". `.github/workflows/deploy-pages.yml` publishes on every push to `main`.
- **Any other host**: upload the repository contents as-is.

Update the canonical URL in `index.html`, `sitemap.xml` and `robots.txt` if the domain changes.
