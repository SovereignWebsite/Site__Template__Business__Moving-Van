# Now (27 Nov 2026)

## Done
- Repository renamed by factory.b to Site__Template__Business__Moving-Van (Dinis's word, 25 Nov). Template, fully generic, no business name.
- New address live: https://moving-van.business.template.sovereignweb.site/ (the old one shows a "Moved to" page). CNAME, canonical and share tags now name it.
- My public key at site/keys/b.site.moving-van.json, in its own signed commit (74955c6); Signers passed.
- This area (8631c65).
- All five designs from design.b's brief, built by tools/designs/build.py from site/data/content/en.json:
  1. The van (/), 2. Moving day (/moving-day/), 3. The boxes (/boxes/), 4. The inventory (/inventory/), 5. The card (/card/), and all five side by side at /designs/.
- A "Choose a design" button in a one-line top bar opens every design as a real screenshot, the current one outlined (screenshots by tools/designs/shots.mjs).
- Demo band on every design page, every detail a [placeholder], the quote form sends nothing. No script anywhere: the inventory's tally is CSS counters.
- tools/check.sh passes; axe clean on every page at 390 px and 1280 px, light and dark; no sideways scroll at 360 px; every page under 4,000 px on a phone.

## Next
1. Ask design.b.rounds for a review round.
2. Admin area like Kate's, and a guided tour with a PDF (learnings-from-lee-elle.md, items 8 to 11).
3. Register with hub.b; an own share card in place of the seed's.
