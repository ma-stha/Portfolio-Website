# Living Mark — creative branding design option

A complete design that positions Manjil Shrestha as a **branding expert in Australia**, built like a brand book for himself: a logo that changes shape, its own icon alphabet, pattern system, texture and voice.

**Building or editing a page? Read [`DESIGN-BLUEPRINT.md`](DESIGN-BLUEPRINT.md) first.** The live page template is [`_template/`](_template/index.html).

- **Living mark:** the red hero shape moves between seven identities (Circle, Signature, Bloom, Squircle, Spark, Sun, Blob). Click it to change it.
- **Brand builder:** visitors type a business name, pick a personality and an icon, and get a live identity: logo, tagline, palette and mockups (business card, tote, app icon, social post).
- **Icon alphabet:** 12 custom geometric icons used as section markers, bullets, the cursor, patterns, service icons and even words in the rebus manifesto.
- **Print feel:** risograph grain, halftone dots, a halftone portrait that reacts to the cursor, rounded sticker cards with slight tilts.
- **Work:** four demo client brands (Melbourne, Yarra Valley, Brisbane, Sydney) with generated identity artwork.
- **Type:** Bricolage Grotesque, Fraunces italic for one emotional word per headline, DM Mono labels.
- **Colour:** red `#F83232` leads, with ink `#161211`, paper `#F4EEE6` and blush `#F9D8D1`.

## Pages

Home, Work, Services, Brand identity service, Book, Contact, Journal with three branding articles and an article template, a page template, and a style guide (`styleguide/`).

## Design files

`design-elements/` holds the brand as files: the 12 icons (red, ink, paper), the MANJIL logo in five versions, favicon and app icon, the seven living-mark shapes, colour tokens (CSS and JSON) and palette, patterns, halftone and grain textures, and the demo artwork. They are regenerated on every build.

## Build

```bash
python3 tools/build_brand.py
```

The generator is standalone: Python 3, no packages. All copy and settings for this design (domain, email, socials, services, packages, case studies, articles, FAQs) live in `tools/build_brand.py`. `css/brand.css`, `js/core.js`, `js/home.js` and `js/inner.js` are hand-written.

## Status

A design option, not the live site. Pages are `noindex`, canonical to the main pages, and `/brand/` is disallowed in `robots.txt`. Demo clients, prices and quotes are marked as demo and must be replaced before launch.
