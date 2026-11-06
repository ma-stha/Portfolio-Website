# LOUD — bold red and black design option

A complete design for the site built to feel loud, confident and impossible to mistake for a template.

**Building or editing a page? Read [`DESIGN-BLUEPRINT.md`](DESIGN-BLUEPRINT.md) first.** It holds the rules, tokens, page architecture, component library and the recipe for new pages. The live page template is [`_template/`](_template/index.html).

- **Idea:** the numbers are the heroes, and so is the name. The hero spells MANJIL as a rising bar chart. Bars near the cursor grow, a live trend line runs across their tops, and a tag shows the "growth". On phones a slow wave runs through the bars instead.
- **System:** full-bleed blocks of logo red `#F83232`, ink `#0A0A0A` and paper `#F2EFE9`. Inside red blocks the accent flips to black, so text on red is always black. 2px rules, no shadows, no gradients, no rounded cards.
- **Type:** Big Shoulders Display (900, uppercase) for headlines and numbers; Instrument Sans for reading; Martian Mono for labels; Newsreader for article body.
- **Signature pieces:**
  - Kinetic manifesto: "Most marketing is GUESSWORK", struck through in red as you scroll, then "Mine is MEASURED."
  - "Receipts": case studies on a horizontal track with giant result numbers.
  - Services as giant outlined words that drift and fill red on hover.
  - Kathmandu to Melbourne route map with a red duotone portrait.
  - Method steps as cards that stack as you scroll.
  - A custom cursor that grows into a label ("Explore", "Let's go") over links. The header changes colour to match the block under it.
  - A giant MASTHA with a spinning star in the footer.
- **Same content** as the main site: home content from `js/content.js`, inner pages from `tools/build_pages.py`.

## Build

```bash
python3 tools/build_loud.py
```

Regenerates every HTML page in `loud/`. It reuses the inner-page structure from `tools/build_studio.py` and swaps the chrome, heroes and home page. `css/loud.css`, `js/core.js` and `js/home.js` are hand-written. The look lives in Part 2 of `css/loud.css`.

## Status

A design option, not the live site. Pages are `noindex`, canonical to the main pages, and `/loud/` is disallowed in `robots.txt`. To make it the main site, move its files to the root and remove the `noindex` tags.
