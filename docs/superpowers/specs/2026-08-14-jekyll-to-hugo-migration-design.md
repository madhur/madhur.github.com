# Jekyll → Hugo Migration — Design

**Date**: 2026-08-14
**Status**: Approved by user, pending implementation plan

## Goal

Migrate madhur.co.in from Jekyll (GitHub Pages, gulp/Less/Bootstrap 3 build) to Hugo, with a
dark, responsive theme, while preserving all content (278 posts, projects, static pages) and
either porting or consciously dropping the site's accumulated Jekyll-specific customizations.

## Current state summary

- Jekyll site, source in repo root, `_config.yml` builds to a sibling `../site/` directory.
- Visual design: already dark (`#222`/`#ddd`), textured/"grungy" 2012-era aesthetic. Responsive
  behavior comes entirely from Bootstrap 3.3.5 grid classes — no custom breakpoints.
- Build pipeline: Gulp + Less, uglify/cssmin, `gulp-git` tasks that commit/push the built
  `_site` directly from the developer's machine.
- 5 custom Jekyll plugins (`_plugins/*.rb`): tag generation, tag cloud, GitHub API embeds
  (dead), slug/date filters, string monkeypatch.
- 278 posts (2011–2028, some intentionally future-dated), plus a projects section driven by
  `_data/projects/*.yml`, plus assorted static single-page sections (code, papers, work, info,
  donate, contact, privacy), a defunct Silverlight demo, and a standalone Chrome-extension
  privacy page (`leetcode-format.html`) unrelated to the Jekyll build.
- Comments via Disqus (277 posts carry `disqus_id`). Search via a dead Google Custom Search
  widget (`/results/`) and a dead AngularJS live-filter on `/404.md`.

Full inventory and per-item Hugo-portability assessment is in the exploration notes below
(§ Appendix); this section captures only what's needed to act.

## Decisions

