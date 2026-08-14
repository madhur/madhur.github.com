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
