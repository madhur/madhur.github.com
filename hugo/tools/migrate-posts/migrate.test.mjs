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
