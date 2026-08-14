# Jekyll to Hugo Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrate madhur.co.in from Jekyll to a dark, responsive Hugo site built on the PaperMod theme, carrying over all content (278 posts, projects, static pages, legacy tools) while dropping or rebuilding the site's custom Jekyll plugin logic per the approved design spec.

**Architecture:** Build the new Hugo site inside a `hugo/` subdirectory of a new `hugo-migration` branch (created from `source`) so it can be iterated on without disturbing the live Jekyll site, then promote it to the repo root in a single task once verified, and finish with a GitHub Actions deploy workflow. Content conversion (posts, project pages) is done by small, unit-tested Node scripts rather than by hand, since there are 278 posts with embedded Liquid syntax to translate.

**Tech Stack:** Hugo (extended), Hugo PaperMod theme (git submodule), Node.js 22 + `gray-matter` for one-off migration scripts (tested with the built-in `node:test` runner), GitHub Actions for build/deploy.

**Spec:** `docs/superpowers/specs/2026-08-14-jekyll-to-hugo-migration-design.md`

## Global Constraints

- Theme is Hugo PaperMod, customized — not a from-scratch theme, not a different theme.
- Site must default to dark mode and be fully responsive (PaperMod provides both natively).
- Comments: giscus (GitHub Discussions-backed). No Disqus comment history import — clean break.
- Search: PaperMod's built-in Fuse.js client-side search page.
- Hosting: GitHub Pages, deployed via GitHub Actions (not the old gulp-git commit/push flow).
- Drop entirely, do not port: `_plugins/octokit.rb` embeds, the Google Custom Search widget on
  `/results/`, the AngularJS search on `/404.md`, `ghbtns.com` badges, the Feedburner link,
  `ph_postings_meta.json`, `serviceWorker.js`, `_scripts/*.rb`, and `.htaccess` (its redirect
  rules target an unrelated third-party domain, `mark.reid.name/iem` — confirmed vestigial
  boilerplate, not madhur.co.in redirects; do not port them as Hugo `aliases`).
  ISSUE(complexity): 0.68
- `silverdemo/` (Silverlight) is carried over as archived static files only — it is not
  functional in any modern browser regardless of host, on Jekyll or Hugo.
- Rebuild as custom Hugo code (not a built-in feature): the weighted tag cloud, using the same
  75%–280% font-size scaling formula as the original `_plugins/tag_cloud.rb`.
- All 278 posts, all `projects/*.md` + `_data/projects/*.yml`, all static sections
  (`code/`, `papers/`, `work/`, `info/`, `donate/`, `contact/`, `privacy/`), and
  `leetcodeformat/`/`leetcode-format.html` must be migrated — nothing in scope is left behind.

---

## Task 1: Scaffold the Hugo project with the PaperMod theme

**Files:**
- Create: `hugo/hugo.toml`
- Create: `hugo/themes/PaperMod/` (git submodule)
- Create: `hugo/content/_index.md`

**Interfaces:**
- Produces: a working Hugo site rooted at `hugo/` that later tasks add content, data, and
  templates into. All later tasks assume `hugo/` exists with `theme = "PaperMod"` configured.

- [ ] **Step 1: Install Hugo (extended) and verify**

```bash
sudo pacman -S hugo
hugo version
```

