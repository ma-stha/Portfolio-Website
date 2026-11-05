# Studio — editorial red design option

A complete design for the site in an editorial Swiss style, built to read like a senior independent practice rather than a template.

- **System:** strict 12-column grid, hairline rules, near-black on warm white (`#F6F5F1`), logo red `#F83232` used rarely: the full stop in the headline, the main button, the contact and call-to-action bands, the footer name.
- **Type:** Host Grotesk for everything functional; Newsreader serif for the manifesto, quotes and article body, so articles read like a magazine.
- **Deliberately absent:** rounded cards, gradients, drop shadows, icon grids, pill chips, glows.
- **Signature pieces:** work shown as an index table with a poster that follows the cursor and rows that open into the full case study; giant name set to the exact page width; side notes beside article paragraphs; a live Melbourne clock; press **G** (or the footer button) to show the layout grid.
- **Same content** as the main site: home content from `js/content.js`, inner pages from `tools/build_pages.py`.

## Build

```bash
python3 tools/build_studio.py
```

Regenerates everything in `studio/` except `css/studio.css`, `js/core.js` and `js/home.js`, which are hand-written.

## Status

A design option, not the live site. Pages are `noindex`, canonical to the main pages, and `/studio/` is disallowed in `robots.txt`. To make it the main site, move its files to the root and remove the `noindex` tags.