1. **Theme**: [Hugo PaperMod](https://github.com/adityatelange/hugo-PaperMod), customized with
   the site's own branding/colors. Chosen over a from-scratch theme because PaperMod already
   provides, natively, nearly everything the current site does with custom code: dark mode,
   full responsiveness, taxonomy (tag) pages, a client-side Fuse.js search page, giscus comment
   integration, and built-in reading time — each of these replaces a piece of custom Jekyll
   plugin code (see Decisions 4–5 below).
2. **Content scope**: everything migrates — posts, projects, all static sections, and the
   leetcodeformat tool assets/pages. `silverdemo/` (Silverlight) is carried over as **archived,
   inert static files only** — the Silverlight runtime is dead in every modern browser, so no
   hosting choice can make it functional again; it is not a working demo post-migration, on
   Jekyll or Hugo.
3. **Comments**: switch from Disqus to **giscus** (GitHub Discussions-backed), using PaperMod's
   native giscus support. Existing Disqus comment threads are not migrated/imported — this is a
   clean break, accepted by the user. `disqus_id` front matter becomes a harmless unused param.
4. **Search**: PaperMod's built-in Fuse.js client-side search page replaces **both** dead search
   implementations (`/results/` Google CSE, `/404.md` AngularJS filter) with one working,
   modern, dependency-light search.
5. **Tag cloud**: rebuilt as a small custom Hugo shortcode/partial (compute min/max post counts
   over `.Site.Taxonomies.tags`, scale font-size inline or via a CSS custom property) — this is
   the one piece of genuine custom logic worth porting rather than replacing with a plain list,
   per user preference to keep the feature.
6. **Hosting/deploy**: GitHub Pages, via a GitHub Actions workflow (Hugo's official build +
   `actions/deploy-pages`) triggered on push to `master`. Replaces the old `gulp-git`
   commit-and-push-the-built-site pattern with proper CI. Existing `CNAME` file carries over
   unchanged.

## What gets dropped (not ported)

These are already dead/broken in the current Jekyll site, or are third-party services not worth
re-integrating:

- `_plugins/octokit.rb` — 4 Liquid tags doing build-time GitHub API embeds. Hardcoded
  Windows-only credential path, deprecated GitHub basic auth, gated behind
  `generate_projects: false` (already disabled). Confirmed no live template calls it in the
  active config.
- Google Custom Search widget on `/results/` — deprecated `google.co.in/jsapi` loader.
- AngularJS live-search on `/404.md` — unmaintained Angular 1.x, replaced by Fuse.js search
  (Decision 4).
- `ghbtns.com` GitHub badge iframes on project pages — legacy/likely-defunct service.
- Feedburner RSS link — legacy Google service; replaced by Hugo's native Atom/RSS feed
  generation.
- `ph_postings_meta.json` — a Liquid-generated JSON dump of all posts with no in-repo consumer
  found. User confirmed: probably dead, drop it rather than build a Hugo custom-output-format
  replacement.
- `serviceWorker.js` — already fully commented out / dead code (`default.html` actively
  unregisters any existing service worker). Nothing to port.
- `_scripts/import_comments.rb`, `_scripts/transfer_urls.rb` — one-off historical Disqus
  migration tools tied to an unrelated old site (`mark.reid.dev/iem`), not part of the current
  build. Left behind.

## What needs custom rework (not a drop-in Hugo feature)

- **Tag cloud** (Decision 5) — no Hugo built-in equivalent; requires a purpose-written
  shortcode/partial.
- **`.htaccess` redirects** (old `/iem/...` 301s, custom 404 doc) — GitHub Pages already ignores
  `.htaccess` entirely, so these are arguably non-functional today regardless. In Hugo, any
  redirects worth preserving become per-page `aliases:` front matter, which is capped by what
  GitHub Pages' static-only hosting supports (no true server-side rewrite rules). If real
  redirect rules turn out to matter, that's a reason to reconsider Netlify/Cloudflare Pages
  later — out of scope for this migration but worth flagging.
- **Print-friendly view** (`Clickheretoprint()` custom `window.print()` + `print.css`) — the
  behavior is portable but needs a vanilla-JS reimplementation, not a copy-paste, since it's
  currently hand-rolled jQuery-era JS.

## Content migration mapping

| Source | Destination | Notes |
|---|---|---|
| `_posts/*.md` (278 files) | Hugo `content/posts/` | Front matter maps directly: `title`, `tags`, `excerpt`→`description`. `disqus_id` kept as unused param (harmless) or stripped. `location`/`time` front-matter defaults (currently from `_config.yml` `defaults:`) become a Hugo archetype default or front-matter cascade. |
| `_data/projects/*.yml`, `_data/oldprojects/*.y*ml` | Hugo `data/projects/` | Copy near-as-is; normalize inconsistent YAML (e.g. tab-indented `publish:\tno` in `oldprojects/DOS.yaml`). |
| `projects/*.md` | Hugo `content/projects/` | Rebuilt as a Hugo content type + list/single templates reading `.Site.Data.projects`. Drop the dead octokit embed calls and `ghbtns.com` iframes. |
| `code/`, `papers/`, `work/`, `info/`, `donate/`, `contact/`, `privacy/` | Hugo `content/<section>/` | Static content pages, direct port. |
| `leetcodeformat/data.json`, `leetcode-format.html` | Hugo `static/` | Unrelated to Jekyll processing today (consumed by an external Chrome extension); copy as static assets. |
| `silverdemo/` | Hugo `static/silverdemo/` | Archived only, not functional (see Decision 2). |
| `blog/index.markdown`, `blog/archives/index.markdown` | Hugo `content/posts/_index.html` + list template | Replaced by Hugo's native `.GroupByDate` (year-grouped archive) — no custom generator plugin needed. |
| Tag pages (`_plugins/site_process.rb` generator, `tag.html`/`tags.html`/`alltags.html`) | Hugo taxonomies | Hugo's built-in tag taxonomy replaces the custom Ruby `Generator` entirely. |
| `_includes/post-listing.html` (group-by-year) | Hugo `.GroupByDate` | Direct built-in replacement. |
| `_includes/social-flat.html` (reading-time calc) | Hugo `.ReadingTime` | Direct built-in replacement. |
| `_plugins/filters.rb` (`slugize`, `format_date`, `length`) | Hugo built-ins (`urlize`, `dateFormat`, `len`) | No custom code needed; verify slug format matches closely enough that old URLs don't break (see `core_ext.rb` note below). |
| `_plugins/core_ext.rb` (`String#slugize` monkeypatch) | Hugo `urlize`/`anchorize` | Verify exact output format matches (custom version replaces whitespace/dots with `-` and strips non-word chars) since tag-page URLs depend on it. |
| `index.md` (latest 5 posts + reading time) | Hugo homepage template | `.Site.RegularPages` + `.ReadingTime`, straightforward rewrite. |
| `404.md` | Hugo 404 template | Search box replaced per Decision 4; static contact-icon links carry over as-is. |
| `robots.txt`, `atom.xml`, `CNAME` | Hugo `static/`, native feed config, unchanged | `atom.xml` replaced by Hugo's generated feed; `robots.txt`/`CNAME` copy as-is. |

## Build & deploy

- Hugo replaces the Gulp/Less/Bootstrap pipeline outright — PaperMod ships its own CSS, no
  Less compilation or Bootstrap dependency needed.
- `Gulpfile.js`, `package.json` (gulp deps), `.jekyll-cache/`, `Gemfile`/`Gemfile.lock`,
  `_plugins/`, `_layouts/`, `_includes/`, `_scripts/` are retired once the Hugo templates cover
  their functionality (per mapping table above).
- New: a GitHub Actions workflow using Hugo's official build action +
  `actions/deploy-pages`, triggered on push to `master`, replacing `_config.yml`'s
  `destination: ../site/` + manual `gulp-git` commit/push pattern.
- `mode: prod`-gated Google Analytics include becomes Hugo's `hugo.IsProduction` /
  `--environment` check.

## Out of scope for this migration

- Real server-side redirect rules beyond what GitHub Pages + Hugo `aliases:` can express
  (flagged above as a possible future reason to move hosts).
- Recovering/importing historical Disqus comment threads into giscus (clean break, per Decision
  3).
- Making `silverdemo/` functional again (impossible on any modern browser/host).

## Appendix: source exploration notes

Full per-directory findings (layouts, includes, plugins, data, frontend assets, build tooling,
third-party JS, content structure) were gathered via targeted codebase exploration on
2026-08-14 and are summarized into the decisions and tables above. Key source paths referenced
during exploration, for anyone re-verifying details while writing the implementation plan:

- `_layouts/*.html`, `_includes/*.html`, `_plugins/*.rb`, `_data/{projects,oldprojects}/*.y*ml`
- `files/css/{styles,searchresults}.less`, `files/js/main.js`, `files/js/vendor/*`
- `Gulpfile.js`, `package.json`, `serviceWorker.js`, `_config.yml`, `.htaccess`, `robots.txt`,
  `atom.xml`, `404.md`, `index.md`
- `_posts/` (278 files), `projects/*.md`, `code/`, `results/`, `papers/`, `work/`, `info/`,
  `donate/`, `contact/`, `privacy/`, `leetcodeformat/`, `leetcode-format.html`, `silverdemo/`,
  `ph_postings_meta.json`, `_scripts/*.rb`
