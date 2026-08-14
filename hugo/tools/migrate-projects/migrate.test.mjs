import { test } from 'node:test';
import assert from 'node:assert/strict';
import { convertProjectFrontMatter, stripCommentBlocks } from './migrate.mjs';

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

test('strips dead {% comment %}...{% endcomment %} octokit blocks entirely, including contents', () => {
  const body = `
{% comment %}
<!--
{% if site.generate_projects == true %}
{% octokit_readme dashclock-feedly-extension%}
{% endif %}
-->
{% endcomment %}

This extension notifies you of unread feed items.
`;
  const out = stripCommentBlocks(body);
  assert.equal(out.includes('{% comment %}'), false);
  assert.equal(out.includes('{% endcomment %}'), false);
  assert.equal(out.includes('octokit_readme'), false);
  assert.equal(out.includes('This extension notifies you of unread feed items.'), true);
});

test('leaves body untouched when there is no comment block', () => {
  const body = 'Just a plain description with no Liquid tags.';
  assert.equal(stripCommentBlocks(body), body);
});
