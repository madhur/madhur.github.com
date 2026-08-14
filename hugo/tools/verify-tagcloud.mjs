#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import matter from 'gray-matter';

const POSTS_DIR = 'hugo/content/posts';
const TAGS_HTML = 'hugo/public/tags/index.html';

// `hugo build -s hugo -D` (used in Step 3, and throughout this migration) passes -D
// (include drafts) but not -F (include future), matching Hugo's default publish rules:
// draft posts are built, but posts dated after "now" are excluded from the site (and
// therefore from .Site.Taxonomies.tags) until their date arrives. Some of the 278
// migrated posts carry future publish dates (scheduled content), so the independent
// recount here must apply the same exclusion Hugo applies, or it isn't actually
// independently verifying the same output.
const now = new Date();

// Hugo's taxonomy keys are case-insensitive: two tags that differ only in case (e.g.
// "Github" and "GitHub", or "WireGuard" and "Wireguard") collapse into a single
// .Site.Taxonomies.tags entry with a combined post count. Hugo also title-cases the
// auto-generated term page label (e.g. front-matter tag "ionic" renders as "Ionic",
// "Pass The Hash" renders as "Pass the Hash") using rules the shortcode does not
// control and does not implement — that title-casing is a Hugo/PaperMod built-in, not
// something Task 5 built, so it is out of scope for this check. What Task 5 *did*
// build is the weight math, keyed off the tag's URL slug (which the shortcode derives
// with `| urlize`, mirroring Hugo's own taxonomy term URL). So this script:
//   1. groups posts by the same case-insensitive slug Hugo/urlize would produce
//      (lowercase, whitespace collapsed to hyphens — matches observed hrefs like
//      "/tags/pass-the-hash/", "/tags/tcp/ip/", "/tags/.net/", "/tags/node.js/"),
//   2. recomputes the expected weight per merged slug from the real post count, and
//   3. checks the rendered HTML for a tag-cloud entry at that href with that weight,
//      regardless of the visible label text Hugo chose to display for it.
function slugify(tag) {
  return tag.trim().toLowerCase().replace(/\s+/g, '-');
}

const counts = {};
for (const f of fs.readdirSync(POSTS_DIR).filter((f) => f.endsWith('.md'))) {
  const { data } = matter(fs.readFileSync(path.join(POSTS_DIR, f), 'utf8'));
  if (data.date && new Date(data.date) > now) continue;
  for (const tag of data.tags || []) {
    const slug = slugify(tag);
    counts[slug] = (counts[slug] || 0) + 1;
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
for (const [slug, count] of Object.entries(counts)) {
  const expected = expectedWeight(count);
  const escapedSlug = slug.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const re = new RegExp(`font-size:\\s*${expected}%"\\s*><a href="/tags/${escapedSlug}/"`);
  if (!re.test(html)) {
    console.error(`MISMATCH: "${slug}" (count=${count}) expected weight ${expected}% not found`);
    failures++;
  }
}
console.log(failures === 0 ? `OK: all ${Object.keys(counts).length} tags match expected weights` : `${failures} mismatches`);
process.exit(failures === 0 ? 0 : 1);
