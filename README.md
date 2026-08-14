# madhur.co.in

Source for [madhur.co.in](https://madhur.co.in) — a blog I have been writing
since 2011. It was originally a Jekyll site; it now runs on
[Hugo](https://gohugo.io).

## Stack

* Static site generation with [Hugo](https://gohugo.io) (extended, pinned to
  0.164.0 in CI)
* Theme: [PaperMod](https://github.com/adityatelange/hugo-PaperMod), vendored as
  a git submodule under `themes/PaperMod`
* Comments via [giscus](https://giscus.app) (GitHub Discussions)
* Client-side search with [Fuse.js](https://fusejs.io), driven by a JSON index
  Hugo emits for the home page
* Syntax highlighting with Hugo's built-in Chroma
* Weighted tag cloud, a custom shortcode ported from the old Jekyll plugin
* Google Analytics, production builds only
* Hosted on GitHub Pages, deployed by GitHub Actions

## Layout

```
content/          posts (content/posts), projects, and standalone pages
data/projects     project metadata driving /projects/
data/oldprojects  legacy project metadata driving /projects/old/
layouts/          project-level template overrides on top of PaperMod
static/           images, CSS, CNAME and other files copied verbatim
themes/PaperMod/  theme submodule
```

Posts keep the original Jekyll permalink scheme,
`/blog/:year/:month/:day/:slug.html`, configured via `[permalinks]` plus
`uglyURLs` scoped to the `posts` section, so old links keep working.

## Building locally

Clone with submodules (or run `git submodule update --init --recursive`
afterwards):

```sh
git clone --recurse-submodules https://github.com/madhur/madhur.github.com.git
```

Live-reloading dev server on <http://localhost:1313>:

```sh
hugo server -D
```

Production build into `public/`:

```sh
hugo build --environment production
```

Posts dated in the future are not built unless you pass `--buildFuture`.

## Writing a post

Add `content/posts/YYYY-MM-DD-slug.md`. The front matter needs a `slug` (the
filename without the date prefix) so the permalink matches the historical
scheme:

```yaml
---
slug: "my-post"
title: My post
date: '2026-08-15'
description: One-line summary
tags:
  - Hugo
draft: false
---
```

## Deployment

`.github/workflows/hugo.yml` builds the site with `hugo --minify` and publishes
`public/` to GitHub Pages on every push to `master`.

## Credits

Design and structure over the years borrowed ideas from:

* [Carl Boettiger](http://carlboettiger.info/index.html)
* [Damien du Toit](http://coda.co.za/)
* [Bilal Syed Hussain](http://bilalh.github.io/)
