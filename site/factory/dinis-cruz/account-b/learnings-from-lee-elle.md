# What Dinis asked for on this site, for every site we build

Dinis Cruz's comments in b.site.lee-elle-horowitz's session on 25 November 2026, while reviewing Lee-Elle Horowitz's site, and what each means for any site keeper. He asked: "can you please relay all these comments and changes that I'm making, so that all sites that we build take this into account". Quotes are his words; the rest is the keeper's reading of them.

## Content
1. **Every word in JSON, nothing in the HTML.** "the key is to make sure that all content from the site is on json files and nothing is hardcoded into html". Keep content in `site/data/content/*.json` (one file per language, plus site settings, start page, tour and admin) and build the pages from it. The generator holds no words. Here: `tools/designs/build.py`.
2. **Every design in every language the owner works in.** "the home page should be in english, but can you allow all 5 designs to be translated?" For a Hebrew tutor: each design in English and in Hebrew (right to left, `lang`/`dir` on the html element, logical CSS). Mark a translation the owner has not checked, on every page, until she checks it.
3. **The language switch is super visible.** "please make that switch between English and Hebrew super visible". Both languages always shown in the top bar, the current one filled; a floating button that appears once you scroll (so it never covers a first-screen button).
4. **Stand-in photos are fine to show what is possible**, credited honestly. "this is just to give LEH a view of what can be done, she will then upload more photos". Credit each one as its source shows it; never invent a photographer.

## Design
5. **Make it wow, especially for artists.** "really make this site have the WOW factor", "since these are artists". Each design opens differently on a phone, with the owner's photo on the first screen (design.b's wow brief, guideline 2a).
6. **The design chooser: one button, real screenshots.** "this is wrong ... it should be like" Emily Cruz's and Grace Farrell's sites. One "Choose a design" button next to the language switch opens every design as a real screenshot (number, name, one line), the current one outlined, and "All five, side by side". Now design.b's guideline 2a.
7. **The top bar is one line.** "make it so that in the option to change the design I see all of them in one go", "which will also gain you one line from that top nav bar".

## Pages every site gets
8. **An admin area like Kate's.** "add that admin section (like we did for kate)". Status, tasks (one Markdown file per task in `issues/`), designs, content files, photos and credits, quality checks, every change, agents, how it was made. Built from the repository.
9. **Presentations on the site, with a PDF to download.** "some really nice presentations (code on the site with option to download the PDF) that explains what we have here and provides a nice guided tour of the main features". Slides are HTML on the site, built from JSON, with screenshots of the live site; each has a PDF made from the same page.
10. **Slides need clear navigation.** "can you add a better navigation (left and right arrows)". Previous and next arrows under every slide, and the arrow keys.
11. **Name downloads for the person who will share them.** "can you name the files better", "so that I can share them". For example `Lee-Elle-Horowitz-website-guided-tour.pdf`, not `your-site.pdf`. Keep PDFs up to date with every change to the pages.

## Process
12. **Relay what the owner's reviewer teaches**, so every keeper learns it once: "can you tell this to the design agent so that other sites.* agents don't make these mistakes".
13. **Check at phone width as well as desktop.** Not Dinis's words: design.b.rounds found a serious accessibility fault only at 390 px, which `tools/check.sh` (desktop width) missed. Run axe at 390 px in light and dark before every push (`tools/checks/axe-phone.mjs` here).

The site: https://lee-elle-horowitz.artist.sovereignweb.site · source: https://github.com/SovereignWebsite/Site__Artist__Lee-Elle-Horowitz
