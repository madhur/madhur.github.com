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

// Dead Jekyll octokit embed, e.g.:
//   {% comment %}
//   ...
//   {% if site.generate_projects == true %}{% octokit_readme SLControls %}{% endif %}
//   {% endcomment %}
// `{% comment %}` made this fully invisible under Liquid. Goldmark doesn't understand
// Liquid tags, so left as-is it renders as visible garbage text. Drop the whole block,
// contents included — it's dead/broken code (bad credentials path, deprecated auth),
// not an escaping wrapper around content that should survive.
export function stripCommentBlocks(body) {
  return body.replace(/\{%\s*comment\s*%\}[\s\S]*?\{%\s*endcomment\s*%\}\s*\n?/g, '');
}

export function migrateProject(srcPath) {
  const raw = fs.readFileSync(srcPath, 'utf8');
  const { data, content } = matter(raw);
  const frontMatter = convertProjectFrontMatter(data);
  const baseName = path.basename(srcPath, path.extname(srcPath));
  const destFilename = `${slugize(baseName)}.md`;
  const body = stripCommentBlocks(content);
  const out = matter.stringify(body, frontMatter);
  return { destFilename, out };
}

function main() {
  const srcDir = process.argv[2] || '../../../projects';
  const destDir = process.argv[3] || '../../content/projects';
  fs.mkdirSync(destDir, { recursive: true });
  const files = fs
    .readdirSync(srcDir)
    .filter((f) => f.endsWith('.md') || f.endsWith('.markdown'))
    .filter((f) => f !== 'index.markdown' && f !== 'old.markdown');
  for (const f of files) {
    const { destFilename, out } = migrateProject(path.join(srcDir, f));
    fs.writeFileSync(path.join(destDir, destFilename), out, 'utf8');
  }
  console.log(`Migrated ${files.length} project pages to ${destDir}`);
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}
