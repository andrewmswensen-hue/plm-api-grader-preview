# PM API Report Card — preview build

Staging copy of the API Report Card page, kept **out of peterlohmann.com** while
it is being drafted.

**Preview:** https://andrewmswensen-hue.github.io/plm-api-grader-preview/

## Why this repo exists

The page is not ready to be part of the live site, and "unlisted on the live
site" was not private enough. Here it is on a separate host entirely: nothing on
peterlohmann.com links to it, it carries `noindex, nofollow`, and `robots.txt`
disallows crawling.

## Where changes go

| Change | Goes to |
|---|---|
| The API Report Card page | **this repo** |
| Anything else on peterlohmann.com | `pslohmann/peterlohmann-website` |

## What is in here

| File | Notes |
|---|---|
| `index.html` | The page. Nav/footer link out to the live peterlohmann.com. |
| `styles.css` | **A COPY** of the live site's stylesheet. See the warning below. |
| `site.js` | A copy of the live site's script (mobile nav, scroll reveals). |
| `files/pm-api-report-card-methodology.md` | The grading file the download button serves. |
| `favicon.*` | Copies. |

## The one thing to watch

`styles.css` is a **copy**, not a link. If the live site's stylesheet changes,
this preview will drift and stop being an accurate preview. Re-copy it from
`peterlohmann-website/styles.css` before judging any fine visual detail.

## Going live

When the page is approved, it moves back into `peterlohmann-website` as
`pm-api-grader.html`:

1. Copy `index.html` back, and restore the root-absolute links
   (`https://www.peterlohmann.com/blog` → `/blog`, and the download back to
   `/files/…`).
2. Drop the `noindex, nofollow` meta tag.
3. Make sure `pm-api-grader.html` is NOT in `build-sitemap.py`'s EXCLUDE set,
   then re-run it.
4. Archive or delete this repo so there is never a second copy of the page on
   the internet.
