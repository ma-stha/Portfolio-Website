# Trajectory — purple design option

A third, complete design for the site: **"Growth, plotted."** The whole site reads like a live chart.

- **Palette:** lavender graph-paper background `#F5F3FC`, aubergine ink `#170B38`, electric violet `#6A2CFF`, lilac `#C4B3FF`, and one lime signal `#D7FF3E` for the data point that matters. Deep night sections `#12092B`.
- **Type:** Bricolage Grotesque (variable display), Instrument Serif italic for the one accent word in each headline, Inter (body), IBM Plex Mono (data labels).
- **Signature pieces:** interactive hero chart (hover for values, switch Leads / ROAS / Revenue), bento service grid where each tile is a mini live chart, a scrollytelling case-study section where the chart morphs per case, a growth lab with a 12-month projection, an experience timeline drawn as a Gantt chart, a section-progress "spine" on wide screens, and smooth cross-page view transitions in Chrome, Edge and Safari.
- **Same content** as the main red site. Home content comes from `js/content.js`; inner-page content comes from `tools/build_pages.py`. Edit content there once and both designs pick it up after a rebuild.

## Build

```bash
python3 tools/build_trajectory.py
```

It regenerates everything in `trajectory/` except `css/`, `js/core.js` and `js/home.js`, which are hand-written.

## Status

This is a **design option**, not the live site. Every page has `noindex` and a canonical link pointing to the matching red page, so it cannot compete with the main site in Google. To make it the main site, move its files to the root and remove the `noindex` tags.
