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
