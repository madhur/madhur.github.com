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
  out = out.replace(/\{%\s*highlight\s+([a-zA-Z0-9_+#-]+)(?:\s+[^%]*)?\s*%\}/g, '```$1');
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
