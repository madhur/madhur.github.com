---
slug: "migrating-from-jekyll-to-hugo"
title: This Blog Just Moved From Jekyll to Hugo
date: '2026-08-15'
description: After 15 years on Jekyll, this site now runs on Hugo with the PaperMod theme — here's what changed, what I kept, and what I dropped.
tags:
  - Hugo
  - Jekyll
  - PaperMod
  - Static Site Generator
draft: false
---

> **Disclaimer**: This blog post was written with the assistance of AI, working through the actual migration alongside me. The decisions, trade-offs, and the site you're reading this on are the result of real work, not a generated demo.

If you're reading this and everything mostly looks the same, that's on purpose. If you're reading this and a few things look different — the fonts, the tag cloud, the comments box — that's also on purpose. This site has run on [Jekyll](https://jekyllrb.com/) since June 2011. As of today, it runs on [Hugo](https://gohugo.io/), using the [PaperMod](https://github.com/adityatelange/hugo-PaperMod) theme.

## Why bother

Jekyll served this blog well for 15 years, but the toolchain around it had aged badly. The site was still built with Bootstrap 3, a Gulp/Less pipeline, jQuery-era JavaScript, and five custom Ruby plugins — one of which tried to hit the GitHub API with a hardcoded Windows credential path that hadn't worked in years. Ruby builds had gotten slower and fussier to keep working across machines, and every "just add one feature" request meant fighting fifteen-year-old glue code before writing anything new.

Hugo builds this entire site — 278 posts, projects, tag pages, search index — in under half a second. That alone would have been worth it.

## What actually moved

- **All 278 posts**, front matter and all, including the syntax-highlighted code blocks and cross-post links that used to be Jekyll's `{% post_url %}` tags.
- **Projects**, both the active list and a "legacy projects" page for the ones I'm not maintaining anymore.
- **The weighted tag cloud** — yes, the one where more-used tags render bigger. That was a custom Jekyll plugin; it's now a custom Hugo shortcode doing the same 75%–280% font-size math.
- **The URL scheme.** Posts still live at `/blog/YYYY/MM/DD/slug.html`, exactly like before. Fifteen years of links pointing at this site from elsewhere shouldn't start 404ing today.

## What changed

- **Theme**: PaperMod, dark by default, with the toggle removed entirely — this site is staying dark. I also pulled the original site's fonts, link colors, and that repeating dark linen background back in, so the bones of the old design are still here under a much faster engine.
- **Search**: client-side, via [Fuse.js](https://www.fusejs.io/), baked into the build. The old search box depended on a Google Custom Search widget that had quietly stopped working years ago.
- **Comments**: [giscus](https://giscus.app/), backed by GitHub Discussions, replacing Disqus. This is a clean break — old Disqus threads aren't imported — but it means no ads, no tracking, and comments that live in the same place as the code.
- **Deploys**: a GitHub Actions workflow builds and publishes the site on every push. No more building locally and pushing a `_site` directory by hand.

## What got dropped

A few things were dead weight and stayed dead: the GitHub API embeds mentioned above, the broken search widget, a Feedburner link nobody's used in a decade, and an old Silverlight demo that no browser on Earth can still run.

## If something looks broken

This was a big, mostly-automated migration — content scripted and verified across all 278 posts, then reviewed, several times over. If you spot a broken link, a missing image, or something that used to work and doesn't anymore, the comments below now go straight to a GitHub Discussion. Let me know.