Expected: version output contains `extended` (needed for PaperMod's asset pipeline). If the
Arch package is not extended, download the `extended` build from
https://github.com/gohugoio/hugo/releases instead and put it on `PATH`.

- [ ] **Step 2: Create the migration branch**

```bash
git checkout source
git pull
git checkout -b hugo-migration
```

- [ ] **Step 3: Scaffold the Hugo site**

```bash
hugo new site hugo --format toml
```

Expected: creates `hugo/` with `hugo.toml`, `content/`, `archetypes/`, `static/`, `layouts/`,
`data/`, `themes/`.

- [ ] **Step 4: Add PaperMod as a git submodule**

```bash
git submodule add --depth=1 https://github.com/adityatelange/hugo-PaperMod.git hugo/themes/PaperMod
git submodule update --init --recursive
```

- [ ] **Step 5: Write minimal site config**

Overwrite `hugo/hugo.toml`:

```toml
baseURL = "https://madhur.co.in/"
languageCode = "en-us"
title = "Coding it my way"
theme = "PaperMod"

[pagination]
  pagerSize = 15
```

- [ ] **Step 6: Create a placeholder home page and verify the server runs**

```bash
mkdir -p hugo/content
cat > hugo/content/_index.md <<'EOF'
---
title: Home
---
Hugo + PaperMod scaffold is working.
EOF
```

Run: `hugo server -s hugo -D &` then `curl -s http://localhost:1313/ | grep -o 'Hugo + PaperMod scaffold is working.'`
Expected: prints the sentence, confirming the server renders the PaperMod base layout. Stop the
server (`kill %1`) after confirming.

- [ ] **Step 7: Commit**

```bash
git add hugo .gitmodules
git commit -m "feat: scaffold Hugo site with PaperMod theme"
```

---

## Task 2: Site-wide config — dark theme, analytics, feeds, robots, favicon, raw HTML

**Files:**
- Modify: `hugo/hugo.toml`
- Create: `hugo/layouts/partials/extend_head.html`
- Create: `hugo/static/CNAME`

**Interfaces:**
- Consumes: `hugo/hugo.toml` from Task 1.
- Produces: `[markup.goldmark.renderer] unsafe = true` — later tasks (projects, static pages)
  rely on this to render embedded `<iframe>`s (PayPal donate form, Slideshare/ProductHunt
  embeds) that raw Goldmark would otherwise strip.

- [ ] **Step 1: Extend `hugo/hugo.toml` with PaperMod params, GA, feeds, robots**

Append to `hugo/hugo.toml`:

```toml
enableRobotsTXT = true
googleAnalytics = "G-N14VDHYFHQ"

[params]
  defaultTheme = "dark"
  disableThemeToggle = false
  ShowReadingTime = true
  ShowShareButtons = true
  ShowPostNavLinks = true
  ShowBreadCrumbs = true
  ShowCodeCopyButtons = true
  ShowRssButtonInSectionTermList = true
  comments = true

  [params.homeInfoParams]
    Title = "Hi, I'm Madhur 👋"
    Content = "A software developer who likes building things and writing about technology."

  [params.assets]
    disableHLJS = true

[markup]
  [markup.highlight]
    noClasses = false
  [markup.goldmark.renderer]
    unsafe = true

[outputs]
  home = ["HTML", "RSS", "JSON"]
```

Note: `googleAnalytics` is only emitted by PaperMod when Hugo runs with
`--environment production` (via `hugo --minify` in the deploy workflow, Task 9); `hugo server`
in development does not load it — this replaces the old `{% if site.mode == 'prod' %}` gate with
Hugo's built-in environment mechanism, no custom code needed.

- [ ] **Step 2: Preserve the existing favicon (Gravatar-hosted)**

```bash
mkdir -p hugo/layouts/partials
cat > hugo/layouts/partials/extend_head.html <<'EOF'
<link rel="shortcut icon" href="http://www.gravatar.com/avatar/5352cde0b084abcd6d4d783c08a51c76?s=16" />
EOF
```

- [ ] **Step 3: Copy the CNAME file for the custom domain**

```bash
cp CNAME hugo/static/CNAME
```

- [ ] **Step 4: Port the print-friendly stylesheet, simplifying the old popup-window trick**

The old site's `Clickheretoprint()` opened post content in a new window styled by `print.css` —
a workaround for browsers that didn't respect `@media print` well in 2012. Modern browsers'
native print dialogs (Ctrl+P) do respect `@media print` correctly, so the popup-window
JavaScript is no longer needed; only the stylesheet itself is worth porting. This is a
deliberate simplification of the "needs custom rework" item from the design spec, not a silent
drop — the printable output is preserved, the obsolete delivery mechanism isn't.

```bash
mkdir -p hugo/static/css
cp files/css/print.css hugo/static/css/print.css
```

Add the print stylesheet link to `hugo/layouts/partials/extend_head.html` (appending to the
favicon line added in Step 2):

```bash
cat >> hugo/layouts/partials/extend_head.html <<'EOF'
<link rel="stylesheet" type="text/css" media="print" href="/css/print.css" />
EOF
```

- [ ] **Step 5: Build and verify**

Run: `hugo build -s hugo -D --environment production`
Expected: exits 0. Then:

```bash
grep -c "G-N14VDHYFHQ" hugo/public/index.html
test -f hugo/public/robots.txt && cat hugo/public/robots.txt
test -f hugo/public/CNAME && cat hugo/public/CNAME
test -f hugo/public/css/print.css && echo "OK: print.css"
grep -o 'media="print"' hugo/public/index.html
```

Expected: GA snippet present, `robots.txt` contains `Allow: /`, `CNAME` contains
`www.madhur.co.in`, `OK: print.css`, and `media="print"` found in the page head.

- [ ] **Step 6: Commit**

```bash
git add hugo
git commit -m "feat: configure dark theme, analytics, feeds, robots, favicon, print stylesheet"
```

---

## Task 3: Post migration script (tested) and full post conversion

**Files:**
- Create: `hugo/tools/package.json`
- Create: `hugo/tools/migrate-posts/migrate.mjs`
- Create: `hugo/tools/migrate-posts/migrate.test.mjs`
- Create: `hugo/content/posts/*.md` (278 files, generated by the script)

**Interfaces:**
- Produces: `convertBody(body: string): string` and
  `convertFrontMatter(data: object, filename: string): object` — pure functions, exported from
  `migrate.mjs`, exercised directly by the test file. `migratePost(srcPath: string): {filename,
  out}` — the file-level function `main()` calls to do the actual conversion.

- [ ] **Step 1: Set up the tools package**

```bash
mkdir -p hugo/tools/migrate-posts
cat > hugo/tools/package.json <<'EOF'
{
  "name": "migration-tools",
  "private": true,
  "type": "module",
  "dependencies": {
    "gray-matter": "^4.0.3"
  }
}
EOF
cd hugo/tools && npm install && cd -
```

- [ ] **Step 2: Write the failing tests**

Create `hugo/tools/migrate-posts/migrate.test.mjs`:

```js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { convertBody, convertFrontMatter } from './migrate.mjs';

test('converts highlight blocks to fenced code blocks', () => {
  const input = '{% highlight javascript %}\nconsole.log(1);\n{% endhighlight %}';
  assert.equal(convertBody(input), '```javascript\nconsole.log(1);\n```');
});

test('strips raw/endraw wrapper tags but keeps their inner content', () => {
  const input = '{% raw %}\n{% for x in y %}\n{% endraw %}\n';
  assert.equal(convertBody(input), '{% for x in y %}\n');
});

test('unescapes the literal-string trick used to display Liquid syntax', () => {
  const input = '{{ "{% if article.previous? " }}%}';
  assert.equal(convertBody(input), '{% if article.previous? %}');
});

test('converts post_url tags to the equivalent Hugo permalink', () => {
  const input = 'See [my post]({% post_url 2011-09-01-runningjekyllwindows %}) for details.';
  assert.equal(
    convertBody(input),
    'See [my post](/blog/2011/09/01/runningjekyllwindows.html) for details.'
  );
});

test('leaves unrelated brace text untouched (e.g. Python format strings)', () => {
  const input = "print('%s has {%s}' % (1, 2))";
  assert.equal(convertBody(input), input);
});

test('maps front matter fields to Hugo equivalents', () => {
  const data = {
    title: 'Reverse engineering Google chrome extensions',
    excerpt: 'How to reverse engineer Google Chrome extensions',
    disqus_id: '/2011/06/03/reverse engineer/',
    location: 'Pittsburgh, US',
    time: '12:18 AM',
    tags: ['Reverse Engineering', 'Chrome'],
  };
  const fm = convertFrontMatter(data, '2011-06-03-reverseengineerchrome.md');
  assert.equal(fm.title, data.title);
  assert.equal(fm.date, '2011-06-03');
  assert.equal(fm.description, data.excerpt);
  assert.deepEqual(fm.tags, data.tags);
  assert.deepEqual(fm.params, {
    disqus_id: data.disqus_id,
    location: data.location,
    time: data.time,
  });
});

test('front-matter date override takes precedence over the filename date', () => {
  const data = { title: 'X', date: '2020-05-20' };
  const fm = convertFrontMatter(data, '2020-05-16-http-timeouts.md');
  assert.equal(fm.date, '2020-05-20');
});

test('front-matter slug override is preserved without renaming the file', () => {
  const data = { title: 'X', slug: 'custom-slug' };
  const fm = convertFrontMatter(data, '2020-01-12-git-prepare-commit-message-jira-id.md');
  assert.equal(fm.slug, 'custom-slug');
});

test('categories are preserved as a native Hugo taxonomy', () => {
  const data = { title: 'X', categories: ['Security'] };
  const fm = convertFrontMatter(data, '2012-01-01-x.md');
  assert.deepEqual(fm.categories, ['Security']);
});

test('posts with no optional fields produce no params block', () => {
  const data = { title: 'X' };
  const fm = convertFrontMatter(data, '2012-01-01-x.md');
  assert.equal(fm.params, undefined);
});
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `cd hugo/tools && node --test migrate-posts/migrate.test.mjs`
Expected: FAIL — `Cannot find module './migrate.mjs'` (it doesn't exist yet).

- [ ] **Step 4: Implement the migration script**

Create `hugo/tools/migrate-posts/migrate.mjs`:

```js
#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import matter from 'gray-matter';

export function convertBody(body) {
  let out = body;
  // Unescape Jekyll's "print literal Liquid syntax" trick: {{ "TEXT" }} -> TEXT
  out = out.replace(/\{\{\s*"([^"]*)"\s*\}\}/g, '$1');
  // Raw/endraw wrappers are meaningless to Goldmark (it never executes {% %} anyway) — drop them
  out = out.replace(/\{%\s*raw\s*%\}\s*\n?/g, '');
  out = out.replace(/\{%\s*endraw\s*%\}\s*\n?/g, '');
  // {% highlight LANG %}...{% endhighlight %} -> fenced code blocks
  out = out.replace(/\{%\s*highlight\s+([a-zA-Z0-9_+-]+)\s*%\}/g, '```$1');
  out = out.replace(/\{%\s*endhighlight\s*%\}/g, '```');
  // {% post_url YYYY-MM-DD-slug %} -> the equivalent Hugo permalink (same slug, same
  // /blog/:year/:month/:day/:slug.html permalink scheme configured in Task 8)
  out = out.replace(
    /\{%\s*post_url\s+(\d{4})-(\d{2})-(\d{2})-([\w-]+)\s*%\}/g,
    (_, y, m, d, slug) => `/blog/${y}/${m}/${d}/${slug}.html`
  );
  return out;
}

export function convertFrontMatter(data, filename) {
  const dateMatch = filename.match(/^(\d{4}-\d{2}-\d{2})-/);
  const fileDate = dateMatch ? dateMatch[1] : null;

  const out = {
    title: data.title,
    date: data.date || fileDate,
    description: data.excerpt || '',
    tags: data.tags || [],
    draft: false,
  };
  if (data.categories) out.categories = data.categories;
  if (data.slug) out.slug = data.slug;

  const params = {};
  if (data.disqus_id) params.disqus_id = data.disqus_id;
  if (data.location) params.location = data.location;
  if (data.time) params.time = data.time;
  if (Object.keys(params).length) out.params = params;

  return out;
}

export function migratePost(srcPath) {
  const raw = fs.readFileSync(srcPath, 'utf8');
  const { data, content } = matter(raw);
  const filename = path.basename(srcPath);
  const frontMatter = convertFrontMatter(data, filename);
  const body = convertBody(content);
  const out = matter.stringify(body, frontMatter);
  return { filename, out };
}

function main() {
  const srcDir = process.argv[2] || '../../../_posts';
  const destDir = process.argv[3] || '../../content/posts';
  fs.mkdirSync(destDir, { recursive: true });
  const files = fs.readdirSync(srcDir).filter((f) => f.endsWith('.md'));
  for (const f of files) {
    const { filename, out } = migratePost(path.join(srcDir, f));
    fs.writeFileSync(path.join(destDir, filename), out, 'utf8');
  }
  console.log(`Migrated ${files.length} posts to ${destDir}`);
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `cd hugo/tools && node --test migrate-posts/migrate.test.mjs`
Expected: PASS, all 10 tests green.

- [ ] **Step 6: Run the script against the real posts**

```bash
cd hugo/tools/migrate-posts
node migrate.mjs ../../../_posts ../../content/posts
cd -
```

Expected output: `Migrated 278 posts to ../../content/posts`.

- [ ] **Step 7: Verify no unconverted Liquid markers remain**

```bash
grep -rlE '\{%\s*(highlight|endhighlight|raw|endraw|post_url)\b' hugo/content/posts/ || echo "CLEAN"
```

Expected: `CLEAN` (no matches). If any file is listed, inspect it — it means a variant of one of
these tags wasn't covered by the regexes in Step 4 (e.g. unusual whitespace); fix the regex and
re-run Steps 5–7.

- [ ] **Step 8: Verify the post count matches the source**

```bash
test "$(ls hugo/content/posts | wc -l)" = "$(ls _posts | wc -l)" && echo "COUNT MATCHES"
```

Expected: `COUNT MATCHES`.

- [ ] **Step 9: Commit**

```bash
git add hugo/tools hugo/content/posts
git commit -m "feat: migrate all 278 posts from Jekyll to Hugo content"
```

---

## Task 4: Projects data and content migration

**Files:**
- Create: `hugo/tools/lib/slugize.mjs`
- Create: `hugo/tools/lib/slugize.test.mjs`
- Create: `hugo/tools/migrate-projects/migrate.mjs`
- Create: `hugo/tools/migrate-projects/migrate.test.mjs`
- Create: `hugo/data/projects/*.yml`, `hugo/data/oldprojects/*.yml`
- Create: `hugo/content/projects/*.md` (from `projects/*.md`, 20 files)
- Create: `hugo/content/projects/_index.md`
- Create: `hugo/layouts/projects/list.html`

**Interfaces:**
- Consumes: `hugo/tools/package.json` (gray-matter) from Task 3.
- Produces: `slugize(text: string): string`, replicating `_plugins/core_ext.rb`'s exact
  behavior — used both for project filenames here and available for any later task needing the
  same slug format.

- [ ] **Step 1: Write the failing slugize test**

Create `hugo/tools/lib/slugize.test.mjs`:

```js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { slugize } from './slugize.mjs';

test('lowercases and replaces whitespace/dots with hyphens', () => {
  assert.equal(slugize('Feed Notifier'), 'feed-notifier');
  assert.equal(slugize('OSX Hdd Usage'), 'osx-hdd-usage');
});

test('strips characters that are not word characters or hyphens', () => {
  assert.equal(slugize("Realtime Google Analytics Count in Tab!"), 'realtime-google-analytics-count-in-tab');
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd hugo/tools && node --test lib/slugize.test.mjs`
Expected: FAIL — module not found.

- [ ] **Step 3: Implement slugize**

Create `hugo/tools/lib/slugize.mjs`:

```js
// Replicates _plugins/core_ext.rb's String#slugize exactly:
//   self.downcase.gsub(/[\s\.]/, '-').gsub(/[^\w\d\-]/, '').downcase
export function slugize(text) {
  return text
    .toLowerCase()
    .replace(/[\s.]/g, '-')
    .replace(/[^\w\d-]/g, '')
    .toLowerCase();
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd hugo/tools && node --test lib/slugize.test.mjs`
Expected: PASS, 2 tests green.

- [ ] **Step 5: Write the failing migrate-projects test**

Create `hugo/tools/migrate-projects/migrate.test.mjs`:

```js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { convertProjectFrontMatter } from './migrate.mjs';

test('drops the dead octokit "github" field and keeps title/img', () => {
  const data = { title: 'LeetCode Format Extension', layout: 'project-detail', github: 'x', img: ['/images/format-demo.gif'] };
  const fm = convertProjectFrontMatter(data);
  assert.equal(fm.title, 'LeetCode Format Extension');
  assert.deepEqual(fm.img, ['/images/format-demo.gif']);
  assert.equal(fm.github, undefined);
  assert.equal(fm.layout, undefined);
});

test('handles projects with no img field', () => {
  const fm = convertProjectFrontMatter({ title: 'Bookmart' });
  assert.equal(fm.title, 'Bookmart');
  assert.equal(fm.img, undefined);
});
```

- [ ] **Step 6: Run test to verify it fails**

Run: `cd hugo/tools && node --test migrate-projects/migrate.test.mjs`
Expected: FAIL — module not found.

- [ ] **Step 7: Implement migrate-projects**

Create `hugo/tools/migrate-projects/migrate.mjs`:

```js
#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import matter from 'gray-matter';
import { slugize } from '../lib/slugize.mjs';

export function convertProjectFrontMatter(data) {
  const out = { title: data.title };
  if (data.img) out.img = data.img;
  return out;
}

export function migrateProject(srcPath) {
  const raw = fs.readFileSync(srcPath, 'utf8');
  const { data, content } = matter(raw);
  const frontMatter = convertProjectFrontMatter(data);
  const destFilename = `${slugize(path.basename(srcPath, '.md'))}.md`;
  const out = matter.stringify(content, frontMatter);
  return { destFilename, out };
}

function main() {
  const srcDir = process.argv[2] || '../../../projects';
  const destDir = process.argv[3] || '../../content/projects';
  fs.mkdirSync(destDir, { recursive: true });
  const files = fs.readdirSync(srcDir).filter((f) => f.endsWith('.md'));
  for (const f of files) {
    const { destFilename, out } = migrateProject(path.join(srcDir, f));
    fs.writeFileSync(path.join(destDir, destFilename), out, 'utf8');
  }
  console.log(`Migrated ${files.length} project pages to ${destDir}`);
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}
```

- [ ] **Step 8: Run test to verify it passes, then run against real data**

Run: `cd hugo/tools && node --test migrate-projects/migrate.test.mjs`
Expected: PASS, 2 tests green.

```bash
cd hugo/tools/migrate-projects
node migrate.mjs ../../../projects ../../content/projects
cd -
test "$(ls hugo/content/projects | wc -l)" = "$(ls projects/*.md | wc -l)" && echo "COUNT MATCHES"
```

Expected: `Migrated 20 project pages...` and `COUNT MATCHES`.

- [ ] **Step 9: Copy and normalize the projects data files**

```bash
mkdir -p hugo/data/projects hugo/data/oldprojects
cp _data/projects/*.yml hugo/data/projects/
cp _data/oldprojects/*.y*ml hugo/data/oldprojects/
# Normalize tab-indented `publish:\tno` / `publish:\tyes` into standard YAML booleans
sed -i -E 's/publish:\t?(no|false)/publish: false/; s/publish:\t?(yes|true)/publish: true/' hugo/data/oldprojects/*.y*ml
```

Verify all data files still parse as valid YAML. First ensure `js-yaml` is installed directly
(don't rely on it being hoisted transitively from `gray-matter`):

```bash
cd hugo/tools && npm install js-yaml && cd -
```

Then parse every data file with it:

```bash
for f in hugo/data/projects/*.yml hugo/data/oldprojects/*.y*ml; do
  node --input-type=commonjs -e "
    const yaml = require('$(pwd)/hugo/tools/node_modules/js-yaml');
    const fs = require('fs');
    yaml.load(fs.readFileSync('$f', 'utf8'));
    console.log('OK: $f');
  "
done
```

Expected: `OK: <path>` printed for every data file, no YAML parse errors.

- [ ] **Step 10: Write the projects list template and index page**

Create `hugo/content/projects/_index.md`:

```markdown
---
title: Projects
---
```

Create `hugo/layouts/projects/list.html`:

```html
{{ define "main" }}
<h1>{{ .Title }}</h1>
{{ $detailPages := where .Site.RegularPages "Section" "projects" }}
{{ range site.Data.projects }}
  {{ if .publish }}
  <h2><i class="{{ .icon }}"></i> {{ .name }}</h2>
  <ul>
    {{ range .projects }}
      {{ if .publish }}
        {{ $slug := printf "%s" (.file | urlize) }}
        {{ $match := where $detailPages "File.BaseFileName" $slug }}
        <li>
          {{ if $match }}
            <a href="{{ (index $match 0).Permalink }}">{{ .project }}</a>
          {{ else }}
            <strong>{{ .project }}</strong>
          {{ end }}
          — {{ .description }}
          {{ with .languages }}<em>({{ delimit . ", " }})</em>{{ end }}
        </li>
      {{ end }}
    {{ end }}
  </ul>
  {{ end }}
{{ end }}
{{ end }}
```

- [ ] **Step 11: Build and verify**

Run: `hugo build -s hugo -D`
Expected: exits 0.

```bash
grep -o "LeetCode Format" hugo/public/projects/index.html
```

Expected: prints `LeetCode Format`, confirming the data-driven listing renders. If the build
fails on a template function, fix the template per the error message (Hugo's error output names
the exact line/function) and re-run — this is expected first-pass template iteration.

- [ ] **Step 12: Commit**

```bash
git add hugo/tools hugo/data hugo/content/projects hugo/layouts/projects
git commit -m "feat: migrate projects data and content to Hugo"
```

---

## Task 5: Weighted tag cloud shortcode

**Files:**
- Create: `hugo/layouts/shortcodes/tagcloud.html`
- Modify: `hugo/layouts/_default/terms.html` (or create if PaperMod doesn't ship one — check
  `hugo/themes/PaperMod/layouts/_default/terms.html` first)
- Create: `hugo/tools/verify-tagcloud.mjs`

**Interfaces:**
- Consumes: `.Site.Taxonomies.tags` (Hugo built-in, populated once Task 3's posts exist).
- Produces: a `{{< tagcloud >}}` shortcode usable in any content page.

- [ ] **Step 1: Write the tag cloud shortcode**

Create `hugo/layouts/shortcodes/tagcloud.html`:

```html
{{/* Weighted tag cloud: mirrors _plugins/tag_cloud.rb's 75%-280% font-size scaling by post count */}}
{{ $minSize := 75 }}
{{ $maxSize := 280 }}
{{ $tags := .Site.Taxonomies.tags }}
{{ $counts := slice }}
{{ range $name, $pages := $tags }}
  {{ $counts = $counts | append (len $pages) }}
{{ end }}
{{ $minCount := 0 }}
{{ $maxCount := 0 }}
{{ if gt (len $counts) 0 }}
  {{ $sorted := sort $counts }}
  {{ $minCount = index $sorted 0 }}
  {{ $maxCount = index $sorted (sub (len $sorted) 1) }}
{{ end }}
<div class="tag-cloud">
{{ range $name, $pages := $tags }}
  {{ $count := len $pages }}
  {{ $weight := $minSize }}
  {{ if ne $maxCount $minCount }}
    {{ $weight = add (div (mul (sub $count $minCount) (sub $maxSize $minSize)) (sub $maxCount $minCount)) $minSize }}
  {{ end }}
  <span style="font-size: {{ $weight }}%"><a href="/tags/{{ $name | urlize }}/" title="{{ $count }} post{{ if ne $count 1 }}s{{ end }}">{{ $name }}</a></span>
{{ end }}
</div>
```

- [ ] **Step 2: Add the shortcode to the tags list page**

```bash
mkdir -p hugo/layouts/_default
test -f hugo/layouts/_default/terms.html || cp hugo/themes/PaperMod/layouts/_default/terms.html hugo/layouts/_default/terms.html
```

Edit `hugo/layouts/_default/terms.html`: add `{{< tagcloud >}}` immediately after the
`{{ define "main" }}` line (or after the page title, if the file has one) — open the file first
to find the exact insertion point before editing, since PaperMod's template content varies by
version.

- [ ] **Step 3: Build**

Run: `hugo build -s hugo -D`
Expected: exits 0. Fix any Hugo template function errors reported (e.g. argument order for
`add`/`div`/`mul`/`sub`, all of which take `(a, b)` and compute `a OP b`) and re-run until clean.

- [ ] **Step 4: Write an independent verification script**

Create `hugo/tools/verify-tagcloud.mjs` — recomputes expected weights straight from the migrated
post front matter (independent of the template) and cross-checks the rendered HTML:

```js
#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import matter from 'gray-matter';

const POSTS_DIR = 'hugo/content/posts';
const TAGS_HTML = 'hugo/public/tags/index.html';

const counts = {};
for (const f of fs.readdirSync(POSTS_DIR).filter((f) => f.endsWith('.md'))) {
  const { data } = matter(fs.readFileSync(path.join(POSTS_DIR, f), 'utf8'));
  for (const tag of data.tags || []) {
    counts[tag] = (counts[tag] || 0) + 1;
  }
}

const values = Object.values(counts);
const minCount = Math.min(...values);
const maxCount = Math.max(...values);
const MIN_SIZE = 75;
const MAX_SIZE = 280;

function expectedWeight(count) {
  if (maxCount === minCount) return MIN_SIZE;
  return Math.trunc(((count - minCount) * (MAX_SIZE - MIN_SIZE)) / (maxCount - minCount)) + MIN_SIZE;
}

const html = fs.readFileSync(TAGS_HTML, 'utf8');
let failures = 0;
for (const [tag, count] of Object.entries(counts)) {
  const expected = expectedWeight(count);
  const re = new RegExp(`font-size:\\s*${expected}%"\\s*><a[^>]*>${tag.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}<`);
  if (!re.test(html)) {
    console.error(`MISMATCH: "${tag}" (count=${count}) expected weight ${expected}% not found`);
    failures++;
  }
}
console.log(failures === 0 ? `OK: all ${Object.keys(counts).length} tags match expected weights` : `${failures} mismatches`);
process.exit(failures === 0 ? 0 : 1);
```

- [ ] **Step 5: Run the verification**

Run: `node hugo/tools/verify-tagcloud.mjs`
Expected: `OK: all N tags match expected weights`, exit code 0. If it reports mismatches, compare
the shortcode's template math against `expectedWeight()` above (same formula) and fix the
template.

- [ ] **Step 6: Commit**

```bash
git add hugo/layouts hugo/tools/verify-tagcloud.mjs
git commit -m "feat: add weighted tag cloud shortcode"
```

---

## Task 6: Static sections, leetcodeformat, and silverdemo

**Files:**
- Create: `hugo/content/{code,papers,work,info,donate,contact}/_index.md`
- Create: `hugo/content/privacy/{hddusage,vocabbuilder,weather}.md`
- Create: `hugo/static/leetcodeformat/data.json`
- Create: `hugo/static/leetcode-format.html`
- Create: `hugo/static/silverdemo/` (copied as-is)

**Interfaces:**
- Consumes: `unsafe = true` Goldmark config from Task 2 (these pages contain raw `<img>`/
  `<iframe>` HTML that must pass through unescaped).

- [ ] **Step 1: Migrate the six single-page sections**

All six (`code`, `papers`, `work`, `info`, `donate`, `contact`) are plain Markdown with no Liquid
— only their front matter needs trimming (drop `layout`/`section`/`top`, keep `title`) and the
body copies verbatim:

```bash
for section in code papers work info donate contact; do
  mkdir -p "hugo/content/$section"
  title=$(sed -n '/^title:/{s/^title:\s*//;p;q}' "$section/index.markdown")
  {
    echo "---"
    echo "title: $title"
    echo "---"
    echo
    sed '1,/^---$/d; 1,/^---$/d' "$section/index.markdown"
  } > "hugo/content/$section/_index.md"
done
```

- [ ] **Step 2: Migrate the three privacy policy pages**

```bash
mkdir -p hugo/content/privacy
for f in hddusage vocabbuilder weather; do
  title=$(sed -n '/^title:/{s/^title:\s*//;p;q}' "privacy/$f.md")
  {
    echo "---"
    echo "title: $title"
    echo "---"
    echo
    sed '1,/^---$/d; 1,/^---$/d' "privacy/$f.md"
  } > "hugo/content/privacy/$f.md"
done
```

- [ ] **Step 3: Copy leetcodeformat and the extension privacy page as static assets**

```bash
mkdir -p hugo/static/leetcodeformat
cp leetcodeformat/data.json hugo/static/leetcodeformat/data.json
cp leetcode-format.html hugo/static/leetcode-format.html
```

- [ ] **Step 4: Archive silverdemo as inert static files**

```bash
cp -r silverdemo hugo/static/silverdemo
```

- [ ] **Step 5: Build and verify every page renders**

Run: `hugo build -s hugo -D`
Expected: exits 0.

```bash
for section in code papers work info donate contact privacy/hddusage privacy/vocabbuilder privacy/weather; do
  test -f "hugo/public/$section/index.html" && echo "OK: $section" || echo "MISSING: $section"
done
test -f hugo/public/leetcodeformat/data.json && echo "OK: leetcodeformat/data.json"
test -f hugo/public/leetcode-format.html && echo "OK: leetcode-format.html"
test -f hugo/public/silverdemo/Index.html && echo "OK: silverdemo"
```

Expected: `OK` printed for all nine sections plus the three static-asset checks, no `MISSING`
lines.

- [ ] **Step 6: Commit**

```bash
git add hugo/content hugo/static
git commit -m "feat: migrate static sections, leetcodeformat, and archived silverdemo"
```

---

## Task 7: Search (Fuse.js) and comments (giscus)

**Files:**
- Create: `hugo/content/search.md`
- Modify: `hugo/hugo.toml`

**Interfaces:**
- Consumes: `[outputs] home = ["HTML", "RSS", "JSON"]` from Task 2 (Fuse.js search reads the
  generated `index.json`).

- [ ] **Step 1: Add the PaperMod search page**

Create `hugo/content/search.md`:

```markdown
---
title: Search
layout: search
description: Search posts
summary: search
placeholder: Search posts...
---
```

- [ ] **Step 2: Configure giscus params**

Append to `hugo/hugo.toml`:

```toml
[params.giscus]
  repo = "madhur/madhur.github.com"
  repoId = "REPLACE_WITH_REPO_ID_FROM_GISCUS_APP"
  category = "Comments"
  categoryId = "REPLACE_WITH_CATEGORY_ID_FROM_GISCUS_APP"
  mapping = "pathname"
  strict = "0"
  reactionsEnabled = "1"
  emitMetadata = "0"
  inputPosition = "bottom"
  theme = "dark"
  lang = "en"
```

**Manual step required (cannot be automated from this repo):** before this config works, go to
the repo's GitHub Settings → General → Features and enable "Discussions". Then visit
https://giscus.app, enter `madhur/madhur.github.com`, pick (or create) a "Comments" discussion
category, and copy the generated `data-repo-id` and `data-category-id` values into
`repoId`/`categoryId` above, replacing the `REPLACE_WITH_...` placeholders.

- [ ] **Step 3: Build and verify the search page and JSON index**

Run: `hugo build -s hugo -D`
Expected: exits 0.

```bash
test -f hugo/public/index.json && echo "OK: index.json"
grep -o 'Search posts' hugo/public/search/index.html
```

Expected: `OK: index.json` and `Search posts` printed.

- [ ] **Step 4: Commit**

```bash
git add hugo/content/search.md hugo/hugo.toml
git commit -m "feat: enable Fuse.js search and configure giscus comments"
```

Note: leave the `REPLACE_WITH_...` placeholders in place if the manual giscus.app step hasn't
been done yet — comments will simply not render until real IDs are filled in; this does not
block the rest of the migration.

---

## Task 8: Promote the Hugo site to the repo root and retire Jekyll/Gulp artifacts

**Files:**
- Move: everything under `hugo/` to the repo root
- Delete: `_layouts/`, `_includes/`, `_plugins/`, `_posts/`, `_data/`, `_scripts/`,
  `.jekyll-cache/`, `Gulpfile.js`, `Gemfile`, `Gemfile.lock`, `node_modules/`, `files/`,
  `blog/`, `projects/`, `code/`, `papers/`, `work/`, `info/`, `donate/`, `contact/`,
  `privacy/`, `leetcodeformat/`, `leetcode-format.html`, `silverdemo/`, `index.md`, `404.md`,
  `.htaccess`, `serviceWorker.js`, `atom.xml`, `robots.txt`, `ph_postings_meta.json`,
  `_config.yml`, `package.json`, `package-lock.json`, `.nvmrc`, `.ruby-version`
- Delete: `hugo/tools/` (one-off migration scripts, no longer needed post-migration)

**Interfaces:**
- Consumes: the fully-built `hugo/` tree from Tasks 1–7.
- Produces: a repo root that is a normal Hugo project (`hugo.toml`, `content/`, `layouts/`,
  `static/`, `data/`, `themes/` all at top level) — everything after this task assumes root-level
  Hugo, not `hugo/`-prefixed paths.

- [ ] **Step 1: Confirm every migrated file is accounted for before deleting sources**

```bash
diff <(cd hugo/content/posts && ls | sort) <(cd _posts && ls | sort) && echo "POSTS MATCH"
diff <(cd hugo/content/projects && ls | sort) <(cd projects && ls -1 *.md | node -e "process.stdin.on('data', d => process.stdout.write(d))" | sort) || true
```

Expected: `POSTS MATCH`. (The projects diff will show filename differences since names were
slugized in Task 4 — that's expected; visually confirm the count matches instead:
`ls hugo/content/projects | wc -l` should equal `ls projects/*.md | wc -l`, i.e. 20.)

- [ ] **Step 2: Delete the one-off migration tooling (no longer needed)**

```bash
git rm -r hugo/tools
```

- [ ] **Step 3: Move the Hugo tree to the repo root**

```bash
git mv hugo/hugo.toml ./hugo.toml
git mv hugo/content ./content
git mv hugo/layouts ./layouts
git mv hugo/static ./static
git mv hugo/data ./data
git mv hugo/themes ./themes
git mv hugo/archetypes ./archetypes 2>/dev/null || true
rmdir hugo
```

- [ ] **Step 4: Delete retired Jekyll/Gulp/Ruby artifacts**

```bash
git rm -r _layouts _includes _plugins _posts _data _scripts .jekyll-cache \
  Gulpfile.js Gemfile Gemfile.lock node_modules files blog projects code papers work info \
  donate contact privacy leetcodeformat leetcode-format.html silverdemo index.md 404.md \
  .htaccess serviceWorker.js atom.xml robots.txt ph_postings_meta.json _config.yml \
  package.json package-lock.json .nvmrc .ruby-version
```

- [ ] **Step 5: Update `.gitmodules` and re-verify the submodule path**

```bash
cat .gitmodules
```

Expected: the PaperMod submodule path now reads `path = themes/PaperMod` (it was
`hugo/themes/PaperMod`). If `git mv` didn't update it automatically, edit `.gitmodules` by hand
to fix the `path` value, then `git submodule sync`.

- [ ] **Step 6: Build and serve from the repo root**

Run: `hugo build -D --environment production`
Expected: exits 0, produces `public/` at repo root.

Run: `hugo server -D &` then `curl -s http://localhost:1313/ | grep -o "Hi, I'm Madhur"` then
`kill %1`
Expected: prints the homepage greeting, confirming the root-level site serves correctly.

- [ ] **Step 7: Commit**

```bash
git add -A
git commit -m "chore: promote Hugo site to repo root, retire Jekyll/Gulp artifacts"
```

---

## Task 9: GitHub Actions deploy workflow

**Files:**
- Create: `.github/workflows/hugo.yml`

**Interfaces:**
- Consumes: the root-level Hugo project from Task 8.

- [ ] **Step 1: Write the workflow**

Create `.github/workflows/hugo.yml`:

```yaml
name: Deploy Hugo site to GitHub Pages

on:
  push:
    branches: [master]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          submodules: recursive
          fetch-depth: 0

      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v3
        with:
          hugo-version: 'latest'
          extended: true

      - name: Setup Pages
        id: pages
        uses: actions/configure-pages@v5

      - name: Build
        run: hugo --minify --environment production --baseURL "${{ steps.pages.outputs.base_url }}/"

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./public

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

- [ ] **Step 2: Validate the workflow YAML is syntactically correct**

```bash
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/hugo.yml')); print('VALID YAML')"
```

Expected: `VALID YAML`.

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/hugo.yml
git commit -m "feat: add GitHub Actions workflow to build and deploy the Hugo site"
```

**Manual steps required (cannot be automated from this repo, and are outward-facing/hard to
reverse — do not do these without explicit sign-off):**

1. In the GitHub repo's Settings → Pages, change the "Source" to "GitHub Actions" (it's
   currently whatever the old Jekyll `destination: ../site/` + gulp-git flow was using).
2. Merging `hugo-migration` into `master` is what actually takes the new site live — treat this
   as a separate, deliberate cutover step after reviewing the built site (e.g. via a
   `workflow_dispatch` run against `hugo-migration` pointed at a Pages preview, or a local
   `hugo server` walkthrough), not an automatic consequence of finishing this plan.
3. Complete the giscus manual step from Task 7 (enable Discussions, fill in real `repoId`/
   `categoryId`) before or after cutover — comments simply won't render until then.
