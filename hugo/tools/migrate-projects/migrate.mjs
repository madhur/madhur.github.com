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
